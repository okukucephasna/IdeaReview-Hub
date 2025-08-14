import React, { useState, useEffect } from "react";
import axios from "axios";
import { Modal, Button } from "react-bootstrap"; // Bootstrap for modals & buttons

const AdminTable = () => {
  const [users, setUsers] = useState([]);
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);

  const [showUserModal, setShowUserModal] = useState(false);
  const [showNoteModal, setShowNoteModal] = useState(false);

  const [editUser, setEditUser] = useState(null);
  const [editNote, setEditNote] = useState(null);

  const [formData, setFormData] = useState({ name: "", email: "" });
  const [noteData, setNoteData] = useState({ title: "", content: "" });

  // Fetch data
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const usersRes = await axios.get("/api/admin/users");
      const notesRes = await axios.get("/api/admin/notes");
      setUsers(usersRes.data);
      setNotes(notesRes.data);
    } catch (err) {
      console.error("Error fetching data", err);
    } finally {
      setLoading(false);
    }
  };

  // Open User Modal
  const openUserModal = (user = null) => {
    setEditUser(user);
    setFormData(user || { name: "", email: "" });
    setShowUserModal(true);
  };

  // Open Note Modal
  const openNoteModal = (note = null) => {
    setEditNote(note);
    setNoteData(note || { title: "", content: "" });
    setShowNoteModal(true);
  };

  // Save user
  const saveUser = async () => {
    try {
      if (editUser) {
        await axios.put(`/api/admin/users/${editUser.id}`, formData);
      } else {
        await axios.post("/api/admin/users", formData);
      }
      fetchData();
      setShowUserModal(false);
    } catch (err) {
      console.error("Error saving user", err);
    }
  };

  // Save note
  const saveNote = async () => {
    try {
      if (editNote) {
        await axios.put(`/api/admin/notes/${editNote.id}`, noteData);
      } else {
        await axios.post("/api/admin/notes", noteData);
      }
      fetchData();
      setShowNoteModal(false);
    } catch (err) {
      console.error("Error saving note", err);
    }
  };

  // Delete
  const deleteItem = async (type, id) => {
    try {
      await axios.delete(`/api/admin/${type}/${id}`);
      fetchData();
    } catch (err) {
      console.error(`Error deleting ${type}`, err);
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div className="p-4">
      <h2 className="mb-3">Admin Dashboard</h2>

      {/* Users Table */}
      <h4>Manage Users</h4>
      <Button variant="success" className="mb-2" onClick={() => openUserModal()}>+ Add User</Button>
      <table className="table table-bordered">
        <thead>
          <tr><th>Name</th><th>Email</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>
                <Button size="sm" onClick={() => openUserModal(user)}>Edit</Button>{" "}
                <Button size="sm" variant="danger" onClick={() => deleteItem("users", user.id)}>Delete</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Notes Table */}
      <h4 className="mt-4">Manage Notes</h4>
      <Button variant="success" className="mb-2" onClick={() => openNoteModal()}>+ Add Note</Button>
      <table className="table table-bordered">
        <thead>
          <tr><th>Title</th><th>Content</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {notes.map(note => (
            <tr key={note.id}>
              <td>{note.title}</td>
              <td>{note.content}</td>
              <td>
                <Button size="sm" onClick={() => openNoteModal(note)}>Edit</Button>{" "}
                <Button size="sm" variant="danger" onClick={() => deleteItem("notes", note.id)}>Delete</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* User Modal */}
      <Modal show={showUserModal} onHide={() => setShowUserModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>{editUser ? "Edit User" : "Add User"}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <input className="form-control mb-2" placeholder="Name" value={formData.name}
            onChange={e => setFormData({ ...formData, name: e.target.value })}/>
          <input className="form-control" placeholder="Email" value={formData.email}
            onChange={e => setFormData({ ...formData, email: e.target.value })}/>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={() => setShowUserModal(false)}>Cancel</Button>
          <Button variant="primary" onClick={saveUser}>Save</Button>
        </Modal.Footer>
      </Modal>

      {/* Note Modal */}
      <Modal show={showNoteModal} onHide={() => setShowNoteModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>{editNote ? "Edit Note" : "Add Note"}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <input className="form-control mb-2" placeholder="Title" value={noteData.title}
            onChange={e => setNoteData({ ...noteData, title: e.target.value })}/>
          <textarea className="form-control" placeholder="Content" value={noteData.content}
            onChange={e => setNoteData({ ...noteData, content: e.target.value })}/>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={() => setShowNoteModal(false)}>Cancel</Button>
          <Button variant="primary" onClick={saveNote}>Save</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default AdminTable;
