import aiohttp
import asyncio
from openai import AsyncOpenAI
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
LEWIN = "https://sites.google.com/a/pleasantonusd.net/mr-lewin-s-page_x/ha2-sem1-2-2023-2024"

async def get_lewin_soup():
  async with aiohttp.ClientSession() as session:
    async with session.get(LEWIN) as response:
      text = await response.text()
      return BeautifulSoup(text, "html.parser")

async def get_hw_raw(soup):
  # first = soup.find("div", {"class": "tyJCtd mGzaTb Depvyb baZpAe"}).text.replace("\xa0", "")
  # thing = datetime.now()
  # counter = 0
  # begin = None
  # end = None
  # while not begin:
  #   if counter >= 7:
  #     return None
  #   current = (thing - timedelta(days=counter))
  #   if current.strftime("%-m/%d/%y") in first:
  #     begin = current
  #   counter += 1
  # while not end:
  #   if counter >= 14:
  #     return None
  #   current = (thing - timedelta(days=counter))
  #   if current.strftime("%-m/%d/%y") in first:
  #     end = current
  #   counter += 1
  # barrier = "Assignments Semester 2:- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
  # return first.split(end.strftime("%-m/%d/%y"))[0].split(barrier)[1]

  # that was a goofy way to do it
  # just get last 2000 characters after the barrier
  barrier = "Assignments Semester 2:-"
  return soup.get_text().split(barrier)[1][-2000:]


async def to_legible(raw):
  prompt = """
  Given the raw text, extract the homework assignment. 
  Anything in the below format enclosed in parentheses is something to be replaced with the actual information.
  Output in this format:
  ```
  CLASSWORK: (none)
  HOMEWORK: 7-40 even
  FROM: (textbook, worksheet, etc.)
  You will turn in (fill in the blank).
  ```
  """
  res = await client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": prompt},
      {"role": "user", "content": raw}
    ]
  )
  return res.choices[0].message.content

async def get_hw():
  soup = await get_lewin_soup()
  if not soup:
    return "Could not access Mr. Lewin's page."
  raw = await get_hw_raw(soup)
  if not raw:
    return "No homework found."
  print(raw)
  return await to_legible(raw)
