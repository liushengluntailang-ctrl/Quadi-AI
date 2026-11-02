import os
from quadi.generators.image_gen import ImageGenerator
from quadi.dcc.blender_runner import BlenderRunner
from quadi.templates.soldier_template import get_assembly_soldier_script

class QuadiPipeline:
    """Quadi 3D アセット生成パイプライン"""
    def __init__(self, work_dir: str = "/kaggle/working"):
        self.work_dir = os.path.abspath(work_dir)
        os.makedirs(self.work_dir, exist_ok=True)
        self.img_gen = ImageGenerator()
        self.dcc = BlenderRunner(base_dir=self.work_dir)

    def generate(self, prompt: str, output_name: str = "quadi_asset.glb") -> str:
        output_glb_path = os.path.join(self.work_dir, output_name)
        design_img_path = os.path.join(self.work_dir, "design.png")
        script_path = os.path.join(self.work_dir, "build_script.py")

        # 1. 2D意匠生成
        self.img_gen.generate(prompt=prompt, output_path=design_img_path)

        # 2. Blenderアセンブリスクリプトの生成
        blender_code = get_assembly_soldier_script(
            texture_path=design_img_path,
            output_glb_path=output_glb_path
        )
        with open(script_path, "w") as f:
            f.write(blender_code)

        # 3. ヘッドレスBlenderによるコンパイル
        success = self.dcc.run_script(script_path)
        if success and os.path.exists(output_glb_path):
            print(f"\n[Quadi] 3Dアセット生成完了: {output_glb_path}")
            return output_glb_path
        else:
            raise RuntimeError("[Quadi] 3Dアセットのビルドに失敗しました。")
