from fastapi import APIRouter
from enum import Enum

router = APIRouter()

class Tags (Enum):
    worker = 'worker'
    webhook = 'webhook'
    health = 'health'

@router.get("/health", tags=[Tags.worker, Tags.health])
async def health():
    return {"message": "Healthy!"}

@router.post("/worker/start", tags=[Tags.worker, Tags.webhook])
async def worker_start(system:str, use_case:str, itContinous:str = 'false'):
    return {"message": "Task Started!", "system": system, "use_case": use_case}

@router.post("/worker/stop", tags=[Tags.worker, Tags.webhook])
async def worker_stop(system:str, use_case:str):
    return {"message": "Task Stopped!", "system": system, "use_case": use_case}

@router.post("/worker/restart", tags=[Tags.worker, Tags.webhook])
async def worker_restart(system:str, use_case:str):
    return {"message": "Task Restarted!", "system": system, "use_case": use_case}
