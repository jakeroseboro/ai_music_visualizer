import os
import torch
from diffusers import StableDiffusionPipeline
from download_model import ensure_stable_diffusion_download

class SceneGenerator:
    def __init__(self, prompts, output_folder="generated_scenes"):
        self.prompts = prompts
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
        local_model_path = ensure_stable_diffusion_download()
        device = "cuda" if torch.cuda.is_available() else "cpu"
        use_fp16 = device == "cuda"

        self.pipe = StableDiffusionPipeline.from_pretrained(
            local_model_path,
            torch_dtype=torch.float16 if use_fp16 else torch.float32
        )
        self.pipe.to(device)

    def generate(self):
        scene_paths = []
        for idx, prompt in enumerate(self.prompts):
            output_path = os.path.join(self.output_folder, f"scene_{idx}.png")
            if not os.path.exists(output_path):
                print(f"Generating scene {idx+1}: {prompt}")
                image = self.pipe(prompt).images[0]
                image.save(output_path)
            scene_paths.append(output_path)
        return scene_paths
