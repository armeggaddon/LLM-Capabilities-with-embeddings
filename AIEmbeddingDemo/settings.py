import uvicorn
import logging
import subprocess
from config import CONSTS
from fastapi import FastAPI
from router import embedding_api
from utils.support import record_closure

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=CONSTS.app_name,
              description=CONSTS.app_desc)

logging.setLogRecordFactory(record_closure(None))

app.include_router(embedding_api.router)

app.add_middleware(
    CORSMiddleware,
    allow_origin=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    
    
    subprocess.Popen(["chroma", "run", "--host", CONSTS.chroma_host, "--port", CONSTS.chroma_port, "--path", CONSTS.chroma_storage_path])
    subprocess.Popen(["python", f"./bot_interface.py"])
    uvicorn.run("settings:app", host="0.0.0.0", port=int(CONSTS.app_port))
    