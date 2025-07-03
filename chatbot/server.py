from fastapi import FastAPI, Request
from animalbot import AnimalAgent

app = FastAPI()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data["message"]
    chat_history = data["chat_history"]
    state = data["state"]
    
    agent = AnimalAgent(state=state)
    response, log_message = agent.get_response(user_message, chat_history)
    return {"response": response, "state": agent.state}

