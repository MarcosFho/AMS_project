import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const token = localStorage.getItem("token");
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate("/login");
    }
  }, [token, navigate]);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold text-green-700 mb-4">Painel do Usuário</h1>
      <p>Bem-vindo! Aqui está seu token de autenticação:</p>
      <pre className="mt-4 p-2 bg-gray-100 border rounded">{token}</pre>
    </div>
  );
}

export default Dashboard;
