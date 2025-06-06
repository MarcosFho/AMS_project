import { useEffect, useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";
import Header from "../components/Header";
import Footer from "../components/Footer";

function Chat() {
  const { idDestinatario } = useParams();
  const [mensagens, setMensagens] = useState([]);
  const [novaMensagem, setNovaMensagem] = useState("");
  const [usuarioLogado, setUsuarioLogado] = useState({});
  const [destinatario, setDestinatario] = useState({});
  const [carregando, setCarregando] = useState(true);
  const mensagensEndRef = useRef(null);
  const navigate = useNavigate();

  // Buscar info do usuário logado
  useEffect(() => {
    api.get("/usuarios/me")
      .then(res => setUsuarioLogado(res.data))
      .catch(() => {});
  }, []);

  // Buscar info do destinatário
  useEffect(() => {
    if (!idDestinatario) return;
    api.get(`/usuarios/${idDestinatario}`)
      .then(res => setDestinatario(res.data))
      .catch(() => setDestinatario({}));
  }, [idDestinatario]);

  // Buscar mensagens
  useEffect(() => {
    if (!idDestinatario) return;
    async function fetchMensagens() {
      setCarregando(true);
      try {
        const res = await api.get(`/mensagens/${idDestinatario}`);
        setMensagens(res.data);
        setTimeout(() => mensagensEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
      } catch {
        setMensagens([]);
      }
      setCarregando(false);
    }
    fetchMensagens();
    const interval = setInterval(fetchMensagens, 3500);
    return () => clearInterval(interval);
  }, [idDestinatario]);

  async function handleEnviarMensagem(e) {
    e.preventDefault();
    if (!novaMensagem.trim()) return;
    try {
      await api.post("/mensagens", {
        id_destinatario: Number(idDestinatario),
        conteudo: novaMensagem
      });
      setNovaMensagem("");
      const res = await api.get(`/mensagens/${idDestinatario}`);
      setMensagens(res.data);
      setTimeout(() => mensagensEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
    } catch (e) {
      alert("Erro ao enviar mensagem");
    }
  }

  // Helper para mostrar nome ou telefone se não tiver nome
  const nomeDestinatario = destinatario.nome || destinatario.telefone || "Destinatário";

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-1 max-w-2xl mx-auto p-4 bg-white shadow rounded my-8">
        <div className="flex items-center gap-3 mb-4 border-b pb-2">
          {destinatario.foto_url ? (
            <img
              src={destinatario.foto_url.startsWith("/")
                ? `http://localhost:5000${destinatario.foto_url}`
                : destinatario.foto_url}
              alt={nomeDestinatario}
              className="w-12 h-12 rounded-full border object-cover"
            />
          ) : (
            <div className="w-12 h-12 rounded-full bg-gray-300 flex items-center justify-center text-2xl text-white">
              <span>{nomeDestinatario.charAt(0)}</span>
            </div>
          )}
          <div>
            <div className="font-bold text-green-800 text-lg">{nomeDestinatario}</div>
            {destinatario.telefone && (
              <div className="text-sm text-gray-500">Tel: {destinatario.telefone}</div>
            )}
          </div>
          <button
            className="ml-auto text-green-600 underline"
            onClick={() => navigate(-1)}
          >Voltar</button>
        </div>
        <div className="h-96 overflow-y-auto border rounded p-3 bg-gray-50 mb-4">
          {carregando ? (
            <div className="text-gray-400 text-center">Carregando mensagens...</div>
          ) : mensagens.length === 0 ? (
            <div className="text-gray-500 text-center">Nenhuma mensagem ainda.</div>
          ) : (
            mensagens.map(msg => (
              <div
                key={msg.id}
                className={`mb-2 flex ${msg.id_remetente === usuarioLogado.id ? "justify-end" : "justify-start"}`}
              >
                <div className={`max-w-xs p-2 rounded ${msg.id_remetente === usuarioLogado.id ? "bg-green-200" : "bg-gray-200"}`}>
                  <span className="block text-sm">{msg.conteudo}</span>
                  <span className="block text-xs text-gray-600">{new Date(msg.data_envio).toLocaleString("pt-BR")}</span>
                </div>
              </div>
            ))
          )}
          <div ref={mensagensEndRef} />
        </div>
        <form onSubmit={handleEnviarMensagem} className="flex gap-2">
          <input
            type="text"
            value={novaMensagem}
            onChange={e => setNovaMensagem(e.target.value)}
            placeholder="Digite sua mensagem..."
            className="flex-1 border rounded px-3 py-2"
            autoFocus
          />
          <button
            type="submit"
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Enviar
          </button>
        </form>
      </main>
      <Footer />
    </div>
  );
}

export default Chat;
