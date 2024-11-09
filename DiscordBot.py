if __name__ == '__main__' :
    print('\033cStarting ...\n') # Clear Terminal

import os
import dotenv
import discord

dotenv.load_dotenv()

Discord_Token = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
client  = discord.Client(intents=intents)

async def send_message(message, user_message: str) -> None :
    if not user_message :
        print('Intents configured wrongly (probably)')
        return

    try :
        response: str = get_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)

def get_response(user_input:str)->str :
    lowered: str = user_input.lower()
    if 'collecte' in lowered and 'jus' in lowered :
        message = 'Voici le jus'
        raise NotImplementedError #TODO lancer le getinfo et envoyer un message en plus du fichier
    else :
        message = 'kys'

    return message

@client.event
async def on_ready() -> None:
    print(f'{client.user} is running')

@client.event
async def on_message(message) -> None:
    if message.author == client.user:
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

def main() -> None:
    client.run(token=Discord_Token)

if __name__ == '__main__':
    main()