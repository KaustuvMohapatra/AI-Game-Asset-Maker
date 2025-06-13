// src/App.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// --- TYPE DEFINITIONS ---
type AssetType = 'icon' | 'texture';
type JobStatus = 'QUEUED' | 'PENDING' | 'STARTED' | 'SUCCESS' | 'FAILURE'; // Added 'STARTED'
interface Job {
    id: string;
    status: JobStatus;
    result: { urls: string[] } | null;
    prompt: string;
    type: AssetType;
}

// --- API CONFIG ---
const API_URL = 'http://127.0.0.1:8000';

// --- COMPONENTS ---

// ImageCard Component: Renders a single generated image or its loading state
const ImageCard: React.FC<{ job: Job }> = ({ job }) => {
    const handleSave = async () => {
        if (job.result?.urls?.[0]) {
            // The backend returns a relative path like 'output/job_id/icon.png'
            // We need to construct the full URL for the download request.
            const fullUrl = `${API_URL}/${job.result.urls[0]}`;

            // Access the 'saveImage' function exposed by preload.js
            const result = await window.electronAPI.saveImage({ url: fullUrl, prompt: job.prompt });

            if (result.success) {
                console.log(`Image saved to ${result.path}`);
                alert(`Image saved successfully!`);
            } else {
                console.error('Save failed:', result.error);
                // Don't alert on user cancellation
                if (result.error !== 'Save cancelled by user.') {
                    alert(`Failed to save image: ${result.error}`);
                }
            }
        }
    };

    return (
        <div className="grid-item">
            <div className="image-wrapper">
                {job.status === 'SUCCESS' && job.result?.urls?.[0] ? (
                    <img src={`${API_URL}/${job.result.urls[0]}`} alt={job.prompt} />
                ) : (
                    <div className="placeholder">
                        <div className="spinner"></div>
                        <p>{job.status}</p>
                    </div>
                )}
            </div>
            <div className="card-footer">
                <p className="image-prompt" title={job.prompt}>{job.prompt}</p>
                {job.status === 'SUCCESS' && (
                    <button onClick={handleSave} className="save-button" title="Save Image">
                        {/* Using a simple save icon SVG */}
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                            <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
                        </svg>
                    </button>
                )}
            </div>
        </div>
    );
};

// Main App Component
function App() {
    const [prompt, setPrompt] = useState<string>('A powerful magic sword, fantasy game icon');
    const [assetType, setAssetType] = useState<AssetType>('icon');
    const [jobs, setJobs] = useState<Job[]>([]);
    const [isGenerating, setIsGenerating] = useState<boolean>(false);

    // Polling effect
    useEffect(() => {
        const activeJobs = jobs.filter(job => job.status !== 'SUCCESS' && job.status !== 'FAILURE');

        if (activeJobs.length === 0) {
            setIsGenerating(false);
            return;
        }

        const intervalId = setInterval(() => {
            activeJobs.forEach(async (job) => {
                try {
                    // Note the task_id in the API response is what we need to match, not job.id
                    const res = await axios.get<{ task_id: string; status: JobStatus; result: any }>(`${API_URL}/status/${job.id}`);
                    setJobs(prevJobs => prevJobs.map(j => (j.id === res.data.task_id ? { ...j, status: res.data.status, result: res.data.result } : j)));
                } catch (error) {
                    console.error(`Error polling job ${job.id}:`, error);
                    // Optional: handle failed jobs
                    setJobs(prevJobs => prevJobs.map(j => (j.id === job.id ? { ...j, status: 'FAILURE'} : j)));
                }
            });
        }, 2500);

        return () => clearInterval(intervalId); // Cleanup function
    }, [jobs]); // Rerun effect if jobs array changes

    // Prompt History Management (Load once on mount)
    useEffect(() => {
        try {
            const savedHistory = localStorage.getItem('promptHistory');
            if (savedHistory) {
                const parsedHistory = JSON.parse(savedHistory);
                // Basic validation
                if (Array.isArray(parsedHistory)) {
                    setJobs(parsedHistory);
                }
            }
        } catch (error) {
            console.error("Failed to load or parse prompt history:", error);
            localStorage.removeItem('promptHistory'); // Clear corrupted data
        }
    }, []); // Empty dependency array means this runs only once on component mount

    // Save history whenever it changes
    useEffect(() => {
        localStorage.setItem('promptHistory', JSON.stringify(jobs));
    }, [jobs]);


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!prompt.trim()) {
            alert("Prompt cannot be empty.");
            return;
        }
        setIsGenerating(true);
        try {
            const res = await axios.post<{ task_id: string }>(`${API_URL}/generate`, { prompt, type: assetType });
            const { task_id } = res.data;
            // Prepend the new job to the top of the list
            setJobs(prevJobs => [{ id: task_id, status: 'QUEUED', result: null, prompt, type: assetType }, ...prevJobs]);
        } catch (error) {
            console.error("Error submitting job:", error);
            alert("Failed to submit job. Is the backend server running?");
            setIsGenerating(false);
        }
    };

    return (
        <div className="app-container">
            <header className="app-header">
                <h1>Aetherium Studio</h1>
            </header>
            <main className="app-main">
                <form onSubmit={handleSubmit} className="prompt-form">
                    {/* ====================================================== */}
                    {/* THIS IS THE PART THAT FIXES THE ERROR                    */}
                    {/* ====================================================== */}
                    <div className="form-group">
                        <label htmlFor="prompt-input">Prompt</label>
                        <textarea
                            id="prompt-input"
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            rows={3}
                            placeholder="e.g., seamless stone texture, 2D, highly detailed"
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="asset-type">Asset Type</label>
                        <select
                            id="asset-type"
                            value={assetType}
                            onChange={(e) => setAssetType(e.target.value as AssetType)}
                        >
                            <option value="icon">Icon</option>
                            <option value="texture">Seamless Texture</option>
                        </select>
                    </div>
                    {/* ====================================================== */}
                    {/* END OF FIX                                             */}
                    {/* ====================================================== */}
                    <button type="submit" disabled={isGenerating}>
                        {isGenerating ? 'Generating...' : 'Generate'}
                    </button>
                </form>
                <div className="gallery-container">
                    <h2>Generation History</h2>
                    <div className="image-grid">
                        {jobs.length > 0 ? (
                            jobs.map(job => <ImageCard key={job.id} job={job} />)
                        ) : (
                            <p className="empty-gallery-message">Your generated assets will appear here.</p>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;