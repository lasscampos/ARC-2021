import discord
import random

intents = discord.Intents.default()
intents.members = True

client = discord.Client()

@client.event
async def on_ready():
    print("O MÃE TA ON")


@client.event
async def on_message(message):
    txt = message.content.lower()
    canal = message.channel
    autor = message.author.name
    user = message.author.mention

    #Impedir que role erro
    if(autor == "LaLeBot"):
        return 
    
    if(txt == "alo"):
        await canal.send("Olá")

    if(txt == "teste"):
        await canal.send("Testado" + user)

    if(txt == "bom dia"):
        await canal.send("Bom dia"  + user)

    if(txt == "roleta"):
        choice = random.randint(1,2)
        if(choice == 1):
            await canal.send(user + "Você ta vivo")
        if(choice == 2):
            await canal.send(user + "Você ta morto")

client.run("ODY0NTI0Nzg3MjY2MzU1MjEw.YO2tcw.dxizkll2qe8Oi328msLLb5hnHhM")