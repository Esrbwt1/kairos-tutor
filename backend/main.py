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

# The new endpoint for executing code
@app.post("/api/execute")
async def execute_code(request: CodeRequest):
    # The Rust Playground API endpoint
    PLAYGROUND_URL = "https://play.rust-lang.org/execute"

    # The payload to send to the Playground API
    payload = {
        "channel": "stable",
        "mode": "debug",
        "edition": "2021",
        "crateType": "bin",
        "tests": False,
        "code": request.code,
    }

    # We use an async client to make the external API call without blocking our server
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(PLAYGROUND_URL, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            result = response.json()
            
            # The playground returns 'stdout' on success and 'stderr' on failure/compilation error
            # We will combine them for simplicity, prioritizing stderr if it exists.
            output = result.get("stderr", "") or result.get("stdout", "")
            
            return {"success": True, "output": output}

        except httpx.RequestError as e:
            return {"success": False, "output": f"Error contacting execution server: {e}"}
        except Exception as e:
            return {"success": False, "output": f"An unexpected error occurred: {e}"}