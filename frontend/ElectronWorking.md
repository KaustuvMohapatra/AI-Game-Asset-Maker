# Assetorium: AI-Assisted Game Asset Generator

This repository contains the frontend desktop application for **Assetorium**, a tool designed to accelerate game development by leveraging generative AI. The application allows users to generate stylistically consistent 2D game assets, such as icons and seamless textures, directly from text prompts.

This project was built as part of an intensive 1-week sprint, focusing on delivering a functional desktop client using Electron and React.

## Key Features

-   **Desktop Application:** Built with Electron for a native, cross-platform experience.
-   **Modern UI:** A responsive and intuitive user interface built with React, TypeScript, and Vite.
-   **Asynchronous Generation:** Communicates with a Python backend (FastAPI + Celery) to handle long-running AI tasks without freezing the UI.
-   **Asset Generation:** Supports generating both 2D game icons and seamless textures via simple text prompts.
-   **Local History:** Saves your generation history to `localStorage` so you can pick up where you left off.
-   **File System Access:** Allows users to save generated assets directly to their local machine.

## Tech Stack (Frontend)

-   **Framework:** Electron
-   **UI Library:** React 18
-   **Language:** TypeScript
-   **Bundler:** Vite
-   **API Client:** Axios
-   **Build/Packaging:** `electron-builder`

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Node.js (v18.x or later recommended)
-   Git
-   A running instance of the backend API service for Assetorium.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KaustuvMohapatra/AI-Game-Asset-Maker.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd AI-Game-Asset-Maker
    ```

3.  **Navigate to the frontend directory:**
    *All frontend-related commands must be run from this folder.*
    ```bash
    cd frontend
    ```

4.  **Install NPM packages:**
    ```bash
    npm install
    ```

## Running the Application for Development

This project uses `concurrently` to run the Vite development server and the Electron app in parallel, which enables hot-reloading for a smooth development experience.

**From the `frontend` directory, run:**

```bash
npm run dev

