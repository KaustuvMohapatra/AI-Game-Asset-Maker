// frontend/electron.js

const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const http = require('http');
const { spawn } = require('child_process'); // <-- ADD THIS

function createWindow() {
    // Create the browser window.
    const mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            // preload.js is crucial for secure communication between Electron and React
            preload: path.join(__dirname, 'preload.js'),
            // For security, contextIsolation should be true (the default)
            contextIsolation: true, 
        },
    });

    // Load the React app. In development, we load from the Vite server.
    // In production, we load the static index.html file.
    const startUrl = process.env.ELECTRON_START_URL || `file://${path.join(__dirname, '../dist/index.html')}`;
    mainWindow.loadURL(startUrl);

    // Open the DevTools automatically in development.
    if (!app.isPackaged) {
        mainWindow.webContents.openDevTools();
    }
}

// --- IPC HANDLERS (How React talks to Electron) ---

// This handler listens for a 'save-image' message from the React frontend.
ipcMain.handle('save-image', async (event, { url, prompt }) => {
    const defaultFileName = prompt.replace(/[^a-z0-9]/gi, '_').toLowerCase() + '.png';
    const { filePath } = await dialog.showSaveDialog({
        title: 'Save Generated Image',
        defaultPath: defaultFileName,
        filters: [{ name: 'Images', extensions: ['png'] }]
    });

    if (filePath) {
        // The URL is from our backend, e.g., 'http://127.0.0.1:8000/output/...'
        // We need to download this file and save it to the chosen path.
        return new Promise((resolve, reject) => {
            const file = fs.createWriteStream(filePath);
            http.get(url, (response) => {
                response.pipe(file);
                file.on('finish', () => {
                    file.close(() => resolve({ success: true, path: filePath }));
                });
            }).on('error', (err) => {
                fs.unlink(filePath, () => {}); // Delete the file if download fails
                reject({ success: false, error: err.message });
            });
        });
    }
    return { success: false, error: 'Save cancelled by user.' };
});


// --- NEW: IPC HANDLER FOR LAUNCHING THE GAME ---
ipcMain.on('launch-game', (event, configPath) => {
  console.log('Received launch-game event for config:', configPath);

  // Construct the absolute path to the backend directory and the python script
  // It's robustly defined from this file's location.
  const backendPath = path.join(app.getAppPath(), '..', 'backend');
  const gameScriptPath = path.join(backendPath, 'run_game.py');

  console.log(`Attempting to run script: ${gameScriptPath}`);
  console.log(`Working directory: ${backendPath}`);
  console.log(`With config: ${configPath}`);


  // Use 'spawn' to run the python script as a separate process.
  // We pass the config file path as a command-line argument.
  const pythonProcess = spawn('python', [gameScriptPath, configPath], {
    cwd: backendPath, // Set the 'current working directory' to the backend folder
    stdio: 'inherit'  // Pipe python's console output (print statements, errors) to Electron's console
  });

  pythonProcess.on('close', (code) => {
    console.log(`Pygame process exited with code ${code}`);
  });

  pythonProcess.on('error', (err) => {
    // This will be called if the process could not be spawned, e.g., 'python' not in PATH
    console.error('Failed to start Pygame process:', err);
    dialog.showErrorBox('Execution Error', `Failed to start the game engine. Make sure Python is installed and configured in your system's PATH.\n\nError: ${err.message}`);
  });
});


// --- APP LIFECYCLE ---

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});