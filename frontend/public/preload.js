const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    // We are exposing the 'save-image' functionality to our React app
    saveImage: (data) => ipcRenderer.invoke('save-image', data),
});