const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const http = require('http');

function createWindow() {
    // Create the browser window.
    const mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            // preload.js is crucial for secure communication between Electron and React
            preload: path.join(__dirname, 'preload.js'),
            // For security, contextIsolation should be true (the default)
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