import string
from discord.ext import commands
from discord import Embed
import requests
class Stunden:
    def __init__(self) -> None:
        self.cols = {1:"Beginn",2:"Ende",3:"Veranstaltung",4:"Art",5:"Dozent",6:"Räume",7:"Bemerkung"}
        self.translated = {
            "Beginn":"",
            "Ende":"",
            "Veranstaltung":"",
            "Art":"",
            "Dozent":"",
            "Räume":"",
            "Bemerkung":""
        }
        pass
class Day:
    def __init__(self,) -> None:
        self.day:string = ""
        self.stunden = []
        pass
class Week:
    def __init__(self) -> None:
        self.days = []
        pass


class htwk(commands.Cog):
    def __init__(self, bot:commands.bot.Bot):
        self.bot = bot

    @commands.command(name="Plan",help="get your INB-1 university shedule")
    async def plan(self,ctx:commands.Context,dayinp=None,weekinp=None):
        url = "https://stundenplan.htwk-leipzig.de/ws/Berichte/Text-Listen;Studenten-Sets;name;21INB-1?template=sws_semgrp"
        if dayinp == "-1":
            dayinp = None
        if weekinp:
            try:
                weekinp = int(weekinp)
                url += "&weeks=_"+str(weekinp)
            except:
                await ctx.send("wrong week input try again")
                return 0
        if dayinp:
            try:
                dayinp = int(dayinp)
            except:
                await ctx.send("wrong day input try again")
        resp = requests.get(url)
        await ctx.send("getting your shedule")
        content = str(resp.content)[7500:]
        i = content[0]
        x = 0
        week = Week()
        while True:
            if i == "<" and "<p><span" in content[x:x+8]:
                while True:
                    x += 1
                    if content[x:x+5] == "<span":
                        x+=25
                        day = Day()
                        while (content[x] != "<"):
                            day.day+=content[x]
                            x+=1
                        break
                row = 0
                col = 0
                while x<len(content)-1:
                    if(content[x:x+7]=="</table"):
                        break
                    if content[x:x+4]=="<tr>":
                        row += 1
                        stunde = Stunden()
                        col = 0
                        if row >=1:
                            while col < 7:
                                if content[x:x+4]=="<td>":
                                    x+=4
                                    col += 1
                                    if col >= 2:
                                        while True:
                                            if(content[x]=="<"):
                                                break
                                            stunde.translated[stunde.cols[col-1]] += str(content[x])
                                            x+=1
                                if content[x:x+5]=="</tr>":
                                    break
                                x+=1
                        day.stunden.append(stunde)
                    x+=1
                week.days.append(day)
                if dayinp:
                    if len(week.days)>dayinp:
                        break
            x+=1
            if x > len(content)-1:
                break
            i = content[x]
        if dayinp != None:
            week.days = [week.days[dayinp]]
        embedvar = Embed(title="Stundenplan",color=0x00ff00)
        for day in week.days:
            if len(day.stunden)>0:
                embedvar.add_field(name=day.day,value="\u200b",inline=False)
            else:
                embedvar.add_field(name=day.day,value="heute Frei",inline=False)
                continue
            for cat in day.stunden[0].cols:
                values = ""
                empty = True
                for x in day.stunden:
                    values += x.translated[x.cols[cat]]+"\n"
                    if x.translated[x.cols[cat]] !="":
                        empty = False
                if empty:
                    values = "\u200b"
                embedvar.add_field(name=day.stunden[0].cols[cat],value=values,inline=True)
            if len(embedvar) >1200:
                await ctx.send(embed=embedvar)
                embedvar = Embed(title="\u200b",color=0x00ff00)
        await ctx.send(embed=embedvar)
