import os
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageFont


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def thumb(thumbnail, title, userid, ctitle):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"driver/source/81671ed0156630ad5db4e.png", mode="wb")
                await f.write(await resp.read())
                await f.close()
    image1 = Image.open(f"driver/source/81671ed0156630ad5db4e.png")
    final = f"driver/source/81671ed0156630ad5db4e.png"
    return final
