import os

def setup_env():
  os.environ["BOT_TOKEN"] = open(".secrets/BOT_TOKEN", "r").read().strip()
  os.environ["OPENAI_API_KEY"] = open(".secrets/OPENAI_API_KEY", "r").read().strip()
  os.environ["GUILD_ID"] = open(".secrets/GUILD_ID", "r").read().strip()
  os.environ["CHANNEL_ID"] = open(".secrets/CHANNEL_ID", "r").read().strip()
  os.environ["BOT_MOD_ROLE"] = open(".secrets/BOT_MOD_ROLE", "r").read().strip()