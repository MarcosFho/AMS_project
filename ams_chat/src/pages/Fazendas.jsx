import Header from "../components/Header";
import Footer from "../components/Footer";
import SidebarFazenda from "../components/SidebarFazenda";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Fazendas() {
  const [fazendas, setFazendas] = useState([]);
  const [erro, setErro] = useState("");
  const [busca, setBusca] = useState("");
  const [categoria, setCategoria] = useState("");
  const [usuarioLogadoId, setUsuarioLogadoId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Busca fazendas com filtro de busca/categoria
    const fetchFazendas = async () => {
      try {
        const params = {};
        if (busca) params.busca = busca;
        if (categoria) params.categoria = categoria;
        const response = await api.get("/fazendas", { params });
        setFazendas(response.data);
      } catch (error) {
        setErro("Erro ao carregar fazendas.");
      }
    };
    fetchFazendas();
  }, [busca, categoria]);

  useEffect(() => {
    // Verifica usuário logado
    const fetchUsuarioLogado = async () => {
      try {
        const res = await api.get("/usuarios/me");
        setUsuarioLogadoId(res.data.id);
      } catch {
        // Usuário não autenticado
      }
    };
    fetchUsuarioLogado();
  }, []);

  const handleAnunciarFazenda = () => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/cadastrofazenda");
    } else {
      navigate("/login");
    }
  };

  const handleEditarFazenda = (fazenda) => {
    navigate(`/fazendaeditar/${fazenda.id}`);
  };

  const handleExcluirFazenda = async (id) => {
    if (window.confirm("Deseja realmente excluir esta fazenda?")) {
      try {
        await api.delete(`/fazendas/${id}`);
        setFazendas(fazendas.filter((f) => f.id !== id));
      } catch (error) {
        alert("Erro ao excluir a fazenda.");
      }
    }
  };

  function getCardImageProps(foto) {
    const src = foto.url_foto.startsWith("/")
      ? `http://localhost:5000${foto.url_foto}`
      : `http://localhost:5000/uploads/fazenda_fotos/${foto.url_foto}`;
    return {
      src,
      alt: "Foto da fazenda",
      width: 180,
      height: 140,
      style: { width: 180, height: 140, objectFit: "cover" },
      className: "rounded mt-2 mb-3"
    };
  }

  // ATUALIZADO: Solicitação de contato para fazendas
  const handleEntrarEmContato = async (fazenda) => {
    try {
      // Manda mensagem via API backend (não mais solicitacoes)
      await api.post("/mensagens", {
        id_destinatario: fazenda.id_usuario,
        conteudo: "Olá, tenho interesse nesta fazenda.",
        id_fazenda: fazenda.id // <- agora informando o id_fazenda!
      });
      // Redireciona para o chat com o dono da fazenda
      navigate(`/chat/${fazenda.id_usuario}`);
    } catch (error) {
      alert("Erro ao enviar mensagem. Tente novamente.");
    }
  };

  // Passa o filtro para o Sidebar
  const handleFiltrarCategoria = (cat) => {
    setCategoria(cat);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <section
        className="h-[60vh] bg-cover bg-center relative flex items-center justify-center"
        style={{ backgroundImage: "url('/bg.jpg')" }}
      >
        <div className="absolute top-6 left-6">
          <img src="/logo.png" alt="AMS Logo" className="h-24 drop-shadow-lg" />
        </div>
        <h1 className="text-3xl sm:text-5xl font-bold text-white bg-black/40 px-6 py-3 rounded shadow-lg">
          ÁREAS E FAZENDAS DISPONÍVEIS
        </h1>
      </section>

      <div className="bg-white py-8 px-4 flex flex-col md:flex-row justify-center items-center gap-4 shadow">
        <input
          type="text"
          placeholder="🔍 Pesquise uma fazenda ou área..."
          value={busca}
          onChange={e => setBusca(e.target.value)}
          className="w-full max-w-xl border-2 border-gray-300 rounded-full px-6 py-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 shadow-sm transition"
        />
        <button
          onClick={handleAnunciarFazenda}
          className="bg-green-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-green-700 shadow transition"
        >
          Anuncie sua propriedade
        </button>
      </div>

      <section className="flex flex-col lg:flex-row gap-6 px-4 py-12 bg-gray-50">
        <SidebarFazenda onFiltrarCategoria={handleFiltrarCategoria} />

        <div className="flex-1">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-green-700 mb-2">
              Lista de Fazendas e Áreas
            </h2>
            {erro && <p className="text-red-600">{erro}</p>}
          </div>

          {fazendas.length === 0 ? (
            <p className="text-center text-gray-500">Nenhuma área ou fazenda encontrada.</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              {fazendas.map((fazenda) => (
                <div
                  key={fazenda.id}
                  className="bg-white p-4 rounded shadow hover:shadow-lg transition"
                >
                  <h3 className="text-xl font-semibold text-green-800">{fazenda.nome}</h3>

                  {fazenda.fotos && fazenda.fotos.length > 0 ? (
                    <img {...getCardImageProps(fazenda.fotos[0])} />
                  ) : (
                    <div className="text-gray-400 italic mt-2 mb-3">Sem fotos disponíveis</div>
                  )}

                  <p className="text-gray-700">{fazenda.descricao}</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Área Total: {fazenda.area_total ? `${fazenda.area_total} ha` : "—"}
                  </p>
                  <p className="text-sm text-gray-500">
                    <strong>Telefone:</strong> {fazenda.telefone ? fazenda.telefone : "—"}
                  </p>
                  <p className="text-sm text-gray-500">
                    <strong>Localização:</strong> {fazenda.localizacao ? fazenda.localizacao : "—"}
                  </p>
                  <p className="text-sm text-gray-500">
                    Criado em: {fazenda.data_criacao
                      ? new Date(fazenda.data_criacao).toLocaleDateString("pt-BR")
                      : "—"}
                  </p>

                  {fazenda.id_usuario === usuarioLogadoId ? (
                    <div className="flex gap-2 mt-4">
                      <button
                        onClick={() => handleEditarFazenda(fazenda)}
                        className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
                      >
                        Editar
                      </button>
                      <button
                        onClick={() => handleExcluirFazenda(fazenda.id)}
                        className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
                      >
                        Excluir
                      </button>
                    </div>
                  ) : (
                    <div className="flex gap-2 mt-4">
                      <button
                        onClick={() => handleEntrarEmContato(fazenda)}
                        className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
                      >
                        Entrar em contato
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      <Footer />
    </div>
  );
}

export default Fazendas;
