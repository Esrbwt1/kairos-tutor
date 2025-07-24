from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import json
from pathlib import Path
from ai_tutor import get_socratic_response

# Create the FastAPI application instance
app = FastAPI()

# --- CORS Middleware ---
# This is crucial for allowing our frontend (running on a different port)
# to communicate with our backend.
origins = [
    "http://localhost:5173", # The default port for Vite React dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------

# --- Load Curriculum Data ---
CURRICULUM = {}
try:
    curriculum_path = Path(__file__).parent / "curriculum" / "rust_ownership.json"
    with open(curriculum_path, "r") as f:
        CURRICULUM = json.load(f)
    print("Curriculum 'rust_ownership.json' loaded successfully.")
except Exception as e:
    print(f"CRITICAL ERROR: Could not load curriculum file. {e}")
# --------------------------

# Define the root endpoint
@app.get("/")
def read_root():
    return {"message": "Connection Established. Welcome to the Kairos Backend."}

@app.get("/api/curriculum/initial")
def get_initial_module():
    # For now, we hard-code returning the very first module.
    # In the future, this could track user progress.
    try:
        initial_module = CURRICULUM["modules"][0]
        return {"success": True, "module": initial_module}
    except (KeyError, IndexError) as e:
        return {"success": False, "error": f"Failed to retrieve initial module: {e}"}

class CodeRequest(BaseModel):
    code: str

@app.post("/api/execute")
async def execute_code(request: CodeRequest):
    PLAYGROUND_URL = "https://play.rust-lang.org/execute"
    payload = {
        "channel": "stable", "mode": "debug", "edition": "2021",
        "crateType": "bin", "tests": False, "code": request.code,
    }

    socratic_message = None

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(PLAYGROUND_URL, json=payload)
            response.raise_for_status()
            result = response.json()
            output = result.get("stderr", "") or result.get("stdout", "")

            # --- REAL SOCRATIC LOGIC ---
            try:
                module = CURRICULUM["modules"][0]
                triggers = module["socraticTriggers"]
                
                has_error_code = any(code in output for code in triggers["errorCodes"])
                has_keyword = any(keyword in output for keyword in triggers["keywords"])

                if has_error_code and has_keyword:
                    # If triggered, call the REAL AI to get a response
                    guiding_question = triggers["initialQuestion"]
                    socratic_message = await get_socratic_response(request.code, output, guiding_question)

            except (KeyError, IndexError):
                pass
            # -----------------------------

            return {"success": True, "output": output, "socratic_message": socratic_message}

        except httpx.RequestError as e:
            return {"success": False, "output": f"Error contacting execution server: {e}", "socratic_message": None}
        except Exception as e:
            return {"success": False, "output": f"An unexpected error occurred: {e}", "socratic_message": None}