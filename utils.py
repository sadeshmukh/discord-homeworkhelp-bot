from openai import AsyncOpenAI
import os
from ollama import AsyncClient as OllamaClient
from emoji import emoji_list
import typing
import functools
import asyncio
import logging

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper



client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
ollama_client = OllamaClient() # local - no need for api key

async def ai_response(history, model=None):
  if not model:
    logging.error("No model specified. Defaulting to llama3.")
    model = "llama3"
  if model == "gpt-3.5-turbo":
    res = await client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=history,
    )
    msg = res.choices[0].message.content.strip()
  else:
    res = await ollama_client.chat(model=model, messages=history)
    msg = res["message"]["content"].strip()
  return msg or "I'm sorry, there was an error. Please contact the developer."

async def emoji_summary(m, model=None):
  if not model:
    logging.error("No model specified. Defaulting to llama3.")
    model = "llama3"
  prompt = f"""Summarize the message in a single emoji. Example:
  Bot: I'm doing well.
  
  YOUR SUMMARY: 😊"""
  if model in ["gpt-3.5-turbo"]:
    res = await client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": m}
      ]
    )
    raw = res.choices[0].message.content.strip()
    # search for the first emoji
    if emoji_list(raw):
      return emoji_list(raw)[0]["emoji"]
    return "🤔"
  res = await ollama_client.chat(model=model, messages=[{"role": "system", "content": prompt}, {"role": "user", "content": m}])
  raw = res["message"]["content"].strip()
  # search for the first emoji
  if emoji_list(raw):
    return emoji_list(raw)[0]["emoji"]
  return "🤔"

async def response(history, model="llama3"):
  return await ai_response(history, model=model)