"""
Module to handle the Dealmaker command.

Written by Jeremy Noesen
"""

from logging import getLogger
from random import randint
from discord import Interaction, Message
from discord.ext.commands import Cog
from discord.app_commands import ContextMenu

# Set up logger
logger = getLogger(__name__)


class Dealmaker(Cog):
    """
    Cog that handles the Dealmaker command
    """


    def __init__(self, bot):
        """
        Initialize the cog
        :param bot: The bot instance
        """

        self.bot = bot
        self.bot.tree.add_command(ContextMenu(
            name="Dealmaker",
            callback=self.dealmaker
        ))


    async def dealmaker(self, interaction: Interaction, message: Message):
        """
        Make Spamton repeat a message with his typing quirk.
        :param interaction: Interaction created by the context menu command
        :param message: Message the command was run on
        :return: None
        """

        # Split up message by words
        words = message.content.split(" ")

        # Variables to keep track of processing state
        output = ""
        inside = False

        # Iterate through each word
        for word in words:

            # Randomly decide whether to format the word in brackets
            if randint(0, 4) == 0 or inside:

                # Start a new bracket
                if not inside:
                    output += "[["

                # Add word in titlecase
                output += word[0].upper() + word[1:].lower()

                # Randomly decide whether to close the bracket
                if randint(0, 1) == 0:
                    output += "]] "
                    inside = False

                # Otherwise, keep the bracket open
                else:
                    output += " "
                    inside = True

            # If not inside brackets, just add the word in uppercase
            else:
                output += word.upper() + " "

        # Clean up the output
        output = output.rstrip()

        # If still inside brackets, close them
        if inside:
            output += "]]"

        # Send the final output as a response to the interaction
        await interaction.response.send_message(output)


async def setup(bot):
    """
    Register the Dealmaker cog with the bot.
    :param bot: The bot instance
    :return: None
    """

    # Register cog
    await bot.add_cog(Dealmaker(bot))