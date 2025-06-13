import { useState } from 'react';
import GameForm from '../../../ai_game_generator/frontend/src/components/GameForm';

function App() {
  const [gameData, setGameData] = useState(null);

  const handleGameSubmit = (data) => {
    setGameData(data);
    console.log("📝 Game Prompt JSON:", JSON.stringify(data, null, 2));
  };

  return (
    <div className="min-h-screen text-white p-4">
      <GameForm onSubmit={handleGameSubmit} />

      {gameData && (
        <div className="mt-10 max-w-xl mx-auto bg-black bg-opacity-80 p-6 rounded-xl text-sm border border-yellow-300">
          <h3 className="text-yellow-300 text-lg font-bold mb-4">🎮 Game Preview</h3>
          <p><strong>Title:</strong> {gameData.title}</p>
          <p><strong>Main Character:</strong> {gameData.character}</p>
          <p><strong>Background:</strong> {gameData.background}</p>
          <p><strong>Reward:</strong> {gameData.reward}</p>
          <p><strong>Levels:</strong> {gameData.num_levels}</p>
          <p><strong>Enemy Type:</strong> {gameData.enemy}</p>
          <p className="mt-4 italic text-pink-300">🕹️ (Playable game preview coming soon!)</p>
        </div>
      )}
    </div>
  );
}

export default App;

