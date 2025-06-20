// frontend/src/App.tsx
// (All imports and type definitions remain the same)
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import bgImage from './assets/bg.jpg';

// --- (No changes needed in this section) ---
declare global {
    interface Window {
        electronAPI: {
            saveImage: (data: { url: string; prompt: string }) => Promise<{ success: boolean; path?: string; error?: string }>;
            launchGame: (configPath: string) => void;
        };
    }
}
interface GameFormData {
    title: string;
    character: string;
    background: string;
    reward: string;
    enemy: string;
    levels: number;
}
interface GameResult {
    title: string;
    characterUrl: string;
    backgroundUrl: string;
    rewardUrl: string;
    enemyUrl: string;
    configPath: string;
}
type JobStatus = 'QUEUED' | 'PENDING' | 'STARTED' | 'SUCCESS' | 'FAILURE';
interface Job {
    id: string;
    status: JobStatus;
    result: GameResult | null;
    formData: GameFormData;
}
const API_URL = 'http://127.0.0.1:8000';
const GamePreviewModal: React.FC<{ result: GameResult; onClose: () => void }> = ({ result, onClose }) => {
    // ... (This component is perfect, no changes needed)
    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="close-button" onClick={onClose}>×</button>
                <h2>{result.title}</h2>
                <div className="preview-grid">
                    <div className="preview-item">
                        <h3>Character</h3>
                        <img src={`${API_URL}/${result.characterUrl}`} alt="Generated Character" />
                    </div>
                    <div className="preview-item">
                        <h3>Enemy</h3>
                        <img src={`${API_URL}/${result.enemyUrl}`} alt="Generated Enemy" />
                    </div>
                    <div className="preview-item">
                        <h3>Reward</h3>
                        <img src={`${API_URL}/${result.rewardUrl}`} alt="Generated Reward" />
                    </div>
                    <div className="preview-item full-width">
                        <h3>Background</h3>
                        <img src={`${API_URL}/${result.backgroundUrl}`} alt="Generated Background" />
                    </div>
                </div>
            </div>
        </div>
    );
};
// --- (End of unchanged section) ---


// ==============================================================================
// Main App Component
// ==============================================================================
function App() {
    // ... (All your state and handlers are perfect, no changes needed here)
    const [formData, setFormData] = useState<GameFormData>({
        title: 'Test Game',
        character: 'Armored Knight with black steel plated armor and short sword in right hand',
        background: 'A castle with stone walls and blue sky with white clouds in background',
        reward: 'Gold coin',
        enemy: 'Zombie in green color and black pant',
        levels: 3,
    });
    const [latestJob, setLatestJob] = useState<Job | null>(null);
    const [isGenerating, setIsGenerating] = useState<boolean>(false);
    const [showPreview, setShowPreview] = useState<boolean>(false);

    useEffect(() => {
        if (!latestJob || latestJob.status === 'SUCCESS' || latestJob.status === 'FAILURE') {
            setIsGenerating(false);
            return;
        }
        const intervalId = setInterval(async () => {
            try {
                const res = await axios.get<{ task_id: string; status: JobStatus; result: any }>(`${API_URL}/status/${latestJob.id}`);
                if (res.data.status === 'SUCCESS' || res.data.status === 'FAILURE') {
                    setLatestJob(prev => prev ? { ...prev, status: res.data.status, result: res.data.result } : null);
                    clearInterval(intervalId);
                }
            } catch (error) {
                console.error(`Error polling job ${latestJob.id}:`, error);
                setLatestJob(prev => prev ? { ...prev, status: 'FAILURE' } : null);
                clearInterval(intervalId);
            }
        }, 3000);
        return () => clearInterval(intervalId);
    }, [latestJob]);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };
    const handleLevelChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData(prev => ({ ...prev, levels: parseInt(e.target.value, 10) }));
    };
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsGenerating(true);
        setShowPreview(false);
        setLatestJob(null);
        try {
            const res = await axios.post<{ task_id: string }>(`${API_URL}/generate-game`, formData);
            setLatestJob({ id: res.data.task_id, status: 'QUEUED', formData, result: null });
        } catch (error) {
            console.error("Error submitting job:", error);
            alert("Failed to submit job. Is the backend server running?");
            setIsGenerating(false);
        }
    };
    const handlePlayGame = () => {
        if (latestJob?.status === 'SUCCESS' && latestJob.result?.configPath) {
            console.log(`Requesting to launch game with config: ${latestJob.result.configPath}`);
            window.electronAPI.launchGame(latestJob.result.configPath);
        } else {
            alert("Error: Game assets are not generated successfully or config path is missing.");
        }
    };


    return (
        <div className="app-container" style={{ backgroundImage: `url(${bgImage})` }}>
            <main className="app-main">
                {/* --- THIS IS THE KEY STRUCTURAL CHANGE --- */}
                {/* We wrap the form and the results in a single container */}
                <div className="content-wrapper">
                    <form onSubmit={handleSubmit} className="game-form-container">
                        <div className="form-header">
                            <h2>Create Your Game</h2>
                        </div>
                        {/* (All form rows are unchanged) */}
                        <div className="form-row">
                            <label htmlFor="title">Title</label>
                            <input type="text" id="title" name="title" value={formData.title} onChange={handleInputChange} className="input-field" placeholder="Enter your game's title" />
                        </div>
                        <div className="form-row">
                            <label htmlFor="character">Character</label>
                            <textarea id="character" name="character" value={formData.character} onChange={handleInputChange} className="input-field" rows={2} placeholder="Main character (e.g., 'ninja cat', 'pixel knight')" />
                        </div>
                        <div className="form-row">
                            <label htmlFor="background">Background</label>
                            <textarea id="background" name="background" value={formData.background} onChange={handleInputChange} className="input-field" rows={2} placeholder="Game background (e.g., 'space station', 'ancient jungle')" />
                        </div>
                        <div className="form-row">
                            <label htmlFor="reward">Reward</label>
                            <input type="text" id="reward" name="reward" value={formData.reward} onChange={handleInputChange} className="input-field" placeholder="The in-game reward (e.g., 'gold coins', 'magic scrolls')" />
                        </div>
                        <div className="form-row">
                            <label htmlFor="enemy">Enemy</label>
                            <input type="text" id="enemy" name="enemy" value={formData.enemy} onChange={handleInputChange} className="input-field" placeholder="Enemy type (e.g., 'robots', 'zombies')" />
                        </div>
                        <div className="form-row">
                            <label htmlFor="levels">Number of Levels</label>
                            <input type="number" id="levels" name="levels" value={formData.levels} onChange={handleLevelChange} className="number-input" min="1" max="100" />
                        </div>

                        <button type="submit" className="generate-button" disabled={isGenerating}>
                            {isGenerating ? 'Generating...' : '✓ Generate Game'}
                        </button>
                    </form>

                    {/* This section is now INSIDE the content-wrapper, so it will be stacked below the form */}
                    {latestJob && (
                        <div className="status-and-actions">
                            <p className={`job-status status-${latestJob.status.toLowerCase()}`}>
                                Status: {latestJob.status}
                            </p>
                            {latestJob.status === 'SUCCESS' && latestJob.result && (
                                <div className="actions-container">
                                    <button className="action-button preview" onClick={() => setShowPreview(true)}>
                                        🖼️ Preview Assets
                                    </button>
                                    <button className="action-button play" onClick={handlePlayGame}>
                                        ▶️ Play Game
                                    </button>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </main>

            {showPreview && latestJob?.result && (
                <GamePreviewModal result={latestJob.result} onClose={() => setShowPreview(false)} />
            )}
        </div>
    );
}

export default App;