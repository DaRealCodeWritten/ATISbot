import urllib
import requests
from discord.ext import commands


class ATISObject:
    def __init__(self, metar: str, atis_data: dict):
        self.approaches = atis_data["Approaches"]
        self.arr_runways = atis_data["Arr_Runways"]
        self.ident = atis_data["Ident"]
        self.station = atis_data["Station"]
        self.dep_runways = atis_data["Dep_Runways"]
        self.weather = metar
        self.text = None
        self.voice = None

    def generate_text(self):
        base = "http://uniatis.net/atis.php?arr={}&dep={}&apptype={}&info={}&metar={}"
        link = base.format(self.arr_runways, self.dep_runways, self.approaches, self.weather).replace(" ", "%20")
        print(link)
        atis = requests.get(link)
        print(atis)
        self.text = atis

    async def generate_voice(self):




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
        await ctx.send("What arrival runways are active? Separate with ,")
        message = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        await ctx.send("What approach types are active? Separate with ,")
        approaches = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        await ctx.send("What departure runways are active? Separate with ,")
        remarks = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        atis_info = {
            "Arr_Runways": message,
            "Ident": "A",
            "Approaches": approaches,
            "Dep_Runways": remarks,
        }
        metar = self.avwx.get("https://avwx.rest/api/metar/location?options=&airport=true&reporting=true&format=json&onfail=cache")
        self.atises[ctx.author.id] = ATISObject(metar["raw"], atis_info)
        self.atises[ctx.author.id].generate_text()
