🎮 AI Game Asset Generator

A comprehensive AI-powered game development system that generates custom 2D game assets using Stable Diffusion and creates playable games using Pygame, with a React + Electron desktop interface and a Dockerized scalable backend.


---

🧠 Overview

This project bridges the gap between AI-generated art and interactive gameplay. It allows users to describe their desired game elements via text prompts, which are then used to generate assets and build a playable game instantly.


---

🧱 Architecture

The system is composed of three key components:

1. Asset Generation Pipeline

Uses Stable Diffusion (with DreamBooth fine-tuning support)

Prompt-based character/background/enemy generation

Configurable art styles: pixel, cartoon, realistic


2. Game Engine

Built with Pygame

Automatically integrates generated assets into a functioning 2D game

Features include:

Player and enemy logic

Background sceneries

Object/reward handling



3. Backend Service

FastAPI handles API requests

Celery manages asynchronous image generation

Optimized for concurrency and scalable deployment



---

🖼️ Frontend (Electron + React)

The UI is built with React, wrapped in Electron for cross-platform desktop compatibility.

ElectronWorking.md documents the packaging and build structure.

Integrates with the backend via REST API

Shows:

Prompt inputs

Generation status

Output previews

Game launch button



Frontend Highlights:

TypeScript + Vite

Organized project structure in /frontend

Electron builder configured for deployment



---

🐳 Docker Support

Docker is used to containerize both backend and worker services.

Docker Features:

Dockerfile for backend FastAPI + Celery app

Supports GPU acceleration for Stable Diffusion

Simplifies deployment with docker-compose



---

🚀 Features

✅ AI-Powered Asset Generation
✅ Fine-tuned DreamBooth Support
✅ Instant Game Generation with Pygame
✅ Multiple Art Styles (Cartoon, Realistic, Pixel)
✅ React + Electron Frontend
✅ FastAPI + Celery Backend
✅ Dockerized Services
✅ Scalable & Modular Design


---

📁 Directory Structure

/assets/                  ← Generated asset output
/config/                  ← Configuration files
/engine/                  ← Pygame-based game engine
/generator/               ← Stable Diffusion asset generator
/output_model/            ← Custom fine-tuned models (DreamBooth, etc.)
/frontend/                ← React + Electron frontend
    /src/
    ElectronWorking.md
api.py                    ← FastAPI entry point
worker.py                 ← Celery task manager
generate_assets.py        ← Prompt-to-image generator
run_game.py               ← Game runner using generated assets
background.py, creatures.py ← Asset class logic
...


---

⚙️ Usage

1. Clone the Repo

git clone https://github.com/KaustuvMohapatra/AI-Game-Asset-Maker.git
cd AI-Game-Asset-Maker

2. Backend Setup

Make sure you have Python 3.10+, torch, and other dependencies. Then run:

pip install -r requirements.txt
uvicorn api:app --reload
celery -A worker worker --loglevel=info

3. Frontend Setup

cd frontend
npm install
npm run dev          # For development
npm run electron:build  # To build desktop app

4. Docker (optional for deployment)

docker build -t ai-game-backend .
docker-compose up


---

🧪 Example Flow

1. User enters prompt: "A pixel knight with a red cape"


2. Backend generates image via Stable Diffusion


3. Asset saved to /assets/characters/


4. Game is assembled and run using run_game.py


5. User plays the generated game




---

📌 Future Enhancements

Online multiplayer game mode

Asset customization tools (spritesheet editor)

Training new style-specific models (e.g. anime, voxel)

Enhanced level editor in Electron GUI



---

🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first. Contributions in AI tuning, game logic, or UI design are all appreciated.


---

📄 License

MIT License © 2025 Kaustuv Mohapatra


---
