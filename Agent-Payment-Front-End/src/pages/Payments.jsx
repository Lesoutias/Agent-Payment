import { useEffect, useState } from "react";
import { getPayments, createPayment } from "../services/payments";
import { getAgents } from "../services/agents";

export default function Payments() {
  const [payments, setPayments] = useState([]);
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  // Fixed form - includes payment_date
  const [form, setForm] = useState({
    agent_id: "",
    amount: "",
    payment_date: new Date().toISOString().split('T')[0], // Today's date
    status: "pending", // lowercase to match backend
  });

  // Check authentication on load
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("Please login first");
      // Redirect to login after showing error
      setTimeout(() => {
        window.location.href = "/";
      }, 2000);
      return;
    }
    
    loadData();
  }, []);

  async function loadData() {
    try {
      setLoading(true);
      setError("");
      
      // Load payments and agents in parallel
      const [paymentsRes, agentsRes] = await Promise.allSettled([
        getPayments(),
        getAgents()
      ]);

      // Handle payments response
      if (paymentsRes.status === "fulfilled") {
        setPayments(paymentsRes.value.data);
      } else {
        console.error("Failed to load payments:", paymentsRes.reason);
        if (paymentsRes.reason.response?.status === 401) {
          setError("Session expired. Redirecting to login...");
          localStorage.removeItem("token");
          setTimeout(() => window.location.href = "/login", 10000);
        }
      }

      // Handle agents response
      if (agentsRes.status === "fulfilled") {
        setAgents(agentsRes.value.data);
      } else {
        console.error("Failed to load agents:", agentsRes.reason);
      }

    } catch (err) {
      console.error("Error loading data:", err);
      setError("Failed to load data");
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    
    try {
      setError("");
      
      // Prepare data for backend
      const paymentData = {
        ...form,
        amount: parseFloat(form.amount),
        agent_id: parseInt(form.agent_id),
        // payment_date is already in YYYY-MM-DD format
        status: form.status.toLowerCase() // Ensure lowercase
      };
      
      await createPayment(paymentData);
      
      // Reset form
      setForm({
        agent_id: "",
        amount: "",
        payment_date: new Date().toISOString().split('T')[0],
        status: "pending",
      });
      
      // Reload payments
      loadData();
      
    } catch (err) {
      console.error("Error creating payment:", err);
      setError(err.response?.data?.detail || "Failed to create payment");
    }
  }

  // Show loading state
  if (loading) {
    return <div>Loading payments...</div>;
  }

  // Show error state
  if (error) {
    return (
      <div>
        <h2>Payments</h2>
        <div style={{ color: "red", padding: "10px", border: "1px solid red" }}>
          Error: {error}
        </div>
        <button onClick={() => window.location.href = "/login"}>
          Go to Login
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Payments</h2>

      {/* CREATE FORM */}
      <form 
        onSubmit={handleSubmit} 
        style={{ 
          display: "grid", 
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: "10px",
          marginBottom: "20px",
          padding: "20px",
          border: "1px solid #ddd",
          borderRadius: "5px"
        }}
      >
        <div>
          <label htmlFor="agent_id" style={{ display: "block", marginBottom: "5px" }}>
            Agent:
          </label>
          <select
            id="agent_id"
            name="agent_id"
            value={form.agent_id}
            onChange={(e) => setForm({ ...form, agent_id: e.target.value })}
            required
            style={{ width: "100%", padding: "8px" }}
          >
            <option value="">Select Agent</option>
            {agents.map((a) => (
              <option key={a.id} value={a.id}>
                {a.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="amount" style={{ display: "block", marginBottom: "5px" }}>
            Amount:
          </label>
          <input
            id="amount"
            name="amount"
            type="number"
            step="0.01"
            placeholder="Amount"
            value={form.amount}
            onChange={(e) => setForm({ ...form, amount: e.target.value })}
            required
            style={{ width: "100%", padding: "8px" }}
          />
        </div>

        <div>
          <label htmlFor="payment_date" style={{ display: "block", marginBottom: "5px" }}>
            Payment Date:
          </label>
          <input
            id="payment_date"
            name="payment_date"
            type="date"
            value={form.payment_date}
            onChange={(e) => setForm({ ...form, payment_date: e.target.value })}
            required
            style={{ width: "100%", padding: "8px" }}
          />
        </div>

        <div>
          <label htmlFor="status" style={{ display: "block", marginBottom: "5px" }}>
            Status:
          </label>
          <select
            id="status"
            name="status"
            value={form.status}
            onChange={(e) => setForm({ ...form, status: e.target.value })}
            style={{ width: "100%", padding: "8px" }}
          >
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
          </select>
        </div>

        <div style={{ display: "flex", alignItems: "flex-end" }}>
          <button 
            type="submit"
            style={{
              padding: "10px 20px",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer"
            }}
          >
            Add Payment
          </button>
        </div>
      </form>

      {/* PAYMENTS LIST */}
      <div style={{ marginTop: "20px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
          <h3>Payment List ({payments.length})</h3>
          <button 
            onClick={loadData}
            style={{
              padding: "8px 16px",
              backgroundColor: "#6c757d",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer"
            }}
          >
            Refresh
          </button>
        </div>

        {payments.length === 0 ? (
          <div style={{ padding: "20px", textAlign: "center", border: "1px dashed #ddd" }}>
            No payments found
          </div>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ backgroundColor: "#f8f9fa" }}>
                <th style={{ border: "1px solid #dee2e6", padding: "8px" }}>Agent ID</th>
                <th style={{ border: "1px solid #dee2e6", padding: "8px" }}>Amount</th>
                <th style={{ border: "1px solid #dee2e6", padding: "8px" }}>Payment Date</th>
                <th style={{ border: "1px solid #dee2e6", padding: "8px" }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {payments.map((p) => (
                <tr key={p.id}>
                  <td style={{ border: "1px solid #dee2e6", padding: "8px" }}>{p.agent_id}</td>
                  <td style={{ border: "1px solid #dee2e6", padding: "8px" }}>${parseFloat(p.amount).toFixed(2)}</td>
                  <td style={{ border: "1px solid #dee2e6", padding: "8px" }}>{p.payment_date}</td>
                  <td style={{ border: "1px solid #dee2e6", padding: "8px" }}>
                    <span style={{
                      padding: "4px 8px",
                      borderRadius: "4px",
                      backgroundColor: 
                        p.status === "completed" ? "#d4edda" :
                        p.status === "pending" ? "#fff3cd" :
                        "#f8d7da",
                      color: 
                        p.status === "completed" ? "#155724" :
                        p.status === "pending" ? "#856404" :
                        "#721c24"
                    }}>
                      {p.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}