#Announcement-Bot V1.0
import discord
from discord.ext import commands
import os
import platform
from yaml import load, dump
import yaml

bot = commands.Bot(description="Announcement Bot", command_prefix="!", pm_help = True) #you can change here the prefix
game = discord.Game("<help for help")  #change here the game

with open("config.yaml") as file: #load token from config file
        data = load(file)
        token = data["token"]
        user = data["user"]

with open("channels.yaml", encoding='utf-8') as file: #load other channels
        data = load(file)
        channels = data["channels"]

#---bot start---
@bot.event
async def on_ready(): # terminal message on start
	print('Logged in as '+bot.user.name+' (ID:'+str(bot.user.id)+') | Connected to '+str(len(bot.guilds))+' servers')
	print('--------')
	await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command(brief='Measure delays') #ping command
async def ping(ctx):
        await ctx.send(':ping_pong: Pong! ~' + str(round(bot.latency * 1000, 2)) + " ms")

@bot.command(brief='ann [message]')
async def ann(ctx, message : str): #unload extension
        print(str(message))
        if(str(ctx.message.author) == user): #compare usernames
                await ctx.send('user auth ok')
                try:
                        for chan in channels:
                                try:
                                        channel = bot.get_channel(chan)
                                        info = discord.Embed(title='Announcement!', description=str(message), color=0xFFFFFF)
                                        await channel.send(embed=info)
                                except Exception as e:
                                        await ctx.send(e)
                                        await ctx.send("Error: " + str(chan))
                except Exception as e:
                        await ctx.send(e)

@bot.command(pass_context=True, brief='Add to update list')
async def addtolist(ctx):
        if ctx.message.author.guild_permissions.administrator: #does user have admin rights?
                ad_ch = ctx.message.channel.id #get channel id
                
                with open("channels.yaml", encoding='utf-8') as file: #load all channels in list
                        datachan = load(file)
                if ad_ch in datachan["channels"]: #channel already in update list
                        await ctx.send('Already in update list')
                else: #channel not in update list
                        datachan["channels"].append(ad_ch) #add channel
                        channels.append(ad_ch)

                        with open('channels.yaml', 'w') as writer: #save new file
                            yaml.dump(datachan, writer)

                        await ctx.send('Added channel')
        else:
                await ctx.send('You are not allowed to use this command')

@bot.command(pass_context=True, brief='Remove from update list')
async def removefromlist(ctx):
        if ctx.message.author.guild_permissions.administrator: #does user have admin rights?

                re_ch = ctx.message.channel.id #get channel id
                
                with open("channels.yaml", encoding='utf-8') as file: #load other channels
                        datachan = load(file)
                try:
                        datachan["channels"].remove(re_ch) #remove channel
                        channels.remove(re_ch)

                        with open('channels.yaml', 'w') as writer: #save new file
                                yaml.dump(datachan, writer)
                
                        await ctx.send('Removed channel')
                except:
                        await ctx.send('An error occured :|')
        else:
                await ctx.send('You are not allowed to use this command')

bot.run('{}'.format(token))
