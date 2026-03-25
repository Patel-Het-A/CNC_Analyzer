# CNC Analyzer

A modular system that analyzes, debugs, optimizes, and explains CNC G-code using simulation and AI.

---

## Overview

This project processes raw G-code and transforms it into a safer and more efficient machining plan by combining rule-based logic with intelligent optimization.

---

## How It Works

### 1. Parser
We convert raw G-code into structured objects (`Command`) using a tokenizer and modal resolver.  
This ensures consistent interpretation of machine instructions.

---

### 2. Simulator
We simulate machine movement by tracking position (X, Y, Z) and generating toolpath segments.  
Each segment represents actual tool motion in space.

---

### 3. Debugger
We apply rule-based checks (safety, collision, anomalies) on toolpath segments.  
Issues like unsafe rapid moves, deep cuts, and boundary violations are detected.

---

### 4. Optimizer
We improve the toolpath using:
- Geometry cleanup (removing redundant moves)
- Collinear merging
- Safe transitions (Z-lift before rapid moves)
- Path reordering (nearest-neighbor approach)
- Feed constraints

---

### 5. Visualizer
Toolpaths are plotted in 2D/3D to help understand motion and highlight issues.

---

### 6. AI Layer
We generate human-readable explanations and suggestions based on detected issues and optimized output.

---

## Pipeline Architecture

The system follows a staged processing pipeline:

Input → Parsing → State Simulation → Rule-Based Analysis → Optimization → Visualization → AI Interpretation

Each stage operates on structured data models, ensuring modularity and scalability.

---

## To Run

```bash
pip install -r requirements.txt
python main.py