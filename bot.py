import nextcord
from nextcord.ext import commands



def main():
    intents = nextcord.Intents.all()
    bot = commands.Bot(intents=intents)

    @bot.slash_command()
    async def ping(interaction: nextcord.Interaction):
        await interaction.response.send_message("Pong!")


    bot.run("token")
        

if __name__ == "__main__":
    main()
