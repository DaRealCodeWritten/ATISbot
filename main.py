import discord
import traceback
from discord.ext import commands

bot = commands.Bot(command_prefix="a!", case_insensitive=True, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("ATIS E is current")


@bot.command(description="Reloads the ATIS module", hidden=True)
async def atisreload(ctx):
    if ctx.author.id != bot.owner_id:
        embed = discord.Embed(title="Access Denied", color=discord.Colour.red(), description="This command is locked")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Are you sure?", color=discord.Colour.red(),
                              description="Reloading the ATIS will destroy all active ATISes, Continue? (y/n)")
        await ctx.send(embed=embed)
        message = await bot.wait_for("message",
                                     check=lambda m: m.author.id == bot.owner_id and m.channel == ctx.channel)
        if "y" not in message.content:
            embed = discord.Embed(title="Cancelled", color=discord.Colour.red(), description="Operation Cancelled")
            await ctx.send(embed=embed)
        elif message.content == "y":
            try:
                bot.reload_extension("cogs.atis")
                embed = discord.Embed(title="Successful", color=discord.Colour.green(),
                                      description="Operation Successful")
                await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(title="Failed", color=discord.Colour.red(),
                                      description="Traceback can be found on STDERR")
                await ctx.send(embed=embed)
                print(e)


bot.load_extension("cogs.atis")
bot.run("")
