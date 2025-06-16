// frontend/public/preload.js

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    // Keep the existing 'save-image' functionality
    saveImage: (data) => ipcRenderer.invoke('save-image', data),

    // --- NEW: Expose a function to trigger the game launch ---
    // This sends a one-way message to the main process with the config file path.
    launchGame: (configPath) => ipcRenderer.send('launch-game', configPath),
});