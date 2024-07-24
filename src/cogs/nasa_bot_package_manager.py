from discord.ext import commands

from src.utils import nasa_bot_logger


class NASABotPackageManager(commands.GroupCog, name="nasa_bot_package_manager"):
    ...


async def setup(bot: commands.Bot):
    """
    Adds the command to the bot when the extension is loaded.

    Args:
        bot (commands.Bot): The bot to add the command to.
    """
    try:
        await bot.add_cog(NASABotPackageManager(bot), guilds=bot.guilds)
    except Exception as e:
        nasa_bot_logger.exception(e)
