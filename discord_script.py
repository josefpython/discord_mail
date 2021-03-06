import os
import discord
import mail_fetcher as mf
import time
import json

TOKEN = "fuck enviromental variables i hate them"

client = discord.Client()

@client.event
async def on_ready():
    print('Response script running.')

@client.event
async def on_message(message):

    if(str(message.channel.type)=="private"):

        args = message.content.split(" ")

        if(args[0]=="!email.creds"):

            if(len(args)>2):

                await message.channel.send("Fetching...")

                r = mf.mail_create(args[1],args[2], message.author.id)
                if r == 200:
                    await message.channel.send("Base fetched sucesfully. You will get a DM everytime you receive a new mail.")
                else:
                    await message.channel.send(F"Something went wrong: *{r}*")

            else:
                await message.channel.send("Not enough arguments given.")


    else:

        if(message.content=="!email.login"):

            cassio = open("database.json", "r")
            db = json.load(cassio)
            cassio.close()

            db[message.author.id] = "empty"

            cassio = open("database.json", "w")
            json.dump(db, cassio)
            cassio.close()

            await message.channel.send("Sent you a direct message")

            response = discord.Embed(title="Respond to this message with the following to login:", colour=12)
            response.add_field(value="(replace email and pw with yours, ofc)", name="!email.creds yourname@domain.com passwordToMail")

            await message.author.send(embed=response)

client.run(TOKEN)