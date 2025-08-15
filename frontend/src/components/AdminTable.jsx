import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Button, Modal, Form } from 'react-bootstrap';

const AdminTable = () => {
  const [admins, setAdmins] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState("add"); // add | edit
  const [currentAdmin, setCurrentAdmin] = useState({ id: "", name: "", email: "" });

  const API_URL = "http://localhost:5000/api/admins"; // Change to your Flask API URL

  // Fetch admins
  const fetchAdmins = async () => {
    try {
      const res = await axios.get(API_URL);
      setAdmins(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  // Add or update admin
  const handleSave = async () => {
    try {
      if (modalType === "add") {
        await axios.post(API_URL, currentAdmin);
      } else {
        await axios.put(`${API_URL}/${currentAdmin.id}`, currentAdmin);
      }
      fetchAdmins();
      setShowModal(false);
    } catch (err) {
      console.error(err);
    }
  };

  // Delete admin
  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this admin?")) {
      try {
        await axios.delete(`${API_URL}/${id}`);
        fetchAdmins();
      } catch (err) {
        console.error(err);
      }
    }
  };

  // Open modal for add or edit
  const openModal = (type, admin = { id: "", name: "", email: "" }) => {
    setModalType(type);
    setCurrentAdmin(admin);
    setShowModal(true);
  };

  useEffect(() => {
    fetchAdmins();
  }, []);

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Admin Management</h2>
      <Button variant="success" onClick={() => openModal("add")}>+ Add Admin</Button>

      <Table striped bordered hover responsive className="mt-3 shadow-sm">
        <thead className="table-dark">
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Email</th>
            <th style={{ width: "200px" }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {admins.length > 0 ? (
            admins.map((admin, index) => (
              <tr key={admin.id}>
                <td>{index + 1}</td>
                <td>{admin.name}</td>
                <td>{admin.email}</td>
                <td>
                  <Button
                    variant="primary"
                    size="sm"
                    className="me-2"
                    onClick={() => openModal("edit", admin)}
                  >
                    Edit
                  </Button>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => handleDelete(admin.id)}
                  >
                    Delete
                  </Button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" className="text-center">No admins found</td>
            </tr>
          )}
        </tbody>
      </Table>

      {/* Add/Edit Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>{modalType === "add" ? "Add Admin" : "Edit Admin"}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group controlId="adminName" className="mb-3">
              <Form.Label>Name</Form.Label>
              <Form.Control
                type="text"
                value={currentAdmin.name}
                onChange={(e) => setCurrentAdmin({ ...currentAdmin, name: e.target.value })}
                placeholder="Enter name"
              />
            </Form.Group>
            <Form.Group controlId="adminEmail" className="mb-3">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                value={currentAdmin.email}
                onChange={(e) => setCurrentAdmin({ ...currentAdmin, email: e.target.value })}
                placeholder="Enter email"
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
          <Button variant="success" onClick={handleSave}>Save</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default AdminTable;
