import asyncio
import os
import subprocess

import aiohttp
import pyperclip
from dotenv import load_dotenv

load_dotenv()

COPY_TO_CLIPBOARD = True


async def upload(file):
    data = {
        'key': os.getenv('KEY'),
        'file': file
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.upload.systems/images/upload', data=data) as resp:
            return await resp.json()
    
# find ss util location, either maim or scrot
maim_loc = subprocess.run(['whereis','maim'], stdout=subprocess.PIPE).stdout.decode('utf-8')
loc = maim_loc.split(' ')
if len(loc) > 1:
    loc = loc[1]
else:
    scrot_loc = subprocess.run(['whereis','scrot'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    loc = scrot_loc.split(' ')
    if len(loc) > 1:
        loc = loc[1]
    else:
        print('Could not find ss util')
        exit(1)

# get screenshot
process = subprocess.run([loc,'-s','/tmp/screenshot.png'], stdout=subprocess.PIPE)
with open('/tmp/screenshot.png', 'rb') as f:
    img = asyncio.run(upload(f))
if not img.get('error'):
    url = f"https://i.upload.systems/{img['image']['id']}"
    print(url)
    if COPY_TO_CLIPBOARD:
        pyperclip.copy(url)    
else:
    print(img)
subprocess.run(['kitty','icat','/tmp/screenshot.png'], stdout=subprocess.PIPE)

