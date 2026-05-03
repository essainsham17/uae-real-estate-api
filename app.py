from fastapi import FastAPI
from pydantic import BaseModel
from agent import real_estate_agent

app = FastAPI()

class UserQuery(BaseModel):
    user_message: str = 'essa'
    thread_id: str = 'default_session'

class ChatResponse(BaseModel):
    ai_response: str

@app.post('/chat',response_model=ChatResponse)
async def handle_chat(request: UserQuery):
    current_message=request.user_message
    current_thread=request.thread_id

    inputs={"user_query":current_message}

    result=await real_estate_agent.ainvoke(inputs)
    answer=result["final_response"]
    
    return {"ai_response": answer}