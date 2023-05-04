import asyncio
import websockets
import glob, os
import re
import time
from bs4 import BeautifulSoup
import requests
import asyncio

async def send(mes):
            async with websockets.connect("ws://localhost:8765") as websocket:
                await websocket.send(mes)
                await websocket.close()
async def rizzer(): 
        while True:
            bozos = []
            links = open('links.txt', 'r')
            for n in links:
                name = ""
                l = re.search('r/(.+?)/', n)
                if l:
                    name = l.group(1)
                bozos.append(name)
            links.close()
            for b in glob.glob(fr"D:\codus\checker\*.txt"):
                file_name = os.path.basename(b)
                update = os.path.splitext(file_name)[0]
                print(update)
                if str(update) not in bozos:
                    os.remove(fr"D:\codus\checker\{update}.txt")

            links = open('links.txt', 'r')
            for i in links:
                name = ""
                found = ""
                update = str(i.strip('\n'))
                l = re.search('r/(.+?)/', update)
                if l:
                    name = l.group(1)
                print(name)
                url = update 
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                kons = soup.find("a", class_="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE")
                print(response.status_code)
                if response.status_code == 503:
                    continue
                
                text = str(kons)
                m = re.search('href="(.+?)"', text)
                if m:
                    found = m.group(1)
                print(found)
                
                try:
                    riz = open(fr"D:\codus\checker\{name}.txt", "r")
                    i = riz.read()
                    
                    if str(i) == found:
                        riz.close()
                    elif str(i) != found: 
                        riz = open(fr"D:\codus\checker\{name}.txt", "w")
                        riz.write(found)
                        await send(found)
                        riz.close()
                except FileNotFoundError:
                    riz = open(fr"D:\codus\checker\{name}.txt", "w+")
                    riz.write(found)
                    await send(found)
                    riz.close()
                    
                except UnicodeEncodeError:
                    pass
                time.sleep(2)
            
            links.close()
            
            


asyncio.run(rizzer())     