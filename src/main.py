from datetime import datetime
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    current_time = datetime.now()
    unix_timestamp = int(current_time.timestamp())
    return {"current_time": unix_timestamp}

