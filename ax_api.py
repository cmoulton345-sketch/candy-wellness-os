from fastapi import FastAPI
from pydantic import BaseModel
import os
import subprocess

app = FastAPI(title="Ax OS API", version="1.0.0")

class WriteRequest(BaseModel):
    path: str
    content: str

class CommandRequest(BaseModel):
    command: str

@app.get("/read")
def read_file(path: str):
    try:
        with open(path, "r") as f:
            return {"result": f.read()}
    except Exception as e:
        return {"error": str(e)}

@app.get("/list")
def list_directory(path: str):
    try:
        items = os.listdir(path)
        return {"result": sorted(items)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/write")
def write_file(req: WriteRequest):
    try:
        os.makedirs(os.path.dirname(req.path), exist_ok=True)
        with open(req.path, "w") as f:
            f.write(req.content)
        return {"result": f"✅ Written to {req.path}"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/run")
def run_command(req: CommandRequest):
    try:
        result = subprocess.run(
            req.command, shell=True, capture_output=True,
            text=True, timeout=30
        )
        output = result.stdout + result.stderr
        return {"result": output.strip() or "Command completed with no output"}
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out after 30 seconds"}
    except Exception as e:
        return {"error": str(e)}
