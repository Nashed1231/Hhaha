import discord
from discord.ext import commands
import asyncio
from collections import defaultdict

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Kullanıcıların mesajlarını takip etmek için sözlük (user_id -> [mesajlar])
user_messages = defaultdict(list)
users_to_delete = set()  # Silinecek kullanıcıları takip et

@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yaptı!")

@bot.event
async def on_message(message):
    user_id = message.author.id
    content = message.content

    # Eğer kullanıcı zaten spam yaptıysa, mesajlarını anında sil
    if user_id in users_to_delete:
        await message.delete()
        return

    # Kullanıcının mesajlarını takip et
    user_messages[user_id].append(content)

    # Son 3 mesajı kontrol et
    if len(user_messages[user_id]) >= 3:
        last_three = user_messages[user_id][-3:]
        
        if last_three[0] == last_three[1] == last_three[2]:  # 3 aynı mesaj
            await message.channel.send(f"{message.author.mention}, spam tespit edildi! Bundan sonra attığın tüm mesajlar silinecek.")
            users_to_delete.add(user_id)  # Kullanıcıyı silme listesine ekle

    await bot.process_commands(message)

# Token ile botu başlat
TOKEN = "MTM1MzgzNTkxOTkzNzExNDI1Mw.GWVCFW.xnIlpZ9qAxDZT-FCi3g_C5EWtxsaSuJt4aOiA4"
bot.run(TOKEN)
