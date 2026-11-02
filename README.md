# 🔷 Quadi AI

> **Next-Generation 3D Asset Generation Pipeline: Quad-Mesh First, Hierarchical Assembly, and Ready-to-Animate.**

Existing 3D generation models (TripoSR, Meshy, etc.) generate monolithic "melted clay" meshes where weapons melt into hands and topology is broken with random triangles. 

**Quadi AI** is designed with the philosophy of professional 3D artists:
1. **Hierarchical Assembly:** Weapons and armor are treated as decoupled, rigid components attached via sockets—never fused into the body.
2. **Quad-Mesh Topology:** Direct conversion to clean quad loops for deformation and animation.
3. **Decoupled PBR:** High-resolution PBR materials (Albedo, Metallic, Roughness, Emissive).
4. **Instant Animation:** Exports `.glb` files with built-in bone rigs and walk cycles, ready for Unity, Unreal, and WebGL.

---

## 🚀 Features

- **Text-to-3D with Animation:** Go from prompt to a walking, rigged `.glb` in seconds.
- **Socket-Based Weapon Binding:** Hard-surface assets (rifles, swords) maintain straight edges and attach rigidly to hand sockets.
- **Headless Blender Integration:** Powered by Blender 4.2 automation under the hood.
- **Resource-Efficient:** Built to run on consumer GPUs and cloud environments (16GB VRAM friendly).

---

## 🛠️ Quick Start

```bash
git clone https://github.com/your-username/quadi-ai.git
cd quadi-ai
pip install -r requirements.txt
