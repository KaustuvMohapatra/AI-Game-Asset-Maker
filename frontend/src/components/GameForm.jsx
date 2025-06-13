import { useState } from 'react';

export default function GameForm({ onSubmit }) {
  const [gameData, setGameData] = useState({
    title: '',
    character: '',
    background: '',
    reward: '',
    num_levels: '3',
    enemy: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setGameData({ ...gameData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(gameData);
  };

  return (
    <form onSubmit={handleSubmit} className="p-6 space-y-4 bg-gradient-to-b from-purple-800 to-black rounded-xl shadow-lg max-w-xl mx-auto mt-12 text-sm">
      <h2 className="text-center text-yellow-300 text-xl font-bold">🎮 Create Your Game</h2>

      {['title', 'character', 'background', 'reward', 'enemy'].map((field) => (
        <div key={field}>
          <label className="block text-pink-300 capitalize mb-1">{field.replace('_', ' ')}</label>
          <input
            type="text"
            name={field}
            value={gameData[field]}
            onChange={handleChange}
            required
            className="w-full p-2 bg-black border border-pink-500 text-white rounded"
          />
        </div>
      ))}

      <div>
        <label className="block text-pink-300 mb-1">Number of Levels</label>
        <input
          type="number"
          name="num_levels"
          value={gameData.num_levels}
          onChange={handleChange}
          className="w-full p-2 bg-black border border-pink-500 text-white rounded"
          min="1"
          max="20"
        />
      </div>

      <button type="submit" className="w-full py-2 px-4 bg-yellow-300 text-black font-bold rounded hover:bg-yellow-400 transition">
        🚀 Generate Game
      </button>
    </form>
  );
}

