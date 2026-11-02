from quadi import QuadiPipeline

if __name__ == "__main__":
    pipeline = QuadiPipeline()
    glb_path = pipeline.generate(
        prompt="A heavy cybernetic soldier holding a futuristic assault rifle",
        output_name="quadi_walking_soldier.glb"
    )
    print(f"完成アセット: {glb_path}")
