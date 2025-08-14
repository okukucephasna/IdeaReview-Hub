// frontend/src/pages/Home.jsx
import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-md text-center">
        <h1 className="text-3xl font-bold mb-6">Welcome to Idea Hub</h1>
        <p className="text-gray-600 mb-8">
          Share your innovative ideas and collaborate with others.
        </p>
        <div className="space-y-4">
          <Link
            to="/signup"
            className="block bg-blue-500 text-white px-6 py-3 rounded hover:bg-blue-600"
          >
            Get Started
          </Link>
          <Link
            to="/login"
            className="block border border-blue-500 text-blue-500 px-6 py-3 rounded hover:bg-blue-50"
          >
            Already have an account? Sign In
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;
