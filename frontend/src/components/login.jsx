import React, { useState } from "react";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async (e) => { // removi ": React.FormEvent"
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (res.ok) setMessage(data.message);
      else setMessage(data.detail || "Erro no login");
    } catch {
      setMessage("Erro na conexão com a API");
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <div>
        <label>Email:</label><br />
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      </div>
      <div>
        <label>Senha:</label><br />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      </div>
      <button type="submit" style={{ marginTop: "10px" }}>Login</button>
      {message && <p>{message}</p>}
    </form>
  );
}

export default Login;
