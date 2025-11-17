# Tiled Stable Diffusion Upscaler
# with Overlapping Function
# Hermann Knopp 2025
# 17.11.2025 Version 0.1a (Erly Alpha)


# init
import os
os.system("cls")
print("importing lips..please wait")

# get py path
dir_path = os.path.dirname(os.path.realpath(__file__))

# Libs
from datetime import datetime

from PIL import Image
import numpy as np
from diffusers import StableDiffusionUpscalePipeline
import torch

# -----------------------------------------------------------
# CONFIG
# -----------------------------------------------------------
TILE_SIZE = 256
MODEL_ID = "stabilityai/stable-diffusion-x4-upscaler"
device = "cuda"

# -----------------------------------------------------------
# PIPELINE LADEN
# -----------------------------------------------------------
pipe = StableDiffusionUpscalePipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16
).to(device)

# Save Memory (uses 12Gb Vram)
pipe.set_use_memory_efficient_attention_xformers(True)


# Save Memory (uses 6Gb - 8Gb Vram)
 
# Memory optimizations
try:
    #pipe.enable_attention_slicing()
    pass
except Exception:
    pass

# optional: try sequential CPU offload (very memory friendly but slower)
try:
    #pipe.enable_sequential_cpu_offload()
    pass
except Exception:
    # not available in all versions
    pass



# -----------------------------------------------------------
# TILE SPLITTER (NICHT RESCALEN!)
# -----------------------------------------------------------
def split_image(img, tile_size=256):
    W, H = img.size
    tiles = []

    for y in range(0, H, tile_size):
        for x in range(0, W, tile_size):
            tile = img.crop((x, y, x + tile_size, y + tile_size))
            w_real, h_real = tile.size  # wichtig für Randkacheln
            tiles.append({
                "img": tile,
                "x": x,
                "y": y,
                "w": w_real,
                "h": h_real
            })

    return tiles, W, H

# -----------------------------------------------------------
# UPSCALER ONE TILE
# -----------------------------------------------------------
def upscale_tile(tile_img, seed=0):
    generator = torch.Generator(device=device).manual_seed(seed)
    
    #prompt="Masterpiece, UHD, 4k, hyper realistic, extremely detailed, professional, vibrant, not grainy, smooth"

    prompt="Masterpiece"
    up = pipe(prompt=prompt, num_inference_steps = 35, guidance_scale = 4.0, image=tile_img, generator=generator).images[0]
    return up

# -----------------------------------------------------------
# COORD MAPPER
# -----------------------------------------------------------
def map_coords(orig_x, orig_y, w_orig, h_orig, w_up, h_up):
    scale_x = w_up / w_orig
    scale_y = h_up / h_orig
    return int(orig_x * scale_x), int(orig_y * scale_y)

# -----------------------------------------------------------
# TILES UPSCALEN
# -----------------------------------------------------------
def upscale_tiles(tiles):
    result = []
    for i, t in enumerate(tiles):

        seed=200 + i

        print("Upscaling Tile ",str(i+1), " with seed ",str(seed))
        up = upscale_tile(t["img"], seed=seed)

        result.append({
            "img": up,
            "x": t["x"],
            "y": t["y"],
            "w_orig": t["w"],
            "h_orig": t["h"]
        })
    return result

# -----------------------------------------------------------
# MERGE OHNE ÜBERLAPPUNGEN
# -----------------------------------------------------------
def merge_tiles(upscaled, W, H):
    # Ausgabe ist (W*4, H*4)
    out = Image.new("RGB", (W*4, H*4))

    for t in upscaled:
        up = t["img"]
        w_up, h_up = up.size

        X, Y = map_coords(
            t["x"], t["y"],
            t["w_orig"], t["h_orig"],
            w_up, h_up
        )

        out.paste(up, (X, Y))

    return out

# -----------------------------------------------------------
# MAIN
# -----------------------------------------------------------
def main():

    os.system("cls")
    print("Hermanns Stable Diffusion x4 Upscaler")
    

    print("\n\n")
    # input image
    fname = input("Enter Image Name (Path)> ").strip().replace("\\", "/").replace("\"", "")

    if not os.path.exists(fname):
        print("File not found:", fname)
        return

    # open image
    img = Image.open(fname)

    # resize image to 512x512px
    print("\n")
    print("Resizing Image to 512x512 for Tiling")
    size=512
    img = img.resize((size, size), Image.Resampling.LANCZOS)


    print("\n")
    # splitting into 4 tiles
    print("Splitting...into 4 Tiles 256x256 px")
    tiles, W, H = split_image(img, TILE_SIZE)

    print("\n")
    # upscaling 1-4 tiles
    print("Upscaling...Start Tasks")
    upscaled = upscale_tiles(tiles)

    print("\n")
    # merging tiles
    print("Merging...")
    out = merge_tiles(upscaled, W, H)

    # Time and Date
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    filename=dir_path +"/" + "upscaled_image_" + dt_string +".png"

    # Save image    
    out.save(filename)

    print("\n")
    # wait user
    print("OK ->", filename)
    a=input("wait key")


# Start Main Loop
if __name__ == "__main__":

    while True:
        main()
