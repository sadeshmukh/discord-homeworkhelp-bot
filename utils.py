from openai import AsyncOpenAI
import os
from ollama import AsyncClient as OllamaClient
from emoji import emoji_list

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
ollama_client = OllamaClient() # local - no need for api key

async def openai_response(history):
  print("Generating response...")
  res = await client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=history,
  )
  try:
    print("response generated")
    return res.choices[0].message.content.strip()
  except Exception as e:
    print(e)
    return "I'm sorry, I couldn't generate a response."
  
async def llama_response(history, model="llama3"):
  messages = [{**m, "images": []} for m in history] # remove images
  res = await ollama_client.chat(model=model, messages=messages)
  return res["message"]["content"].strip()

async def llava_response(history):
  print(history)
  res = await ollama_client.chat(model="llava", messages=history)
  return res["message"]["content"].strip()

async def llama_emoji_summary(m):
  prompt = f"""Summarize the message in a single emoji. Example:
  Bot: I'm doing well.
  
  YOUR SUMMARY: 😊"""
  res = await ollama_client.chat(model="llama3", messages=[{"role": "system", "content": prompt}, {"role": "user", "content": m}])
  raw = res["message"]["content"].strip()
  # search for the first emoji
  if emoji_list(raw):
    return emoji_list(raw)[0]["emoji"]
  return "🤔"
async def response(history, model="llama3"):
  if model == "gpt-3.5-turbo":
    return await openai_response(history)
  elif model == "llava":
    return await llava_response(history)
  elif model == "llama3":
    return await llama_response(history)
  else:
    print(f"Error: invalid model type. Defaulting to OpenAI. {type}")
    return await openai_response(history)