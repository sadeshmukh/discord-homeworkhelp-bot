import os

def setup_env():
  os.environ["BOT_TOKEN"] = open(".secrets/BOT_TOKEN", "r").read().strip()
  os.environ["OPENAI_API_KEY"] = open(".secrets/OPENAI_API_KEY", "r").read().strip()