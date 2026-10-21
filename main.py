from random import randint
from discord import Interaction, Message, Client, Intents, app_commands, utils
from dotenv import load_dotenv
from os import getenv
from logging import getLogger

# Set up logger
utils.setup_logging()
logger = getLogger(__name__)

# Load environment variables from .env file
load_dotenv(override=True)

# Initialize Discord client and command tree
client = Client(intents=Intents.default())
command_tree = app_commands.CommandTree(client)

@command_tree.context_menu(name="Dealmaker")
async def dealmaker(interaction: Interaction, message: Message):
    """
    Make Spamton say a message in his signature style.
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


@client.event
async def setup_hook():
    """
    Sync command tree globally.
    :return: None
    """

    await command_tree.sync()
    logger.info("Command tree synced")


@client.event
async def on_ready():
    """
    Indicate that the bot is ready.
    :return: None
    """

    logger.info(f"Logged in: {client.user}")

# Run the bot
if __name__ == "__main__":
    client.run(str(getenv("DISCORD_BOT_TOKEN")), log_handler=None)