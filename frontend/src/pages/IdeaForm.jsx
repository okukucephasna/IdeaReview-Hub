// frontend/src/pages/IdeaForm.jsx
import React, { useState } from "react";

const IdeaForm = ({ onSubmit }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (title.trim() && description.trim()) {
      onSubmit({ title, description });
      setTitle("");
      setDescription("");
    }
  };

  return (
    <div className="bg-white shadow-lg rounded-lg p-6 w-full max-w-lg mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">Submit a New Idea</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Idea Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2"
          required
        />
        <textarea
          placeholder="Describe your idea..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2"
          rows="4"
          required
        ></textarea>
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Submit Idea
        </button>
      </form>
    </div>
  );
};

export default IdeaForm;
