/// <reference types="vite/client" />

// Add this to declare the electronAPI on the window object
export interface IElectronAPI {
    saveImage: (data: {url: string, prompt: string}) => Promise<{success: boolean, path?: string, error?: string}>;
}

declare global {
    interface Window {
        electronAPI: IElectronAPI
    }
}