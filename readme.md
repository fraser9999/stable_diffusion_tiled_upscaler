
# **README.md**

````markdown
# Stable Diffusion Tiled Upscaler

A Python-based tiled upscaler for Stable Diffusion (SD-x4).  
This project allows you to upscale large images using small tiles (e.g., 256×256), avoiding GPU memory issues.  
It supports precise tile placement, optional overlap, and soft merge to produce seamless upscaled images.

---

## Features

- Tiled image upscaling (input tiles ~256×256 px)
- Supports x4 Stable Diffusion upscaling
- Optional overlap and soft merge to avoid visible seams
- Handles large images on limited VRAM
- Deterministic per-tile seeding for reproducibility

---

## Requirements

- Python 3.10+
- GPU with CUDA support recommended
- ~6 GB GPU VRAM minimum for 256×256 tiles (Commands missing)
- ~12 GB GPU VRAM minimum for 256×256 tiles (Active for RTX3060)


---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/fraser9999/stable-diffusion-tiled-upscaler.git
cd stable-diffusion-tiled-upscaler
````

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Run the main script:

```bash
python tiled_upscaler_x4.py
```

2. Input the filename of the image you want to upscale when prompted:

```
Filename > path/to/image.png
```

3. The upscaled image will be saved in the same directory as `upscaled_output.png`.

---

## Configuration

* `TILE_SIZE` (default: 256): size of input tiles
* `OVERLAP` (optional): pixels to overlap between tiles
* `UPSCALE_FACTOR` (fixed for SD x4 model)
* `NUM_INFERENCE_STEPS` (default: 40–70)
* `GUIDANCE_SCALE` (default: 7.0–8.0)
* `SEED_BASE`: base seed for deterministic tile generation

Adjust these values in the script as needed.

---

## Notes

* For large images, enabling **overlap + soft merge** improves quality, especially on edges and uniform areas like sky or hair.
* If tiles appear blurry or noisy:

  * Increase `NUM_INFERENCE_STEPS`
  * Adjust `GUIDANCE_SCALE`
  * Ensure seeds are different per tile

---

## License

License. See `LICENSE` file for details.

````

---

# **requirements.txt**

```text
torch>=2.0.0
diffusers>=1.21.0
transformers>=4.30.0
accelerate>=0.21.0
safetensors
numpy>=1.24.0
Pillow>=10.0.0
````

---

💡 **Tip:**

* If using a GPU, ensure **PyTorch is installed with CUDA**. Example:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```



