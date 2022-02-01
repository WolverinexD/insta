import requests
import os
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message

# Bot Name : Insta Downloader
# Author : Jagadish

header = {
            "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }

## Replace this api_token with yours
api_token = os.getenv("TOKEN")
api_hash = os.getenv("API_HASH")
api_id = int(os.getenv("API_ID"))

app = Client(api_token, api_id, api_hash)


@Client.on_message(filters.command("start"))
async def start(client, m: Message):
    m.reply_text(chat_id = m.chat_id, text = f"Hello {m.from_user.mention}! \nI'm here to download instagram image apart from private accounts")
    m.reply_text(chat_id = m.chat_id, text = "Send me only instagram image link")

@Client.on_message(filters.text & ~filters.edited)
async def dl(client, m: Message):
    url = m.text
    if not url.startswith('https://www.instagram.com/'):
        app.send_message(chat_id = m.chat_id, text = "It may not be instagram link !\nCheck once again and send me")
        return

    response = requests.get(url, headers = header)
    
    if not response.ok:
        app.send_message(chat_id = m.chat_id, text = "Server error! Please try again !")
        return

    soup = BeautifulSoup(response.text,'html.parser')

    img_url = None
    for tag in soup.find_all("meta"):
        if tag.get("property", None) == 'og:image':
            img_url = tag.get('content', None)

    if img_url is None:
        app.send_message(chat_id = m.chat_id, text = "Image is not obtained! Please try again!")
        return

    app.send_photo(chat_id = m.chat_id, photo = img_url)



@Client.on_message(filters.sticker)
async def dl(client, m: Message):
    m.reply_text("Only texts allowed !")
    
if __name__ == "__main__":
    app.start()
