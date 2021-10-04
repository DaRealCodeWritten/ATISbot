import requests
from discord.ext import commands


class ATISObject:
    def __init__(self, metar: dict, atis_data: dict):
        self.approaches = atis_data["Approaches"]
        self.runways = atis_data["Runways"]
        self.ident = atis_data["Ident"]
        self.station = atis_data["Station"]
        self.weather = metar
        self.text = None
        self.voice = None


class ATISCompiler(commands.Cog, name="ATIS Text Compiler"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.atises = {}
        self.avwx = requests.Session()
        self.avwx.headers = {
            "Authorization": "d0e2VnMeqcFxQi1Mfia7ScjnGH0a1DJ2q2WGTwRvc_s"
        }

    @commands.command(name="make-atis", aliases=["mkatis", "generate"])
    async def _make_atis(self, ctx, icao: str):
        await ctx.send("What arrival runways are active? Separate with /")
        message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        await ctx.send("What approach types are active? Separate with /")
        approaches = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        await ctx.send("What departure runways are active? Separate with /")
        remarks = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        atis_info = {
            "Runways": message.split("/"),
            "Ident": "A|ALPHA",
            "Approaches": approaches,
            "Remarks": remarks,
            "Station": icao
        }
        self.atises[ctx.author.id] = ATISObject()
