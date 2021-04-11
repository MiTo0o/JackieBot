import discord
import random
from discord.ext import commands
from bogo_sort import big_bogo
import time
import requests
import json
import copy_pasta
import praw
import keys

client = commands.Bot(command_prefix='-')
client.remove_command("help")

reddit = praw.Reddit(client_id=keys.REDDIT_ID,
                     client_secret=keys.REDDIT_SECRECT,
                     username=keys.REDDIT_USERNAME,
                     password=keys.REDDIT_PASS,
                     user_agent="praw_boi"
                     )


def get_inspirational_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    return json_data[0]['q'] + " -" + json_data[0]["a"]


def get_insult(author):
    response = requests.get("https://insult.mattbas.org//api/insult.json?who=" + author)
    json_data = json.loads(response.text)
    return json_data['insult']


@client.event
async def on_ready():
    print("{0.user} is ready to serve.".format(client))
    await client.change_presence(activity=discord.Game(name="-help"))


@client.command()
async def help(ctx):
    embed = discord.Embed(
        description="Looks like you need some help"
    )
    embed.set_author(name="Help Panel")
    embed.set_image(url="https://i.chzbgr.com/full/7651270400/h678A1618/help")
    embed.add_field(name="-asciihelp", value="Displays the possible ascii art commands", inline=False)
    embed.add_field(name="-bogosort  ***amount***", value="(uses best sorting algorithm to sort an array of numbers)",inline=False)
    embed.add_field(name="-clearbogosort  ***amount***", value="(logs the sorting process)", inline=False)
    embed.add_field(name="-8ball  ***question***", value="(magic 8ball answers a yes or no question)", inline=False)
    embed.add_field(name="-inspiration", value="(gets a inspirational quote from api)", inline=False)
    embed.add_field(name="-insult  ***name***", value="(THIS API CONTAINS LOTS OF NSFW INSULTS, USE WITH CAUTION)", inline=False)
    embed.add_field(name="-rps ***rock, paper, or scissor***", value="(plays a never winning rps game with the bot)", inline=False)
    embed.add_field(name="-bigspam", value="(spams the channel with lots of lines)", inline=False)
    embed.add_field(name="-sreddit  ***posts(top of all time)***  ***subreddit***", value="(uses reddit api to return random top post)", inline=False)
    await ctx.send(embed=embed)


@client.command()
async def asciihelp(ctx):
    embed = discord.Embed(
        description="Looking for some ascii art?"
    )
    embed.set_author(name="ASCII Art Help Panel")
    embed.add_field(name="-bongocat  ***amount***(of times it hits the table)", value="Sends a cat \"hitting\" a bongo/table", inline=False)
    embed.add_field(name="-penguin", value="Sends penguin ascii art", inline=False)
    embed.add_field(name="-monkey", value="Sends monkey ascii art", inline=False)
    embed.add_field(name="-catto", value="Sends cat ascii art", inline=False)
    embed.add_field(name="-yoshi", value="Sends yoshi ascii art", inline=False)
    await ctx.send(embed=embed)


@client.command()
async def bogosort(ctx, amount):
    await ctx.send("starting BogoSort, if process takes longer than 1 min, it will time out.")
    start_time = time.time()
    tries = big_bogo(int(amount))
    await ctx.send(
        f"This run took {tries} tries and {time.time() - start_time} second(s) to BogoSort {amount} number(s).")


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
    await ctx.send(
        f"This run took {tries} tries and {time.time() - start_time} second(s) to BogoSort {amount} number(s).")


@client.command()
async def inspiration(ctx):
    await ctx.send(get_inspirational_quote())


@client.command()
async def insult(ctx, *, name):
    await ctx.send(get_insult(name))


@client.event
async def on_message(message):
    author = message.author

    encourage_image = [
        "http://wvau.org/wp-content/uploads/2019/10/l-44801-your-sadness-me-trying-to-take-your-sadness-away.jpg",
        "http://www.quickmeme.com/img/e5/e52b0caea5e982ec56bbba511f80b3f86cd32467e10e6ad3e1897acc29bf551e.jpg",
        "https://www.lovequotesmessages.com/wp-content/uploads/2018/04/white_dogs_encouraging_meme1.jpg",
        "https://www.lovequotesmessages.com/wp-content/uploads/2018/04/puppy_encouraging_meme1.jpg",
        "https://www.lovequotesmessages.com/wp-content/uploads/2018/04/kitten_sleeping_encouraging_meme1.jpg", ]
    word_list = {"sad", "suicide", "depression", "unhappy", "suicidal"}
    mess = message.content.lower()
    if any(word in mess for word in word_list):
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_image(url=random.choice(encourage_image))
        await author.send(embed=embed)
        await author.send(get_inspirational_quote())
    await client.process_commands(message)


@client.command(aliases=['8ball', 'eight_ball', 'eightBall', 'eightball'])
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


@client.command()
async def rps(ctx, *, user_input):
    input = user_input.lower()
    if input == "rock" or input == "r":
        await ctx.send("Paper, YOU LOSE!!!")
    elif input == "paper" or input == "p":
        await ctx.send("Scissor, YOU LOSE!!!")
    elif input == "scissor" or input == "s":
        await ctx.send("Rock, YOU LOSE!!!")
    else:
        await ctx.send("Wrong input, please send r,p,s or Rock, Paper, Scissor")


@client.command()
async def sreddit(ctx, limit1=10, *, sub=None):
    sub = sub or 'ProgrammerHumor'
    subreddit = reddit.subreddit(sub).top(limit=limit1)
    all_top_posts = []
    for post in subreddit:
        all_top_posts.append(post)
    rand_post = random.choice(all_top_posts)
    name = rand_post.title
    url = rand_post.url

    embed = discord.Embed(
        title=name
    )
    embed.set_image(url=url)
    await ctx.send(embed=embed)


@client.command()
async def bigspam(ctx):
    for iqwesf in range(5):
        await ctx.send(copy_pasta.long_spam)


@client.command()
async def bongocat(ctx, limit=5):
    for xd in range(limit):
        time.sleep(1.4)
        await ctx.send(copy_pasta.bongo_cat1)
        time.sleep(1.4)
        await ctx.send(copy_pasta.bongo_cat2)


@client.command()
async def penguin(ctx):
    await ctx.send(copy_pasta.penguin)


@client.command()
async def monkey(ctx):
    await ctx.send(copy_pasta.monkey_boi)


@client.command()
async def catto(ctx):
    await ctx.send(copy_pasta.catto)


@client.command()
async def yoshi(ctx):
    await ctx.send(copy_pasta.yoshi)


client.run(keys.TOKEN)
