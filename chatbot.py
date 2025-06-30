import chainlit as cl
from main import assistant_agent
from agents import Runner

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message(content="👋 Salaam! I'm your AI assistant. How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    prompt = message.content
    history = cl.user_session.get("history") or []

    # Add the latest user message to history
    history.append({"role": "user", "content": prompt})

    # Build the full conversation prompt
    full_prompt = ""
    for item in history:
        role = "User" if item["role"] == "user" else "Assistant"
        full_prompt += f"{role}: {item['content']}\n"

    # Run the assistant on the full context
    result = await Runner.run(assistant_agent, full_prompt)

    # Add the assistant's reply to history
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)

    # Respond with just the latest answer
    await cl.Message(content=f"🤖: {result.final_output}").send()
