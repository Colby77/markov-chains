"""Generate Markov text from text files."""

import os
import discord
from random import choice


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    content = open(file_path).read()
    words = content.split()

    return words



def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains('hi there mary hi there juanita')

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    for n in range(len(text_string) - 1):
        tup = (text_string[n], text_string[n + 1])
        try:
            if tup in chains:
                chains[tup].append(text_string[n + 2])
            else:
                chains[tup] = []
                chains[tup].append(text_string[n + 2])

        except IndexError:
            chains[tup] = text_string[n]

    return chains



def make_text(chains):
    """Return text from chains."""
    words = []
    link = choice(list(chains.keys()))
    pick = choice(list(chains[link]))
    for n in link:
        words.append(n)
    words.append(pick)
    
    while True:

        try:
            new_link = (words[len(words)-2], words[len(words)-1])
            new_word = choice(list(chains[new_link]))
            words.append(new_word)
        except KeyError:
            break

    return ' '.join(words)



# input_path = 'green-eggs.txt'
# input_path = 'gettysburg.txt'
input_path = 'opis_mutiny.txt'

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
# random_text = make_text(chains)

# print(random_text)


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        print('greeting received')
        await message.channel.send('Hello!')

    if message.content.startswith('markov'):
        random_text = make_text(chains)
        if len(random_text) > 2000:
            random_text = random_text[:2000]
        await message.channel.send(random_text)

client.run(os.environ['DISCORD_TOKEN'])