import { useEffect, useState } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import api from "../services/api";

function MensagemFaleConosco() {
  const [mensagens, setMensagens] = useState([]);
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchMensagens() {
      setLoading(true);
      try {
        // Se precisar autenticação, descomente as linhas abaixo:
        // const token = localStorage.getItem("token");
        // const res = await api.get("/fale-conosco", {
        //   headers: { Authorization: `Bearer ${token}` }
        // });
        const res = await api.get("/fale-conosco");
        setMensagens(res.data);
      } catch (e) {
        setErro("Erro ao buscar mensagens.");
      } finally {
        setLoading(false);
      }
    }
    fetchMensagens();
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex flex-col items-center bg-gray-100 py-10 px-4 flex-1">
        <div className="bg-white rounded-xl shadow-md p-8 w-full max-w-3xl">
          <h2 className="text-2xl font-bold text-green-800 mb-4">Mensagens Recebidas</h2>
          {erro && <p className="text-red-500">{erro}</p>}
          {loading ? (
            <div className="text-center text-gray-400">Carregando...</div>
          ) : (
            <div className="space-y-4">
              {mensagens.length === 0 ? (
                <p className="text-gray-500 italic">Nenhuma mensagem recebida ainda.</p>
              ) : (
                mensagens.map((msg, idx) => (
                  <div
                    key={msg.id || msg._id || idx}
                    className="border rounded p-4 bg-green-50 shadow flex flex-col"
                  >
                    <div>
                      <strong>Nome:</strong> {msg.nome} <br />
                      <strong>Email:</strong> {msg.email} <br />
                      <strong>Telefone:</strong> {msg.telefone || "-"} <br />
                      <strong>Assunto:</strong> {msg.assunto || <span className="italic text-gray-400">Sem assunto</span>} <br />
                      <strong>Mensagem:</strong>
                      <div className="bg-white rounded p-2 mt-1">{msg.mensagem}</div>
                      <span className="block text-xs text-gray-500 mt-2">
                        {msg.data_criacao
                          ? new Date(msg.data_criacao).toLocaleString("pt-BR")
                          : ""}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default MensagemFaleConosco;
