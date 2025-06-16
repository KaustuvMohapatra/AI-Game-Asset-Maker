// src/App.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import bgImage from './assets/bg.jpg';

// --- TYPE DEFINITIONS ---
// Represents the data sent to the backend to generate a game
interface GameFormData {
    title: string;
    character: string;
    background: string;
    reward: string;
    enemy: string;
    levels: number;
}

// Represents the structure of the results for a single generated game
interface GameResult {
    title: string;
    characterUrl: string;
    backgroundUrl: string;
    rewardUrl: string;
    enemyUrl: string;
}

// Represents the state of a generation job
type JobStatus = 'QUEUED' | 'PENDING' | 'STARTED' | 'SUCCESS' | 'FAILURE';
interface Job {
    id: string;
    status: JobStatus;
    // The result will now be a GameResult object when successful
    result: GameResult | null;
    formData: GameFormData;
}

const API_URL = 'http://127.0.0.1:8000';

// ==============================================================================
// Game Preview Modal Component
// ==============================================================================
const GamePreviewModal: React.FC<{ result: GameResult; onClose: () => void }> = ({ result, onClose }) => {
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

// ==============================================================================
// Main App Component
// ==============================================================================
function App() {
    const [formData, setFormData] = useState<GameFormData>({
        title: 'Pixel Quest',
        character: 'A brave knight with a glowing sword, pixel art',
        background: 'An enchanted forest with luminous mushrooms, pixel art',
        reward: 'A golden chalice, pixel art game icon',
        enemy: 'A slime monster, pixel art',
        levels: 5,
    });

    const [latestJob, setLatestJob] = useState<Job | null>(null);
    const [isGenerating, setIsGenerating] = useState<boolean>(false);
    const [showPreview, setShowPreview] = useState<boolean>(false);

    // Effect for polling the latest job status
    useEffect(() => {
        if (!latestJob || latestJob.status === 'SUCCESS' || latestJob.status === 'FAILURE') {
            setIsGenerating(false);
            if (latestJob?.status === 'SUCCESS' && latestJob.result) {
                setShowPreview(true);
            }
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
        try {
            // NOTE: Your backend will need an endpoint like '/generate-game'
            // that accepts the new GameFormData structure.
            const res = await axios.post<{ task_id: string }>(`${API_URL}/generate-game`, formData);
            setLatestJob({ id: res.data.task_id, status: 'QUEUED', formData, result: null });
        } catch (error) {
            console.error("Error submitting job:", error);
            alert("Failed to submit job. Is the backend server running?");
            setIsGenerating(false);
        }
    };

    return (
        <div className="app-container" style={{ backgroundImage: `url(${bgImage})` }}>
            <main className="app-main">
                <form onSubmit={handleSubmit} className="game-form-container">
                    <div className="form-header">
                        <h2>Create Your Game</h2>
                    </div>

                    <div className="form-row">
                        <label htmlFor="title">Title</label>
                        <input type="text" id="title" name="title" value={formData.title} onChange={handleInputChange} className="input-field" />
                    </div>
                    <div className="form-row">
                        <label htmlFor="character">Character</label>
                        <textarea id="character" name="character" value={formData.character} onChange={handleInputChange} className="input-field" rows={2} />
                    </div>
                    <div className="form-row">
                        <label htmlFor="background">Background</label>
                        <textarea id="background" name="background" value={formData.background} onChange={handleInputChange} className="input-field" rows={2} />
                    </div>
                    <div className="form-row">
                        <label htmlFor="reward">Reward</label>
                        <input type="text" id="reward" name="reward" value={formData.reward} onChange={handleInputChange} className="input-field" />
                    </div>
                    <div className="form-row">
                        <label htmlFor="enemy">Enemy</label>
                        <input type="text" id="enemy" name="enemy" value={formData.enemy} onChange={handleInputChange} className="input-field" />
                    </div>
                    <div className="form-row">
                        <label htmlFor="levels">Number of Levels</label>
                        <input type="number" id="levels" name="levels" value={formData.levels} onChange={handleLevelChange} className="number-input" min="1" max="100" />
                    </div>

                    <button type="submit" className="generate-button" disabled={isGenerating}>
                        {isGenerating ? 'Generating...' : '✓ Generate Game'}
                    </button>
                </form>
            </main>

            {showPreview && latestJob?.result && (
                <GamePreviewModal result={latestJob.result} onClose={() => setShowPreview(false)} />
            )}
        </div>
    );
}

export default App;