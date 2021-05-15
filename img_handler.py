import requests
import os , requests, glob
from PIL import Image, ImageDraw


imgs = {
    "vs_bg": "./img/vs_bg.png",
    "vs_bg_gif":"./img/vs_bg_gif/frame_*.jpg"
}




async def vs_create(url1:str, url2:str):
    vs_bg = Image.open(os.path.join(imgs["vs_bg"]))
    
    
    size = (150, 150)

    f1 = Image.open( requests.get(url1, stream = True).raw).resize(size)
    f2 = Image.open( requests.get(url2, stream = True).raw).resize(size)

    pos1 = (vs_bg.width//2 - f1.width*2, vs_bg.height//2 - f1.height//2)
    pos2 = (vs_bg.width//2 + f2.width, vs_bg.height//2 - f2.height//2)



    vs_bg.paste(f1, pos1)
    vs_bg.paste(f2, pos2)








    vs_bg.save(os.path.join("./img", "result.png"))



async def vs_create_animated(url1:str, url2:str):
    vs_bg, * img = [Image.open(path) for path in glob.glob(imgs["vs_bg_gif"])]

    size = (120, 120)
 
    f1 = Image.open( requests.get(url1, stream = True).raw).resize(size)
    f2 = Image.open( requests.get(url2, stream = True).raw).resize(size)

    pos1 = (vs_bg.width//2 - f1.width - 100 , vs_bg.height//2 - f1.height)
    pos2 = (vs_bg.width//2 + f2.width - 20 , vs_bg.height//2 - f2.height + 120)

    
    vs_bg.paste(f1, pos1)
    vs_bg.paste(f2, pos2)

    for im in img:
        im.paste(f1, pos1)
        im.paste(f2, pos2)

    vs_bg.save(fp=os.path.join("./img/result.gif"), append_images=img, save_all=True, duration=20, loop=0)

    