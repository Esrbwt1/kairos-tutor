from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

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

# Define the root endpoint
@app.get("/")
def read_root():
    return {"message": "Connection Established. Welcome to the Kairos Backend."}

class CodeRequest(BaseModel):
    code: str

@app.post("/api/execute")
async def execute_code(request: CodeRequest):
    PLAYGROUND_URL = "https://play.rust-lang.org/execute"
    payload = {
        "channel": "stable", "mode": "debug", "edition": "2021",
        "crateType": "bin", "tests": False, "code": request.code,
    }

    socratic_message = None # Our new variable for the AI's message

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(PLAYGROUND_URL, json=payload)
            response.raise_for_status()
            result = response.json()
            
            output = result.get("stderr", "") or result.get("stdout", "")

            # --- MOCK SOCRATIC LOGIC ---
            # This is the first piece of our Socratic Logic Layer.
            # If we detect the specific "moved value" error, we craft
            # our initial Socratic question.
            if "error[E0382]" in output and "moved value" in output:
                socratic_message = (
                    "An interesting error. The compiler mentions a 'moved value'. "
                    "Before we fix it, what is your initial thought on what Rust means by 'move'?"
                )
            # -----------------------------

            return {"success": True, "output": output, "socratic_message": socratic_message}

        except httpx.RequestError as e:
            return {"success": False, "output": f"Error contacting execution server: {e}", "socratic_message": None}
        except Exception as e:
            return {"success": False, "output": f"An unexpected error occurred: {e}", "socratic_message": None}