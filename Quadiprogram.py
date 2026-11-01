import os
import gc
import torch
from diffusers import AutoPipelineForText2Image
from IPython.display import FileLink, display

print("=== Quadi v0.4: 銃を持ったAI兵士 完全自動生成 起動 ===")

gc.collect()
torch.cuda.empty_cache()

# ----------------------------------------------------
# [フェーズ 1: AI] SDXL で「銃を持った重装甲兵士」をデザイン
# ----------------------------------------------------
prompt = "Full body front view of an elite sci-fi cyber soldier holding a futuristic assault rifle, heavy combat armor, tactical military helmet, cyan glowing visor, camo pattern, game asset, white background, 8k Unreal Engine 5"
design_path = "/kaggle/working/soldier_gun_design.png"

print("\n[1/3] AI (SDXL) が銃兵士のコンセプト画を生成中...")
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda:0")

image = pipe(prompt=prompt, num_inference_steps=2, guidance_scale=0.0).images[0]
image.save(design_path)
print(f"-> 兵士のデザイン画を保存: {design_path}")

del pipe
gc.collect()
torch.cuda.empty_cache()


# ----------------------------------------------------
# [フェーズ 2: Blender] 兵士 ＋ 銃 ＋ AIテクスチャ ＋ 歩行リグ
# ----------------------------------------------------
print("\n[2/3] Blender スクリプトを生成中（銃のモデリング ＆ 警戒歩行リグ）...")

blender_script = f"""
import bpy
import math

bpy.ops.wm.read_factory_settings(use_empty=True)

# --- 1. AIテクスチャ PBRマテリアルの構築 ---
mat = bpy.data.materials.new(name="Soldier_AI_Mat")
mat.use_nodes = True
nodes = mat.node_tree.nodes
principled = nodes.get("Principled BSDF")

tex_node = nodes.new('ShaderNodeTexImage')
tex_node.image = bpy.data.images.load('{design_path}')
mat.node_tree.links.new(principled.inputs['Base Color'], tex_node.outputs['Color'])
principled.inputs['Metallic'].default_value = 0.75
principled.inputs['Roughness'].default_value = 0.35

parts = []
def add_part(name, shape, loc, scale):
    if shape == 'cube':
        bpy.ops.mesh.primitive_cube_add(location=loc, scale=scale)
    elif shape == 'cylinder':
        bpy.ops.mesh.primitive_cylinder_add(location=loc, scale=scale)
    obj = bpy.context.active_object
    obj.name = name
    parts.append(obj)
    return obj

# --- 2. 兵士の肉体・アーマー構築 ---
add_part("Head", 'cube', (0, 0, 1.7), (0.13, 0.15, 0.15))
add_part("Chest", 'cube', (0, 0, 1.3), (0.24, 0.16, 0.22))
add_part("Pelvis", 'cube', (0, 0, 0.95), (0.19, 0.14, 0.10))

# 脚
add_part("Thigh_L", 'cylinder', (0.12, 0, 0.65), (0.08, 0.08, 0.22))
add_part("Shin_L", 'cylinder', (0.12, 0, 0.25), (0.07, 0.07, 0.20))
add_part("Thigh_R", 'cylinder', (-0.12, 0, 0.65), (0.08, 0.08, 0.22))
add_part("Shin_R", 'cylinder', (-0.12, 0, 0.25), (0.07, 0.07, 0.20))

# 腕（銃を前で構える角度）
add_part("UpperArm_L", 'cylinder', (0.28, -0.1, 1.25), (0.06, 0.06, 0.16))
add_part("Forearm_L", 'cylinder', (0.18, -0.28, 1.15), (0.05, 0.05, 0.16))
add_part("UpperArm_R", 'cylinder', (-0.28, -0.05, 1.25), (0.06, 0.06, 0.16))
add_part("Forearm_R", 'cylinder', (-0.15, -0.25, 1.15), (0.05, 0.05, 0.16))

# --- 3. アサルトライフルのモデリング ---
add_part("Rifle_Body", 'cube', (0, -0.35, 1.18), (0.04, 0.25, 0.07))
add_part("Rifle_Barrel", 'cylinder', (0, -0.65, 1.2), (0.015, 0.015, 0.15))
parts[-1].rotation_euler = (math.radians(90), 0, 0)
add_part("Rifle_Mag", 'cube', (0, -0.32, 1.05), (0.03, 0.05, 0.08))
add_part("Rifle_Scope", 'cylinder', (0, -0.35, 1.28), (0.02, 0.02, 0.08))
parts[-1].rotation_euler = (math.radians(90), 0, 0)

# 全パーツ結合
bpy.ops.object.select_all(action='DESELECT')
for p in parts:
    p.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()
soldier_mesh = bpy.context.active_object
soldier_mesh.name = "Armed_Soldier"

# AIテクスチャを全パーツに適用 & プロ仕様UVマッピング
soldier_mesh.data.materials.append(mat)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
bpy.ops.object.mode_set(mode='OBJECT')

# Quadiの魂: 四角形ポリゴンリトポ
bpy.ops.object.quadriflow_remesh(target_faces=2500, use_mesh_symmetry=True)


# --- 4. 骨格（アーマチュア）の構築 ---
bpy.ops.object.armature_add(location=(0, 0, 0))
arm_obj = bpy.context.active_object
arm_data = arm_obj.data

bpy.ops.object.mode_set(mode='EDIT')
eb = arm_data.edit_bones
eb.remove(eb[0])

b_hips = eb.new("Hips")
b_hips.head = (0, 0, 0.9)
b_hips.tail = (0, 0, 1.1)

b_chest = eb.new("Chest")
b_chest.head = (0, 0, 1.1)
b_chest.tail = (0, 0, 1.5)
b_chest.parent = b_hips

b_head = eb.new("Head")
b_head.head = (0, 0, 1.5)
b_head.tail = (0, 0, 1.85)
b_head.parent = b_chest

# 脚の骨
b_thigh_l = eb.new("Thigh_L")
b_thigh_l.head = (0.12, 0, 0.9)
b_thigh_l.tail = (0.12, 0, 0.45)
b_thigh_l.parent = b_hips

b_shin_l = eb.new("Shin_L")
b_shin_l.head = (0.12, 0, 0.45)
b_shin_l.tail = (0.12, 0, 0.05)
b_shin_l.parent = b_thigh_l

b_thigh_r = eb.new("Thigh_R")
b_thigh_r.head = (-0.12, 0, 0.9)
b_thigh_r.tail = (-0.12, 0, 0.45)
b_thigh_r.parent = b_hips

b_shin_r = eb.new("Shin_R")
b_shin_r.head = (-0.12, 0, 0.45)
b_shin_r.tail = (-0.12, 0, 0.05)
b_shin_r.parent = b_thigh_r

bpy.ops.object.mode_set(mode='OBJECT')

# スキニング（自動ウェイト）
bpy.ops.object.select_all(action='DESELECT')
soldier_mesh.select_set(True)
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.parent_set(type='ARMATURE_AUTO')


# --- 5. タクティカル警戒歩行アニメーション (Tactical Walk) ---
bpy.ops.object.mode_set(mode='POSE')
pose = arm_obj.pose

frames = 40
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = frames

for f in range(frames + 1):
    bpy.context.scene.frame_set(f)
    t = (f / frames) * 2 * math.pi

    # 銃を構えたまま力強く歩く足腰
    leg_swing = 0.40 * math.sin(t)
    pose.bones["Thigh_L"].rotation_mode = 'XYZ'
    pose.bones["Thigh_L"].rotation_euler = (leg_swing, 0, 0)
    pose.bones["Thigh_L"].keyframe_insert(data_path="rotation_euler")

    pose.bones["Thigh_R"].rotation_mode = 'XYZ'
    pose.bones["Thigh_R"].rotation_euler = (-leg_swing, 0, 0)
    pose.bones["Thigh_R"].keyframe_insert(data_path="rotation_euler")

    knee_l = max(0.0, -0.55 * math.sin(t))
    knee_r = max(0.0, 0.55 * math.sin(t))
    pose.bones["Shin_L"].rotation_mode = 'XYZ'
    pose.bones["Shin_L"].rotation_euler = (-knee_l, 0, 0)
    pose.bones["Shin_L"].keyframe_insert(data_path="rotation_euler")

    pose.bones["Shin_R"].rotation_mode = 'XYZ'
    pose.bones["Shin_R"].rotation_euler = (-knee_r, 0, 0)
    pose.bones["Shin_R"].keyframe_insert(data_path="rotation_euler")

    # 銃の照準を保つための微小な体幹の揺れ
    bob = 0.02 * math.cos(2 * t)
    pose.bones["Hips"].location = (0, 0, bob)
    pose.bones["Hips"].keyframe_insert(data_path="location")

bpy.ops.object.mode_set(mode='OBJECT')

# --- 6. GLBエクスポート ---
export_path = "/kaggle/working/quadi_armed_soldier.glb"
bpy.ops.export_scene.gltf(
    filepath=export_path,
    export_format='GLB',
    export_animations=True,
    export_skins=True
)
print("Armed Soldier Compile Success: " + export_path)
"""

with open("/kaggle/working/gen_armed_soldier.py", "w") as f:
    f.write(blender_script)

# ----------------------------------------------------
# [フェーズ 3: 実行 & ダウンロード]
# ----------------------------------------------------
print("\n[3/3] ヘッドレスBlenderで3D兵士をコンパイル中...")
!cd /kaggle/working && ./blender-4.2.0-linux-x64/blender -b --python /kaggle/working/gen_armed_soldier.py

final_glb = "/kaggle/working/quadi_armed_soldier.glb"
if os.path.exists(final_glb):
    print("\n★★★ 祝！ 銃を持ったAI兵士が爆誕しました！ ★★★")
    print("以下のリンクをクリックしてダウンロードしてください：\n")
    display(FileLink("quadi_armed_soldier.glb"))
    display(FileLink("soldier_gun_design.png"))
else:
    print("生成エラーが発生しました。ログを確認してください。")
