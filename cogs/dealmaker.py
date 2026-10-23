"""
Module to handle the Dealmaker command.

Written by Jeremy Noesen
"""

from logging import getLogger
from random import randint
from discord import Interaction, Message
from discord.ext.commands import Cog
from discord.app_commands import ContextMenu
from emoji import replace_emoji
from re import sub

# Set up logger
logger = getLogger(__name__)

# Words to misspell
misspelled_words = {
    "generosity": "genorisity",
    "guarantee": "guaranttee",
    "delicious": "delicis",
    "special": "specil"
}


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
        words = replace_emoji(sub(r"<a?:\w+:\d+>", "", message.content), "").lower().split()

        # Number of characters to use for the entire message per bracket
        brackets = randint(1, 2)

        # Variables to keep track of processing state
        output = ""
        inside = False

        # Iterate through each word
        for word in words:

            # Replace words that need to be misspelled
            if word in misspelled_words:
                word = misspelled_words[word]

            # Randomly decide whether to format the word in brackets
            if inside or randint(0, 4) == 0:

                # Start a new bracket
                if not inside:
                    output += "[" * brackets

                # Add word in titlecase
                output += word.title()

                # Randomly decide whether to close the bracket
                if randint(0, 1) == 0:
                    output += "]" * brackets + " "
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
            output += "]" * brackets

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