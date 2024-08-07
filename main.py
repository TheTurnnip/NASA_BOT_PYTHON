import os
import subprocess

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import Config
from src.utils import nasa_bot_logger

if __name__ == "__main__":
    # Sets up the initial state of the discord bot.
    config = Config()
    prefix = str(config.get_unique_item("prefix"))
    token = str(config.get_unique_item("token"))
    guild = discord.Object(config.get_unique_item("guild"))
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    @bot.event
    async def on_ready() -> None:
        """
        Prints bot start status and then loads all extensions if set.
        """
        nasa_bot_logger.info("The bot has started...")
        for file in os.listdir("src/cogs"):
            if file.endswith(".py") and "__init__" not in file:
                extension_file = file[:-3]
                await bot.load_extension(f"src.cogs.{extension_file}")
                nasa_bot_logger.info(f"Extension {extension_file} load "
                                     f"successful...")

    @bot.hybrid_command(name="list_extensions", with_app_command=True)
    @app_commands.guilds(guild)
    @commands.has_permissions(administrator=True)
    async def list_extensions(ctx: commands.Context) -> None:
        """
        Lists all the extensions that are available to the bot.

        Args:
            ctx (discord.ext.commands.Context): The context with which the
                                                command has been invoked.
        """
        description = ""
        counter = 0
        for file in os.listdir("src/cogs"):
            if file.endswith(".py") and "__init__" not in file:
                description = description + f"{counter}. {file[:-3]}\n"
                counter = counter + 1
        embed = discord.Embed(
            title="Available Extensions:",
            description=description,
            color=discord.Color.red()
        )
        try:
            await ctx.reply(embed=embed)
        except Exception as e:
            nasa_bot_logger.exception(e)

    @bot.hybrid_command(name="load_extension", with_app_command=True)
    @app_commands.guilds(guild)
    @commands.has_permissions(administrator=True)
    async def load_extension(ctx: commands.Context, extension="*") -> None:
        """
        Loads all available or a specified extension for the bot.

        Args:
            ctx (discord.ext.commands.Context): The context that the command
                                                was invoked with.
            extension (str): The extension specified by the user that should
                             be loaded. If none is specified then all
                             extensions are loaded.
        """
        try:
            if extension == "*":
                for filename in os.listdir("src/cogs"):
                    if filename.endswith(".py") and "__init__" not in filename:
                        extension_file = filename[:-3]
                        await bot.load_extension(f"src.cogs.{extension_file}")
                        nasa_bot_logger.info(f"Extension {extension_file} "
                                             f"load successful...")
                await ctx.reply("All extensions have been loaded.")
            else:
                await bot.load_extension(f"src.cogs.{extension}")
                message = f"The extension {extension} has been loaded."
                nasa_bot_logger.info(message)
                await ctx.reply(message)
        except commands.ExtensionAlreadyLoaded:
            message = f"The extension {extension} is already loaded."
            nasa_bot_logger.info(message)
            await ctx.reply(message)
        except commands.ExtensionNotFound:
            message = f"The extension {extension} could not be found."
            nasa_bot_logger.warning(message)
            await ctx.reply(message)
        except Exception as exception:
            nasa_bot_logger.error(exception)
            await ctx.reply(f"There was a fatal error loading {extension}, "
                            f"please check the bots logs.")

    @bot.hybrid_command(name="unload_extension", with_app_command=True)
    @app_commands.guilds(guild)
    @commands.has_permissions(administrator=True)
    async def unload_extension(ctx: commands.Context, extension="*") -> None:
        """
        Unloads all loaded or a specified extension.

        Args:
            ctx (discord.ext.commands.Context): The context that the command
                                                was invoked with.
            extension (str): The extension that is to be unloaded. If none is
                             specified then all extensions are unloaded.
        """
        try:
            if extension == "*":
                for filename in os.listdir("src/cogs"):
                    if filename.endswith(".py") and "__init__" not in filename:
                        extension_file = filename[:-3]
                        await bot.unload_extension(f"src.cogs.{extension_file}")
                        nasa_bot_logger.info(f"Extension {extension_file} "
                                             f"unload successful...")
                await ctx.reply("All extensions have been unloaded.")
            else:
                await bot.unload_extension(f"src.cogs.{extension}")
                message = f"The extension {extension} has been unloaded."
                await ctx.reply(message)
                nasa_bot_logger.info(message)
        except commands.ExtensionNotLoaded:
            message = f"The extension {extension} is not loaded."
            await ctx.reply(message)
            nasa_bot_logger.info(message)
        except commands.ExtensionNotFound:
            message = f"The extension {extension} could not be found."
            await ctx.reply(message)
            nasa_bot_logger.warning(message)
        except Exception as exception:
            nasa_bot_logger.error(exception)
            await ctx.reply(f"There was a fatal error loading {extension}, "
                            f"please check the bots logs.")

    @bot.hybrid_command(name="reload_extension", with_app_command=True)
    @app_commands.guilds(guild)
    @commands.has_permissions(administrator=True)
    async def reload_extension(ctx: commands.Context, extension="*") -> None:
        """
        Reloads all the extensions or a specified one.

        Args:
            ctx (discord.ext.commands.Context): The context with which the
                                                command has been invoked.
            extension (str): The extension that is to be reloaded. If none is
                             specified then all extensions are reloaded.
        """
        if extension == "*":
            await unload_extension(ctx)
            await load_extension(ctx)
        else:
            await unload_extension(ctx, extension=extension)
            await load_extension(ctx, extension=extension)

    @bot.hybrid_command(name="sync", with_app_command=True)
    @app_commands.guilds(guild)
    @commands.has_permissions(administrator=True)
    async def sync(ctx: commands.Context) -> None:
        """
        Syncs the app commands (slash commands) to the bot.

        Args:
            ctx (discord.ext.commands.Context): The context with which the
                                                command was invoked.
        """
        try:
            synced = await bot.tree.sync(guild=guild)
            if synced:
                await ctx.channel.send("Slash commands have been synced.")
            else:
                nasa_bot_logger.error("Failed to sync app commands.")
                await ctx.channel.send("Failed to sync the commands.")
        except Exception as e:
            nasa_bot_logger.exception(e)


    @bot.hybrid_command(name="version", with_app_command=True)
    @app_commands.guilds(guild)
    async def version(ctx: commands.Context) -> None:
        """
        Gets the current version of the bot.

        Args:
            ctx (discord.ext.commands.Context): The context with which the
                                                command was invoked.
        """
        response = discord.Embed()
        response.title = f"Version Info:"

        # TODO: Check if the most recent version using git ls-remote.

        await ctx.reply(embed=response)

    @bot.hybrid_command(name="core_reload", with_app_command=True)
    @app_commands.guilds(guild)
    @commands.has_permissions(administrator=True)
    async def core_reload(ctx: commands.Context) -> None:
        """
        Fully restarts the bot.

        Args:
            ctx (discord.ext.commands.Context): The context with which the
                                                command was invoked.
        """
        try:
            nasa_bot_logger.info("Bot is being rebooted...")
            await ctx.reply("The bot is being restarted.")
            subprocess.call(["supervisorctl", "restart", "nasa_bot"])
        except Exception as e:
            nasa_bot_logger.critical("There was an error when trying to "
                                     "reboot!")
            nasa_bot_logger.exception(e)

    bot.run(token)