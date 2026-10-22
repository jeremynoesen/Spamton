"""
Spamton is a Discord bot that applies Spamton's typing quirk to messages.

Written by Jeremy Noesen
"""

from logging import getLogger
from os import getenv
from discord import Intents, Game, utils
from discord.app_commands import AppInstallationType, AppCommandContext
from dotenv import load_dotenv
from discord.ext.commands import Bot

# Set up logger
utils.setup_logging()
logger = getLogger(__name__)

# Load environment variables from .env file
load_dotenv(override=True)

# List of cogs to load
cogs = [
    "cogs.dealmaker"
]


class Spamton(Bot):
    """
    Main bot class for Spamton
    """


    def __init__(self):
        """
        Initialize the bot with command prefix, intents, and allowed contexts
        """

        super().__init__(command_prefix="/", intents=Intents.default(), allowed_installs=AppInstallationType(guild=True, user=True), allowed_contexts=AppCommandContext(guild=True, dm_channel=True, private_channel=True))


    async def setup_hook(self):
        """
        Upload assets, load cogs, and sync command tree globally.
        :return: None
        """

        # Set bot avatar if it is missing
        if self.user.avatar is None:
            with open("image/profile/avatar.png", "rb") as file:
                await self.user.edit(avatar=file.read())
                logger.info("Uploaded avatar")

        # Set bot banner if it is missing
        if (await self.fetch_user(self.user.id)).banner is None:
            with open("image/profile/banner.png", "rb") as file:
                await self.user.edit(banner=file.read())
                logger.info("Uploaded banner")

        # Load each cog from the COGS list
        for cog in cogs:
            await self.load_extension(cog)
            logger.info(f"Loaded cog: {cog}")

        # Sync command tree globally
        await self.tree.sync()
        logger.info("Command tree synced")


    async def on_ready(self):
        """
        Indicate that the bot is ready.
        :return: None
        """

        logger.info(f"Logged in: {self.user}")


# Run the bot
if __name__ == "__main__":
    Spamton().run(str(getenv("DISCORD_BOT_TOKEN")), log_handler=None)