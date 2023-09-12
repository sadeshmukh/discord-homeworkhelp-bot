import nextcord
from nextcord.ext import commands

import os


def main():
    intents = nextcord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(intents=intents)

    @bot.slash_command()
    async def ping(interaction: nextcord.Interaction):
        await interaction.response.send_message("Pong!")


    @bot.slash_command("compile", description="Compile the story text into a channel", )
    async def compile(interaction: nextcord.Interaction, from_channel: nextcord.TextChannel, to_channel: nextcord.TextChannel, spacing: int = 1, show_author: bool = False):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)
            return
        await interaction.response.send_message(f"Purging my messages in {to_channel.mention}...", ephemeral=True)
        await to_channel.purge(check=lambda m: m.author == bot.user)

        await interaction.followup.send(f"Compiling from {from_channel.mention} to {to_channel.mention}...", ephemeral=True)
        history = await from_channel.history(limit=None).flatten()
        no_spoilers = [message for message in history if not message.content.startswith("||") and not message.content.endswith("||")]
        no_spoilers.reverse()
        chunks = []
        current_length = 0
        chunk = ""
        for message in no_spoilers:
            messagecontent = message.content.strip()
            for i in [ "**", "*", "_", "`", "~~", ">", "```"]:
                messagecontent = messagecontent.replace(i, "\\" + i)
            message.content = messagecontent
            
            if current_length + len(message.content) > 2000 - spacing:
                chunks.append(chunk + "\n" * spacing)
                chunk = ""
                current_length = 0

            if show_author:
                chunk += f"{message.author.display_name}: "
            
            chunk += message.content.strip().capitalize() + "\n" * spacing
            current_length += len(message.content) + spacing + len(message.author.display_name) + 2
        chunks.append(chunk)
        for chunk in chunks:
            if chunk == "":
                continue
            print(len(chunk))
            await to_channel.send(chunk)
        await interaction.channel.send("Last updated: " + history[0].created_at.strftime("%Y-%m-%d %H:%M:%S"))
        await interaction.followup.send("Done!", ephemeral=True)
        

    @bot.slash_command("echo", description="Echoes the message back to you")
    async def echo(interaction: nextcord.Interaction, message: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.user.send("what are you trying to do kid")
            return
        await interaction.channel.send(message)


    @bot.listen("on_ready")
    async def on_ready():
        await bot.wait_until_ready()
        await bot.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.listening, name="everything you say"
            )
        )

        print(f"{bot.user.name} has connected to Discord.")
      


    bot.run(os.environ["BOT_TOKEN"])
        

if __name__ == "__main__":
    main()
