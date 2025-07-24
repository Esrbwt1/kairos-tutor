from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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