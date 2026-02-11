import { useEffect, useState } from "react";
import { getAgents, createAgent, deleteAgent, updateAgent } from "../services/agents";

export default function Agents() {
  const [agents, setAgents] = useState([]);
  const [form, setForm] = useState({ name: "", role: "", salary: "" });
  const [editingId, setEditingId] = useState(null);

  function loadAgents() {
    getAgents().then((res) => setAgents(res.data));
  }

  useEffect(() => {
    loadAgents();
  }, []);

  function handleSubmit(e) {
    e.preventDefault();
    const data = {
        ...form,
        salary: parseFloat(form.salary) || 0
    };

    if (editingId) {
        updateAgent(editingId, data).then(() => {
            setForm({ name: "", role: "", salary: "" });
            setEditingId(null);
            loadAgents();
        });
    } else {
        createAgent(data).then(() => {
            setForm({ name: "", role: "", salary: "" });
            loadAgents();
        });
    }
  }

  function handleEdit(agent) {
      setForm({ name: agent.name, role: agent.role, salary: agent.salary });
      setEditingId(agent.id);
  }

  function handleCancelEdit() {
      setForm({ name: "", role: "", salary: "" });
      setEditingId(null);
  }

  function handleDelete(id) {
    if (confirm("Delete this agent?")) {
      deleteAgent(id).then(loadAgents);
    }
  }

  return (
    <>
      <h2>Agents</h2>

      {/* CREATE / EDIT FORM */}
      <form className="form-inline" onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          id="name"
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />
        <input
          id="role"
          name="role"
          placeholder="Role"
          value={form.role}
          onChange={(e) => setForm({ ...form, role: e.target.value })}
          required
        />
        <input
          id="salary"
          name="salary"
          type="number"
          placeholder="Salary"
          value={form.salary}
          onChange={(e) => setForm({ ...form, salary: e.target.value })}
          required
        />
        <button type="submit">{editingId ? "Update" : "Add"}</button>
        {editingId && (
            <button type="button" onClick={handleCancelEdit} style={{ marginLeft: "10px", backgroundColor: "#6c757d" }}>
                Cancel
            </button>
        )}
      </form>

      {/* LIST */}
      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Role</th>
            <th>Salary</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {agents.map((a) => (
            <tr key={a.id}>
              <td>{a.name}</td>
              <td>{a.role}</td>
              <td>${a.salary?.toLocaleString() || 0}</td>
              <td>
                <button onClick={() => handleEdit(a)} style={{ marginRight: "5px", backgroundColor: "#ffc107", color: "black" }}>
                    Edit
                </button>
                <button className="danger" onClick={() => handleDelete(a.id)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
