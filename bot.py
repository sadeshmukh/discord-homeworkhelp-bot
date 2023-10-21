import nextcord
from nextcord.ext import commands
import asyncio
import os


def escape(text: str):
    for i in ["**", "*", "_", "`", "~~", ">", "```"]:
        text = text.replace(i, "\\" + i)
    return text.strip()


def main():
    intents = nextcord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(intents=intents)

    @bot.slash_command()
    async def ping(interaction: nextcord.Interaction):
        await interaction.response.send_message("Pong!")

    @bot.slash_command(
        "compile",
        description="Compile the story text into a channel",
    )
    async def compile(
        interaction: nextcord.Interaction,
        from_channel: nextcord.TextChannel,
        to_channel: nextcord.TextChannel,
        spacing: int = 2,
        show_author: bool = False,
    ):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "You must be an administrator to use this command.", ephemeral=True
            )
            return
        await interaction.response.send_message(
            f"Purging my messages in {to_channel.mention}...", ephemeral=True
        )
        await to_channel.purge(check=lambda m: m.author == bot.user)

        await interaction.followup.send(
            f"Compiling from {from_channel.mention} to {to_channel.mention}...",
            ephemeral=True,
        )
        history = await from_channel.history(limit=None).flatten()
        no_spoilers = [
            message
            for message in history
            if not message.content.startswith("||")
            and not message.content.endswith("||")
        ]
        no_spoilers.reverse()
        chunks = []
        current_length = 0
        chunk = ""
        for message in no_spoilers:
            message.content = escape(message.content)
            display = escape(message.author.display_name) if show_author else ""

            if (
                current_length + len(message.content) + spacing + len(display) + 2
                > 2000 - spacing
            ):
                chunks.append(chunk + "\n" * spacing)
                chunk = ""
                current_length = 0

            if show_author:
                chunk += f"{display}: "

            chunk += message.content.strip().capitalize() + "\n" * spacing
            current_length += len(message.content) + spacing + len(display) + 2
        chunks.append(chunk)
        for chunk in chunks:
            if chunk == "":
                continue
            print(len(chunk))
            await to_channel.send(chunk)
        await interaction.channel.send(
            "Last updated: " + history[0].created_at.strftime("%Y-%m-%d %H:%M:%S")
        )
        await interaction.followup.send("Done!", ephemeral=True)

    @bot.listen("on_message")
    async def prob(message: nextcord.Message):
        if message.author.id == bot.user.id:
            return
        if message.mentions and bot.user in message.mentions:
            if message.author.id == 892912043240333322:
                await message.reply("Hi, dad!")
                return
            if message.author.guild_permissions.manage_messages:
                await message.reply("Hi, mod!")
                return
            await message.reply("How ya doin, stupid?")
        if message.content == "p":
            if message.mentions:
                mention = message.mentions[0]
            else:
                mention = None
            await message.channel.send(
                f"""{mention + ' ' if mention else ''}Send a screeenshot of the problem with your question. You can get the screenshot through CPM. \nIf you don't know how to do that, ask a mod for help. \nPlease note that not following the rules or pestering the mods can result in a mute or ban."""
            )
            await message.delete()

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

    @bot.slash_command("loop_msg")
    async def loop_msg(
        interaction: nextcord.Interaction,
        user: nextcord.User,
        message: str,
        interval: int = 10,
        count: int = 10,
    ):
        if (
            not interaction.user.guild_permissions.administrator
            or not interaction.user.id == 892912043240333322
        ):
            await interaction.response.send_message(
                "You must be an administrator to use this command.", ephemeral=True
            )
            return
        for i in range(count):
            await user.send(message)
            await interaction.followup.send(
                f"Sent message {i + 1} of {count} to {user.mention}.", ephemeral=True
            )
            await asyncio.sleep(interval)
        await interaction.followup.send("Done!", ephemeral=True)

    bot.run(os.environ["BOT_TOKEN"])


if __name__ == "__main__":
    main()
