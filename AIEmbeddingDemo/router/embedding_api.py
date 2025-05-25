import logging
from fastapi import APIRouter, Request
from utils.support import record_closure

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/triggerWorkflow",tags=["Embedding"], summary="Embedding demo endpoint", description="Embedding demo endpoint")
async def embedding_workflow(request:Request):
    
    session_id = request.headers['Session-Id']
    logging.setLogRecordFactory(record_closure(session_id))
    req_payload = await request.json()
    
    user_input = req_payload.get('user_input')
    chat_history = req_payload.get('chat_history')
    
