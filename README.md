<div align="center">

# 🔷 Quadi AI

**Next-Generation 3D Asset Generation Pipeline**  
*Quad-Mesh First • Hierarchical Assembly • Ready-to-Animate*

<br>

<!-- 言語切り替えボタン -->
<a href="#english"><img src="https://img.shields.io/badge/English-238636?style=for-the-badge&logo=google-translate&logoColor=white" alt="English"></a>
<a href="#chinese"><img src="https://img.shields.io/badge/中文-de3831?style=for-the-badge&logo=google-translate&logoColor=white" alt="中文"></a>
<a href="#japanese"><img src="https://img.shields.io/badge/日本語-0969da?style=for-the-badge&logo=google-translate&logoColor=white" alt="日本語"></a>

<br><br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Blender 4.2](https://img.shields.io/badge/Blender-4.2+-orange.svg)](https://www.blender.org/)

</div>

---

<a id="english"></a>
## 🌐 English

### 💡 Why Quadi AI?
Most modern 3D generative models (e.g., TripoSR, Meshy) output monolithic "melted clay" meshes where weapons melt into hands and topology is broken.

**Quadi AI breaks this paradigm:**
1. **Hierarchical Assembly:** Weapons and armor are generated as independent hard-surface assets attached via Bone Sockets—never fused into the body.
2. **Quad-Mesh Topology:** Direct quadrangulation via clean edge-loop retopology.
3. **True PBR Materials:** Physical material separation (Rubber suit, Gunmetal steel, Emissive optics).
4. **Built-in Skeletal Animation:** Generates rigged `.glb` files with automatic skinning and walk-cycle loops.

### ⚡ Quick Start
```bash
git clone https://github.com/your-username/quadi-ai.git
cd quadi-ai
pip install -r requirements.txt
python examples/run_soldier.py
```

---

<a id="chinese"></a>
## 🇨🇳 中文

### 💡 为什么选择 Quadi AI？
现有的 3D 生成模型通常生成单一粘连的“融化粘土”网格，武器与手臂融为一体，且三角面混乱无法用于动画。

**Quadi AI 彻底颠覆了这种妥协：**
1. **分层装配（模块化分离）：** 武器和外装甲作为独立模型生成，通过骨骼插槽（Weapon Socket）刚体挂载在手部，绝不粘连。
2. **四边面拓扑优先（Quad-First）：** 规范的四边面布线，专为动画关节拉伸而生。
3. **真实 PBR 物理材质：** 防弹衣、装甲、枪械钢铁与发光瞄具独立分层着色。
4. **内置骨骼动画：** 导出自带骨骼蒙皮与战术行进动画（Walk Cycle）的 `.glb` 文件。

### ⚡ 快速开始
```bash
git clone https://github.com/your-username/quadi-ai.git
cd quadi-ai
pip install -r requirements.txt
python examples/run_soldier.py
```

---

<a id="japanese"></a>
## 🇯🇵 日本語

### 💡 なぜ Quadi AI なのか？
既存の3D生成AIの最大の問題点は、「すべてを一塊の溶けた粘土として出力してしまうこと」でした。

**Quadi AI の特徴：**
1. **階層型アセンブリ：** 武器と装甲を独立パーツとして生成し、「ウェポンソケット」に剛体吸着。銃が手に溶けません。
2. **四角形メッシュ（Quad）優先：** アニメーション時に美しく伸縮するクワッドトポロジー。
3. **本格PBRマテリアル：** スーツ、装甲、スチール銃、発光ドットサイトを素材ごとに完全分離。
4. **歩行アニメーション内蔵：** 骨格と歩行ループが最初から焼き込まれた `.glb` を書き出します。

### ⚡ クイックスタート
```bash
git clone https://github.com/your-username/quadi-ai.git
cd quadi-ai
pip install -r requirements.txt
python examples/run_soldier.py
```

---

## 🗺️ Roadmap

- [x] **v0.1:** Core Hierarchical Assembly & Socket Rigging Pipeline
- [x] **v0.2:** Headless Blender 4.2 Automation & PBR Material Separation
- [ ] **v0.3:** Autonomous LLM Tool-Use (Dynamic Modeling from Arbitrary Prompts)
- [ ] **v0.4:** Multi-view FLUX.1 Texture Projection & Normal Map Baking

---

## 📄 License
Licensed under the [MIT License](LICENSE).
