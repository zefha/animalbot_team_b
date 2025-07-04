from fastapi import FastAPI, Request
from animalbot import AnimalAgent

app = FastAPI()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data["message"]
    chat_history = data["chat_history"]
    state = data["state"]
    user_message_count = data.get("user_message_count", 0)

    agent = AnimalAgent(state=state, user_message_count=user_message_count)
    response, log_message = agent.get_response(user_message, chat_history)
    return {"response": response, "state": agent.state}

