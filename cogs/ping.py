import discord
from discord import app_commands
from discord.ext import commands


class Ping(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        """
        Creates an instance of the Ping class.

        Args:
            bot (commands.Bot): The discord bot the command is being added to.
        """
        self.bot = bot

    @app_commands.command(name="ping", description="Checks the bot latency.")
    async def ping(self,
                   interaction: discord.Interaction,
                   show_latency: bool = True) -> None:
        """
        Creates the ping command.

        Args:
            interaction (discord.Interaction): Represents the interaction
                                               from discord.
            show_latency (bool): Whether to display the latency in the reply
                                 or not.
        """
        message = "Pong..."
        if show_latency:
            message = f"Pong... {round(self.bot.latency, 2) * 1000}ms"
        await interaction.response.send_message(message)


async def setup(bot: commands.Bot) -> None:
    """
    Adds the commands to a bot when the extension is loaded.

    Args:
        bot (commands.Bot): The bot to add the commands to.
    """
    await bot.add_cog(Ping(bot), guilds=bot.guilds)