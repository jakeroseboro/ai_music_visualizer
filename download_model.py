import os
from huggingface_hub import snapshot_download

def ensure_stable_diffusion_download(model_dir="./models/stable-diffusion-v1-4"):
    if os.path.exists(model_dir):
        print(f"✅ Stable Diffusion model already exists at {model_dir}")
        return model_dir

    print(f"⬇️  Downloading Stable Diffusion model to {model_dir}...")
    snapshot_download(
        repo_id="CompVis/stable-diffusion-v1-4",
        repo_type="model",
        local_dir=model_dir,
        local_dir_use_symlinks=False,
    )
    print(f"✅ Download complete: {model_dir}")
    return model_dir

# If you want to directly run this file
if __name__ == "__main__":
    ensure_stable_diffusion_download()
