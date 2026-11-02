import os
import gc
import torch
from diffusers import AutoPipelineForText2Image

class ImageGenerator:
    """2Dコンセプト・テクスチャ生成エンジン (SDXL-Turbo)"""
    def __init__(self, device: str = "cuda:0", dtype=torch.float16):
        self.device = device
        self.dtype = dtype

    def generate(self, prompt: str, output_path: str = "quadi_design.png") -> str:
        print(f"[ImageGen] プロンプトからデザイン画を生成中: 「{prompt}」")
        
        # 使用時のみロードしてVRAMを最小限に保つ
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=self.dtype,
            variant="fp16"
        ).to(self.device)

        full_prompt = f"{prompt}, game asset, clean isolated background, highly detailed 8k Unreal Engine 5"
        image = pipe(prompt=full_prompt, num_inference_steps=2, guidance_scale=0.0).images[0]
        
        abs_output_path = os.path.abspath(output_path)
        image.save(abs_output_path)
        print(f"[ImageGen] デザイン画を保存しました: {abs_output_path}")

        # VRAM即座解放
        del pipe
        gc.collect()
        torch.cuda.empty_cache()
        
        return abs_output_path
