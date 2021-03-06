import time
import os
import discord
import json
import mail_fetcher as mf
import email.header

def cfix(s):
    return u''.join(
        word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(s))

TOKEN = "tokenincodeYEAH"

client = discord.Client()

@client.event
async def on_ready():
    print("Checking script running.")

    cassio = open("database.json", "r")
    db = json.load(cassio)
    cassio.close()

    while True:        

        for key in db.keys():

            newmail = mf.gatherMail(db[key]["creds"][0],db[key]["creds"][1])

            if( db[key]["mailhistory"] ==  newmail ):
                print(F"current and old mail matches on {key}")

            else:

                print(F"current and old mail mismatch on {key}")

                emb = discord.Embed(title="New message", colour=discord.Colour.magenta())

                emb.add_field(name=cfix(newmail[0]), value=cfix(newmail[1]))

                receiver = await client.fetch_user(int(key))
                await receiver.send(embed=emb)

                db[key]["mailhistory"] = newmail

                cassio = open("database.json", "w")
                json.dump(db, cassio)
                cassio.close()

        time.sleep(60)

client.run(TOKEN)