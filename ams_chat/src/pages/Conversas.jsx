import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Header from "../components/Header";
import Footer from "../components/Footer";

function Conversas() {
  const [conversas, setConversas] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchConversas() {
      setCarregando(true);
      try {
        // Você precisa criar essa rota no backend! Veja instrução abaixo.
        const res = await api.get("/conversas");
        setConversas(res.data);
      } catch (e) {
        setErro("Erro ao buscar conversas.");
      }
      setCarregando(false);
    }
    fetchConversas();
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-1 max-w-2xl mx-auto p-4 bg-white shadow rounded my-8">
        <h1 className="text-2xl font-bold text-green-700 mb-6">Minhas Conversas</h1>
        {carregando ? (
          <div className="text-center text-gray-500">Carregando...</div>
        ) : erro ? (
          <div className="text-center text-red-600">{erro}</div>
        ) : conversas.length === 0 ? (
          <div className="text-center text-gray-500">Nenhuma conversa encontrada.</div>
        ) : (
          <ul>
            {conversas.map((c) => {
              const outro = c.outro_usuario;
              return (
                <li
                  key={c.id}
                  onClick={() => navigate(`/chat/${outro.id}`)}
                  className="flex items-center gap-3 border-b py-3 cursor-pointer hover:bg-green-50 rounded transition"
                >
                  {outro.foto_url ? (
                    <img
                      src={outro.foto_url.startsWith("/")
                        ? `http://localhost:5000${outro.foto_url}`
                        : outro.foto_url}
                      alt={outro.nome}
                      className="w-12 h-12 rounded-full border object-cover"
                    />
                  ) : (
                    <div className="w-12 h-12 rounded-full bg-gray-300 flex items-center justify-center text-2xl text-white">
                      <span>{outro.nome?.charAt(0) || "U"}</span>
                    </div>
                  )}
                  <div className="flex-1">
                    <div className="font-bold text-green-900">{outro.nome || outro.telefone || "Usuário"}</div>
                    <div className="text-gray-600 text-sm truncate">{c.ultima_mensagem || <i>Sem mensagens ainda</i>}</div>
                  </div>
                  <div className="text-xs text-gray-400">
                    {c.data_ultima_mensagem &&
                      new Date(c.data_ultima_mensagem).toLocaleDateString("pt-BR")}
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </main>
      <Footer />
    </div>
  );
}

export default Conversas;
