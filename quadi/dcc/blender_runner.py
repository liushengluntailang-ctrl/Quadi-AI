import os
import subprocess
import urllib.request
import tarfile

class BlenderRunner:
    """ヘッドレスBlenderの自動セットアップ & 実行エンジン"""
    def __init__(self, base_dir: str = "/kaggle/working"):
        self.base_dir = os.path.abspath(base_dir)
        self.blender_dir = os.path.join(self.base_dir, "blender-4.2.0-linux-x64")
        self.blender_bin = os.path.join(self.blender_dir, "blender")

    def ensure_installed(self):
        """Blenderがなければ公式から自動ダウンロード＆解凍"""
        if not os.path.exists(self.blender_bin):
            print("[BlenderRunner] Blender 4.2 本体が見つからないため、自動ダウンロード中...")
            tar_path = os.path.join(self.base_dir, "blender-4.2.0-linux-x64.tar.xz")
            url = "https://download.blender.org/release/Blender4.2/blender-4.2.0-linux-x64.tar.xz"
            
            if not os.path.exists(tar_path):
                urllib.request.urlretrieve(url, tar_path)
            
            print("[BlenderRunner] 解凍中...")
            subprocess.run(["tar", "-xf", tar_path, "-C", self.base_dir], check=True)
            print("[BlenderRunner] Blender 4.2 セットアップ完了！")
        return self.blender_bin

    def run_script(self, script_path: str) -> bool:
        """PythonスクリプトをヘッドレスBlenderに流し込んで実行"""
        self.ensure_installed()
        abs_script_path = os.path.abspath(script_path)
        
        print(f"[BlenderRunner] Blenderをヘッドレス実行中: {abs_script_path}")
        result = subprocess.run(
            [self.blender_bin, "-b", "--python", abs_script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"[BlenderRunner] エラー発生:\n{result.stderr}")
            return False
        return True
