from .echo import Echo

def setup(bot):
    bot.add_cog(Echo(bot))