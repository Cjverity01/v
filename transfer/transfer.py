#test
import discord
from datetime import datetime
from discord.ext import commands


from core import checks
from core.models import PermissionLevel

options_menu="You have provided invalid dept code.\n\n`dev` - Developers\n`pt` - Partnership Team\n`gs` -Support Team\n`mod` - Moderation Team\n
DEPS_DATA = {
    "dev": {
        "category_id": 692462165470478337,
        "pretty_name": "DEVELOPERS",
        "reminders": "I have transfered this ticket to our developers. Please wait for a response!",
        "role_id": 1322008053469544498,
        "send_message_to_user": True
    },
    "gs": {
        "category_id": 1275836768180113479,
        "pretty_name": "SUPPORT TEAM",
        "reminders": "I have transfered this ticket to support. Please wait.",
        "role_id": 1321985318127403078,
        "send_message_to_user": True
    },
    "mod": {
        "category_id": 1260329657866129559,
        "pretty_name": "MODERATOR",
        "reminders": "I have escalated this tickets to the moderators. Please wait.",
        "role_id": 1256888999277101117,
        "send_message_to_user": True
    },
}
class AYS(commands.Cog, name="AYS Main Commands"):
    def __init__(self, bot):
        self.bot = bot
        
        
       
    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def transfer(self, ctx, *, to: str=None):
        """Command that transfers thread to other departments."""
        if to is None:
            embed = discord.Embed(title=f"Department Transfer", description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            return await ctx.send(embed=embed)
        to = to.lower()
        data = None
        try:
            data = DEPS_DATA[to]
        except:
            embed = discord.Embed(title=f"Department Transfer",description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            return

        if data["send_message_to_user"]:
            mes = "You are being transferred to **`"
            mes += data["pretty_name"]
            mes += "`**.\n"
            mes += "Please remain __patient__ while we find a suitable staff member to assist in your request.\n\n"
            
            if data["reminders"] is not None:
                mes += "**__Reminders__**\n"
                mes += data["reminders"]

            msg = ctx.message
            msg.content = mes
            
            await ctx.thread.reply(msg, anonymous = False)
        
        await ctx.channel.edit(category=self.bot.get_channel(data["category_id"]), sync_permissions=True) 
        await ctx.send("<@&%s>" % str(data["role_id"]))

    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def stransfer(self, ctx, to: str=None):
        """Silently transfers thread"""
        if to is None:
            embed = discord.Embed(title=f"Silent Transfer", description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            return await ctx.send(embed=embed)
        to = to.lower()
        data = None
        try:
            data = DEPS_DATA[to]
        except:
            embed = discord.Embed(title=f"Silent Transfer",description=options_menu,
                                  color=discord.Color.red(), timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            return

        await ctx.channel.edit(category=self.bot.get_channel(data["category_id"]), sync_permissions=True) 
        await ctx.send("Silent Transfer - <@&%s>" % str(data["role_id"]))

    @commands.command()
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def id(self, ctx):
        await ctx.send(ctx.thread.id)

async def setup(bot):
    await bot.add_cog(AYS(bot))
