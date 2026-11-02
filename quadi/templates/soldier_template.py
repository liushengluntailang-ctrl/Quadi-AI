def get_assembly_soldier_script(texture_path: str, output_glb_path: str) -> str:
    """階層型アセンブリ（素体＋装甲＋剛体武器ソケット＋歩行アニメーション）スクリプト"""
    return f"""import bpy
import math

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. PBRマテリアル
def create_pbr(name, color, metallic, roughness, emission=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    if emission:
        bsdf.inputs['Emission Color'].default_value = emission
        bsdf.inputs['Emission Strength'].default_value = emission_strength
    return mat

mat_suit  = create_pbr("SuitMat",  (0.05, 0.05, 0.06, 1.0), 0.1,  0.8)
mat_armor = create_pbr("ArmorMat", (0.12, 0.14, 0.13, 1.0), 0.85, 0.3)
mat_gun   = create_pbr("GunMat",   (0.03, 0.03, 0.03, 1.0), 0.95, 0.2)
mat_optic = create_pbr("OpticMat", (1.0, 0.1, 0.1, 1.0), 0.0, 0.1, emission=(1.0, 0.1, 0.1, 1.0), emission_strength=8.0)
mat_visor = create_pbr("VisorMat", (0.0, 0.8, 1.0, 1.0), 0.5, 0.1, emission=(0.0, 0.8, 1.0, 1.0), emission_strength=4.0)

# 2. 人体・アーマー
body_parts = []
def make_body(name, shape, loc, scale, mat):
    if shape == 'cube':
        bpy.ops.mesh.primitive_cube_add(location=loc, scale=scale)
    elif shape == 'cylinder':
        bpy.ops.mesh.primitive_cylinder_add(location=loc, scale=scale)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    body_parts.append(obj)
    return obj

make_body("Head_Base", 'cube', (0, 0, 1.7), (0.11, 0.13, 0.13), mat_suit)
make_body("Torso_Base", 'cube', (0, 0, 1.25), (0.18, 0.13, 0.25), mat_suit)
make_body("Pelvis_Base", 'cube', (0, 0, 0.95), (0.16, 0.12, 0.08), mat_suit)

make_body("Helmet_Armor", 'cube', (0, -0.02, 1.74), (0.13, 0.14, 0.12), mat_armor)
make_body("Visor", 'cube', (0, -0.15, 1.71), (0.10, 0.02, 0.03), mat_visor)
make_body("Chest_Plate", 'cube', (0, -0.06, 1.32), (0.21, 0.10, 0.15), mat_armor)
make_body("Shoulder_L", 'cube', (0.32, -0.05, 1.45), (0.09, 0.09, 0.08), mat_armor)
make_body("Shoulder_R", 'cube', (-0.32, -0.05, 1.45), (0.09, 0.09, 0.08), mat_armor)

make_body("Arm_Upper_L", 'cylinder', (0.28, -0.10, 1.25), (0.06, 0.06, 0.16), mat_suit)
make_body("Arm_Lower_L", 'cylinder', (0.16, -0.28, 1.15), (0.05, 0.05, 0.15), mat_armor)
make_body("Arm_Upper_R", 'cylinder', (-0.28, -0.05, 1.25), (0.06, 0.06, 0.16), mat_suit)
make_body("Arm_Lower_R", 'cylinder', (-0.14, -0.25, 1.15), (0.05, 0.05, 0.15), mat_armor)

make_body("Thigh_L", 'cylinder', (0.12, 0, 0.65), (0.08, 0.08, 0.22), mat_suit)
make_body("Knee_L", 'cube', (0.12, -0.09, 0.45), (0.06, 0.04, 0.06), mat_armor)
make_body("Shin_L", 'cylinder', (0.12, 0, 0.22), (0.07, 0.07, 0.18), mat_armor)
make_body("Thigh_R", 'cylinder', (-0.12, 0, 0.65), (0.08, 0.08, 0.22), mat_suit)
make_body("Knee_R", 'cube', (-0.12, -0.09, 0.45), (0.06, 0.04, 0.06), mat_armor)
make_body("Shin_R", 'cylinder', (-0.12, 0, 0.22), (0.07, 0.07, 0.18), mat_armor)

bpy.ops.object.select_all(action='DESELECT')
for p in body_parts: p.select_set(True)
bpy.context.view_layer.objects.active = body_parts[0]
bpy.ops.object.join()
soldier_body = bpy.context.active_object
soldier_body.name = "Soldier_Body"

# 3. 独立ライフル（直線幾何学）
gun_parts = []
def make_gun(name, shape, loc, scale, rot=(0,0,0), mat=mat_gun):
    if shape == 'cube':
        bpy.ops.mesh.primitive_cube_add(location=loc, scale=scale, rotation=rot)
    elif shape == 'cylinder':
        bpy.ops.mesh.primitive_cylinder_add(location=loc, scale=scale, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    gun_parts.append(obj)
    return obj

make_gun("Gun_Receiver", 'cube', (0, -0.38, 1.18), (0.035, 0.22, 0.06))
make_gun("Gun_Barrel", 'cylinder', (0, -0.68, 1.20), (0.015, 0.015, 0.16), rot=(math.radians(90), 0, 0))
make_gun("Gun_Muzzle", 'cylinder', (0, -0.85, 1.20), (0.022, 0.022, 0.03), rot=(math.radians(90), 0, 0))
make_gun("Gun_Mag", 'cube', (0, -0.35, 1.05), (0.028, 0.05, 0.09), rot=(math.radians(15), 0, 0))
make_gun("Gun_Stock", 'cube', (0, -0.12, 1.16), (0.03, 0.08, 0.05))
make_gun("Gun_Optic", 'cube', (0, -0.38, 1.26), (0.025, 0.06, 0.03))
make_gun("Gun_RedDot", 'cylinder', (0, -0.42, 1.26), (0.012, 0.012, 0.01), rot=(math.radians(90), 0, 0), mat=mat_optic)

bpy.ops.object.select_all(action='DESELECT')
for gp in gun_parts: gp.select_set(True)
bpy.context.view_layer.objects.active = gun_parts[0]
bpy.ops.object.join()
rifle_mesh = bpy.context.active_object
rifle_mesh.name = "Assault_Rifle"

# 4. 骨格 ＆ ウェポンソケット
bpy.ops.object.armature_add(location=(0, 0, 0))
arm_obj = bpy.context.active_object
arm_data = arm_obj.data

bpy.ops.object.mode_set(mode='EDIT')
eb = arm_data.edit_bones
eb.remove(eb[0])

b_hips = eb.new("Hips")
b_hips.head, b_hips.tail = (0, 0, 0.9), (0, 0, 1.1)

b_chest = eb.new("Chest")
b_chest.head, b_chest.tail = (0, 0, 1.1), (0, 0, 1.5)
b_chest.parent = b_hips

b_head = eb.new("Head")
b_head.head, b_head.tail = (0, 0, 1.5), (0, 0, 1.85)
b_head.parent = b_chest

b_arm_r = eb.new("Arm_R")
b_arm_r.head, b_arm_r.tail = (-0.28, -0.05, 1.45), (-0.20, -0.20, 1.25)
b_arm_r.parent = b_chest

b_forearm_r = eb.new("Forearm_R")
b_forearm_r.head, b_forearm_r.tail = (-0.20, -0.20, 1.25), (-0.05, -0.32, 1.15)
b_forearm_r.parent = b_arm_r

b_socket = eb.new("Weapon_Socket")
b_socket.head, b_socket.tail = (-0.05, -0.32, 1.15), (-0.05, -0.45, 1.15)
b_socket.parent = b_forearm_r

b_arm_l = eb.new("Arm_L")
b_arm_l.head, b_arm_l.tail = (0.28, -0.05, 1.45), (0.22, -0.20, 1.25)
b_arm_l.parent = b_chest

b_forearm_l = eb.new("Forearm_L")
b_forearm_l.head, b_forearm_l.tail = (0.22, -0.20, 1.25), (0.05, -0.42, 1.16)
b_forearm_l.parent = b_arm_l

b_thigh_l = eb.new("Thigh_L")
b_thigh_l.head, b_thigh_l.tail = (0.12, 0, 0.9), (0.12, 0, 0.45)
b_thigh_l.parent = b_hips
b_shin_l = eb.new("Shin_L")
b_shin_l.head, b_shin_l.tail = (0.12, 0, 0.45), (0.12, 0, 0.05)
b_shin_l.parent = b_thigh_l

b_thigh_r = eb.new("Thigh_R")
b_thigh_r.head, b_thigh_r.tail = (-0.12, 0, 0.9), (-0.12, 0, 0.45)
b_thigh_r.parent = b_hips
b_shin_r = eb.new("Shin_R")
b_shin_r.head, b_shin_r.tail = (-0.12, 0, 0.45), (-0.12, 0, 0.05)
b_shin_r.parent = b_thigh_r

bpy.ops.object.mode_set(mode='OBJECT')

# 5. アセンブリ接続
bpy.ops.object.select_all(action='DESELECT')
soldier_body.select_set(True)
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# 銃をソケットに直接剛体ロック
rifle_mesh.parent = arm_obj
rifle_mesh.parent_type = 'BONE'
rifle_mesh.parent_bone = "Weapon_Socket"

# 6. 歩行アニメーション
bpy.ops.object.mode_set(mode='POSE')
pose = arm_obj.pose
frames = 40
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = frames

for f in range(frames + 1):
    bpy.context.scene.frame_set(f)
    t = (f / frames) * 2 * math.pi
    leg_swing = 0.42 * math.sin(t)
    
    pose.bones["Thigh_L"].rotation_mode = 'XYZ'
    pose.bones["Thigh_L"].rotation_euler = (leg_swing, 0, 0)
    pose.bones["Thigh_L"].keyframe_insert(data_path="rotation_euler")

    pose.bones["Thigh_R"].rotation_mode = 'XYZ'
    pose.bones["Thigh_R"].rotation_euler = (-leg_swing, 0, 0)
    pose.bones["Thigh_R"].keyframe_insert(data_path="rotation_euler")

    knee_l = max(0.0, -0.6 * math.sin(t))
    knee_r = max(0.0, 0.6 * math.sin(t))
    pose.bones["Shin_L"].rotation_mode = 'XYZ'
    pose.bones["Shin_L"].rotation_euler = (-knee_l, 0, 0)
    pose.bones["Shin_L"].keyframe_insert(data_path="rotation_euler")

    pose.bones["Shin_R"].rotation_mode = 'XYZ'
    pose.bones["Shin_R"].rotation_euler = (-knee_r, 0, 0)
    pose.bones["Shin_R"].keyframe_insert(data_path="rotation_euler")

    bob = 0.02 * math.cos(2 * t)
    pose.bones["Hips"].location = (0, 0, bob)
    pose.bones["Hips"].keyframe_insert(data_path="location")

bpy.ops.object.mode_set(mode='OBJECT')

# 7. エクスポート
bpy.ops.export_scene.gltf(
    filepath='{output_glb_path}',
    export_format='GLB',
    export_animations=True,
    export_skins=True
)
print("Quadi Build Success: {output_glb_path}")
"""
