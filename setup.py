import os
from bot import main


os.environ["BOT_TOKEN"] = open(".secrets/BOT_TOKEN", "r").read().strip()
main()
