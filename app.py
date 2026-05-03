from fastapi import FastAPI
from pydantic import BaseModel
from agent import real_estate_agent
import os
from fastapi import Request
from telegram import Update, Bot
from agent import real_estate_agent

app = FastAPI()

# Initialize the Bot with your Token from @BotFather
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)

@app.post("/telegram")
async def telegram_webhook(request: Request):
    # 1. Get the data sent by Telegram
    data = await request.json()
    update = Update.de_json(data, bot)
    
    # 2. Extract the message and chat ID
    if update.message and update.message.text:
        user_text = update.message.text
        chat_id = update.message.chat_id
        
        # 3. Call your existing LangGraph logic
        inputs = {"user_query": user_text}
        result = await real_estate_agent.ainvoke(inputs)
        answer = result.get("final_response")
        
        # 4. Send the answer back to the user on Telegram
        await bot.send_message(chat_id=chat_id, text=answer)
    
    return {"status": "ok"}


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