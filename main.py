import discord
import random
from discord.ext import commands
from bogo_sort import big_bogo
import time
import requests
import json


client = commands.Bot(command_prefix='//')
client.remove_command("help")

@client.event
async def on_ready():
    print("{0.user} is ready to serve.".format(client))

# @client.command()
# async def help(ctx):
#     embed = discord.Embed(
#         Description="You"
#     )
#     embed.set_author(name="Help Panel")
#     embed.add_field(name="//bogosort", value="Uses the (//bogosort )")
#     await ctx.send(embed=embed)

#Imlpement some restrictions to the user
@client.command()
async def bogosort(ctx, amount):
    await ctx.send("starting BogoSort, if process takes longer than 1 min, it will time out.")
    start_time = time.time()
    tries = big_bogo(int(amount))
    await ctx.send(f"This run took {tries} tries and {time.time() - start_time} second(s) to BogoSort {amount} number(s).")

@client.command()
async def clearbogosort(ctx, amount):

    def is_sorted(x):
        for i in range(len(x) - 1):
            if x[i] > x[i + 1]:
                return False
        return True

    num_list = []
    for i in range(int(amount)):
        num_list.append(i)
    start_time = time.time()
    random.shuffle(num_list)

    tries = 0
    await ctx.send(num_list)
    while not is_sorted(num_list):
        tries += 1
        random.shuffle(num_list)
        await ctx.send(num_list)
    await ctx.send(f"This run took {tries} tries and {time.time() - start_time} second(s) to BogoSort {amount} number(s).")

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    return json_data[0]['q'] + " -" + json_data[0]["a"]

@client.command()
async def inspiration(ctx):
    await ctx.send(get_quote())

@client.event
async def on_message(message):
    author = message.author

    encourage_image = ["http://wvau.org/wp-content/uploads/2019/10/l-44801-your-sadness-me-trying-to-take-your-sadness-away.jpg",
                       "http://www.quickmeme.com/img/e5/e52b0caea5e982ec56bbba511f80b3f86cd32467e10e6ad3e1897acc29bf551e.jpg",
                       "https://www.lovequotesmessages.com/wp-content/uploads/2018/04/white_dogs_encouraging_meme1.jpg",
                       "https://www.lovequotesmessages.com/wp-content/uploads/2018/04/puppy_encouraging_meme1.jpg",
                       "https://www.lovequotesmessages.com/wp-content/uploads/2018/04/kitten_sleeping_encouraging_meme1.jpg",]
    word_list = {"sad", "suicide", "depression", "unhappy", "suicidal"}
    mess = message.content.lower()
    if any(word in mess for word in word_list):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_image(url=random.choice(encourage_image))
        await author.send(embed=embed)
        await author.send(get_quote())
    await client.process_commands(message)

@client.command()
async def _8ball(ctx, *, question):
    responses = ['I have no idea man',
                "I honestly just don't care",
                'Ah, my brain hurts from listening to you talk',
                "Don't wanna answer you",
                'Ask that question again, I dare you',
                'Yea...probably not my dude',
                'Maybe? How would I know',
                "Maybe you'll get the answer if you finally use that brain of yours"
                "That's a negative",
                'You wish',
                "I mean.....sure?",
                "look at me, does it look like I have the answer to that question?"]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

client.run()
