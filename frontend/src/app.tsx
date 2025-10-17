import React, { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import Reservation from "./components/reservation";

function App() {
  const [showLogin, setShowLogin] = useState(true);

  const path = window.location.pathname;

  if (path === "/reservation") {
    return <Reservation />;
  }

  return (
    <div style={{ maxWidth: "400px", margin: "50px auto", fontFamily: "Arial, sans-serif" }}>
      <h1>Sistema de Reservas</h1>
      <button onClick={() => setShowLogin(true)} style={{ marginRight: "10px" }}>Login</button>
      <button onClick={() => setShowLogin(false)}>Cadastrar</button>
      <hr />
      {showLogin ? <Login /> : <Register />}
    </div>
  );
}

export default App;
