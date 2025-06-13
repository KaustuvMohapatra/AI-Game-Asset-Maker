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

---

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Node.js (v18.x or later recommended)
-   Git
-   **A running instance of the backend API service for Assetorium.**

### Backend Requirement

This frontend application is a client only; it **cannot function** without the corresponding backend service running locally. The backend handles all AI model processing.

**Before running `npm run dev`, you must first set up and run the Python backend.**

*(Optional: Add a link to your backend repository here if you have one)*
> Backend Repository: `[Link to your FastAPI/Celery project]`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KaustuvMohapatra/AI-Game-Asset-Maker.git
    ```
2.  **Navigate into the project and then the frontend directory:**
    *All frontend-related commands must be run from the `frontend` folder.*
    ```bash
    cd AI-Game-Asset-Maker/frontend
    ```
3.  **Install NPM packages:**
    ```bash
    npm install
    ```

---

## Running the Application for Development

This project uses `concurrently` to run the Vite development server and the Electron app in parallel, enabling hot-reloading.

**From the `frontend` directory, run:**

```bash
npm run dev


---

## Running the Application for Development

This project uses `concurrently` to run the Vite development server and the Electron app in parallel, enabling hot-reloading.

**From the `frontend` directory, run:**

```bash
npm run dev
```

This command starts both the React development server and the Electron application.

## Building for Production

To create a distributable `.exe` (for Windows) or `.dmg` (for macOS):

1.  **Build the React App:**
    ```bash
    npm run build
    ```
2.  **Package the Electron App:**
    ```bash
    npm run build:electron
    ```
    The final installer (e.g., `Assetorium Setup 0.1.0.exe`) will be located in the `frontend/dist_electron` folder.

---

## Project Structure

A quick overview of the key files in the `frontend` directory:

```
frontend/
├── dist/             # Vite build output (ignored by Git)
├── dist_electron/    # Electron build output (ignored by Git)
├── node_modules/     # Project dependencies (ignored by Git)
├── public/
│   ├── electron.js   # Main Electron process, window creation, IPC handlers
│   └── preload.js    # Secure bridge between Electron and React
├── src/
│   ├── App.css       # Main styles
│   ├── App.tsx       # Main React component, state management, UI
│   └── main.tsx      # React entry point
├── .gitignore        # Specifies files for Git to ignore
├── package.json      # Project metadata, dependencies, and scripts
└── ...
```

## Troubleshooting

-   **App launches but "Generate" fails:** The most common issue is that the backend API service is not running. Make sure you have started your local Python (FastAPI + Celery) server before running the Electron app.
-   **`npm install` fails:** Try deleting the `node_modules` folder and the `package-lock.json` file, then run `npm install` again.


