import React, { useState, useEffect } from "react";

function Reservation() {
  const [reservations, setReservations] = useState([]);
  const [form, setForm] = useState({
    user_email: "",
    lab_id: "",
    date: "",
    start_time: "",
    end_time: "",
  });
  const [message, setMessage] = useState("");

  // Buscar todas as reservas
  useEffect(() => {
    fetch("http://127.0.0.1:8000/reservations")
      .then((res) => res.json())
      .then((data) => setReservations(data))
      .catch(() => setMessage("Erro ao carregar reservas"));
  }, []);

  // Criar nova reserva
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:8000/reservations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();
      if (res.ok) {
        setMessage(data.message);
        setForm({ user_email: "", lab_id: "", date: "", start_time: "", end_time: "" });
        const updated = await fetch("http://127.0.0.1:8000/reservations").then((r) => r.json());
        setReservations(updated);
      } else {
        setMessage(data.detail || "Erro ao criar reserva");
      }
    } catch {
      setMessage("Erro na conexão com o servidor");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px", fontFamily: "Arial, sans-serif" }}>
      <h1>Sistema de Reservas</h1>

      <form onSubmit={handleSubmit} style={{ display: "inline-block", textAlign: "left" }}>
        <label>Email do usuário:</label><br />
        <input
          type="email"
          value={form.user_email}
          onChange={(e) => setForm({ ...form, user_email: e.target.value })}
          required
        /><br />

        <label>ID do laboratório:</label><br />
        <input
          type="text"
          value={form.lab_id}
          onChange={(e) => setForm({ ...form, lab_id: e.target.value })}
          required
        /><br />

        <label>Data:</label><br />
        <input
          type="date"
          value={form.date}
          onChange={(e) => setForm({ ...form, date: e.target.value })}
          required
        /><br />

        <label>Hora de início:</label><br />
        <input
          type="time"
          value={form.start_time}
          onChange={(e) => setForm({ ...form, start_time: e.target.value })}
          required
        /><br />

        <label>Hora de término:</label><br />
        <input
          type="time"
          value={form.end_time}
          onChange={(e) => setForm({ ...form, end_time: e.target.value })}
          required
        /><br />

        <button type="submit" style={{ marginTop: "10px" }}>Reservar</button>
      </form>

      {message && <p style={{ marginTop: "10px" }}>{message}</p>}

      <h3 style={{ marginTop: "40px" }}>Reservas Existentes</h3>
      {reservations.length > 0 ? (
        <table
          border="1"
          style={{
            margin: "0 auto",
            borderCollapse: "collapse",
            minWidth: "600px",
            backgroundColor: "#f9f9f9",
          }}
        >
          <thead>
            <tr>
              <th>Email</th>
              <th>Lab</th>
              <th>Data</th>
              <th>Início</th>
              <th>Término</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {reservations.map((r) => (
              <tr key={r.id}>
                <td>{r.user_email}</td>
                <td>{r.lab_id}</td>
                <td>{r.date}</td>
                <td>{r.start_time}</td>
                <td>{r.end_time}</td>
                <td>{r.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Nenhuma reserva encontrada.</p>
      )}
    </div>
  );
}

export default Reservation;
