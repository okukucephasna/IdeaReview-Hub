import React, { useEffect, useState } from "react";
import axios from "axios";

const Dashboard = () => {
  const [projects, setProjects] = useState([]);
  const [newProject, setNewProject] = useState({ title: "", description: "" });
  const [editingProject, setEditingProject] = useState(null); // project being edited
  const [modalOpen, setModalOpen] = useState(false);

  // Fetch approved projects on load
  const fetchProjects = async () => {
    try {
      const res = await axios.get("http://localhost:5000/api/projects/approved");
      setProjects(res.data);
    } catch (err) {
      console.error("Error fetching projects", err);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  // Add a project
  const handleAddProject = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5000/api/projects", newProject);
      setNewProject({ title: "", description: "" });
      fetchProjects();
    } catch (err) {
      console.error("Error adding project", err);
    }
  };

  // Edit a project
  const handleEditProject = async (e) => {
    e.preventDefault();
    try {
      await axios.put(`http://localhost:5000/api/projects/${editingProject.id}`, editingProject);
      setEditingProject(null);
      setModalOpen(false);
      fetchProjects();
    } catch (err) {
      console.error("Error editing project", err);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">My Approved Projects</h2>

      {/* Project List */}
      <div className="grid gap-4">
        {projects.map((project) => (
          <div
            key={project.id}
            className="p-4 bg-white rounded-lg shadow flex justify-between items-center"
          >
            <div>
              <h3 className="text-lg font-semibold">{project.title}</h3>
              <p className="text-gray-600">{project.description}</p>
            </div>
            <button
              className="bg-blue-500 text-white px-3 py-1 rounded"
              onClick={() => {
                setEditingProject(project);
                setModalOpen(true);
              }}
            >
              Edit
            </button>
          </div>
        ))}
      </div>

      {/* Add Project Form */}
      <form onSubmit={handleAddProject} className="mt-6 p-4 bg-gray-100 rounded-lg">
        <h3 className="text-lg font-semibold mb-2">Post a New Project</h3>
        <input
          type="text"
          placeholder="Project Title"
          value={newProject.title}
          onChange={(e) => setNewProject({ ...newProject, title: e.target.value })}
          className="border p-2 rounded w-full mb-2"
          required
        />
        <textarea
          placeholder="Project Description"
          value={newProject.description}
          onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
          className="border p-2 rounded w-full mb-2"
          required
        ></textarea>
        <button className="bg-green-500 text-white px-4 py-2 rounded">Post Project</button>
      </form>

      {/* Edit Modal */}
      {modalOpen && editingProject && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96">
            <h3 className="text-lg font-semibold mb-4">Edit Project</h3>
            <form onSubmit={handleEditProject}>
              <input
                type="text"
                value={editingProject.title}
                onChange={(e) =>
                  setEditingProject({ ...editingProject, title: e.target.value })
                }
                className="border p-2 rounded w-full mb-2"
                required
              />
              <textarea
                value={editingProject.description}
                onChange={(e) =>
                  setEditingProject({ ...editingProject, description: e.target.value })
                }
                className="border p-2 rounded w-full mb-2"
                required
              ></textarea>
              <div className="flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="bg-gray-400 text-white px-3 py-1 rounded"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-blue-500 text-white px-3 py-1 rounded"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
