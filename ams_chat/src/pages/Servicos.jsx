import Header from "../components/Header";
import Footer from "../components/Footer";
import SidebarDestaques from "../components/SidebarDestaques";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Servicos() {
  const [servicos, setServicos] = useState([]);
  const [erro, setErro] = useState("");
  const [busca, setBusca] = useState("");
  const [usuarioLogadoId, setUsuarioLogadoId] = useState(null);
  const [categoria, setCategoria] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchServicos = async () => {
      try {
        const params = {};
        if (busca) params.busca = busca;
        if (categoria) params.categoria = categoria;
        const response = await api.get("/servicos", { params });
        setServicos(response.data);
      } catch (error) {
        setErro("Erro ao carregar serviços.");
      }
    };
    fetchServicos();
  }, [busca, categoria]);

  useEffect(() => {
    const fetchUsuarioLogado = async () => {
      try {
        const res = await api.get("/usuarios/me");
        setUsuarioLogadoId(res.data.id);
      } catch (error) {
        console.error("Usuário não autenticado.");
      }
    };
    fetchUsuarioLogado();
  }, []);

  const handleAnunciarServico = () => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/cadastroservico");
    } else {
      navigate("/login");
    }
  };

  const handleEditarServico = (servico) => {
    navigate(`/servicoseditar/${servico.id}`);
  };

  const handleExcluirServico = async (id) => {
    if (window.confirm("Deseja realmente excluir este serviço?")) {
      try {
        await api.delete(`/servicos/${id}`);
        setServicos(servicos.filter((s) => s.id !== id));
      } catch (error) {
        console.error("Erro ao excluir serviço:", error);
        alert("Erro ao excluir o serviço.");
      }
    }
  };

  function getCardImageProps(foto) {
    const src = foto.url_foto.startsWith("/")
      ? `http://localhost:5000${foto.url_foto}`
      : `http://localhost:5000/uploads/servico_fotos/${foto.url_foto}`;
    return {
      src,
      alt: "Foto do serviço",
      width: 180,
      height: 140,
      style: { width: 180, height: 140, objectFit: "cover" },
      className: "rounded mt-2 mb-3"
    };
  }

  // Função para solicitar contato
  const handleEntrarEmContato = async (servico) => {
    try {
      await api.post("/solicitacoes", { id_servico: servico.id });
      navigate(`/chat/${servico.id_usuario}`); // Redireciona para o chat!
    } catch (error) {
      alert("Erro ao enviar solicitação. Tente novamente.");
    }
  };

  const handleFiltrarCategoria = (cat) => {
    setCategoria(cat);
  };

  // UTIL: busca o telefone no local correto do objeto
  function getTelefone(servico) {
    // Adapte para seu backend!
    if (servico.telefone) return servico.telefone;
    if (servico.prestador && servico.prestador.telefone) return servico.prestador.telefone;
    if (servico.usuario && servico.usuario.telefone) return servico.usuario.telefone;
    return "-";
  }

  function getPreco(servico) {
    // Adapte se o nome do campo for diferente no backend
    return servico.preco ? `R$ ${Number(servico.preco).toLocaleString("pt-BR", { minimumFractionDigits: 2 })}` : "Sob consulta";
  }

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
          SERVIÇOS DISPONÍVEIS
        </h1>
      </section>

      <div className="bg-white py-8 px-4 flex flex-col md:flex-row justify-center items-center gap-4 shadow">
        <input
          type="text"
          placeholder="🔍 Pesquise um serviço..."
          value={busca}
          onChange={e => setBusca(e.target.value)}
          className="w-full max-w-xl border-2 border-gray-300 rounded-full px-6 py-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 shadow-sm transition"
        />
        <button
          onClick={handleAnunciarServico}
          className="bg-green-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-green-700 shadow transition"
        >
          Anunciar Serviço
        </button>
      </div>

      <section className="flex flex-col lg:flex-row gap-6 px-4 py-12 bg-gray-50">
        <SidebarDestaques onFiltrarCategoria={handleFiltrarCategoria} />

        <div className="flex-1">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-green-700 mb-2">
              Lista de Serviços
            </h2>
            {erro && <p className="text-red-600">{erro}</p>}
          </div>

          {servicos.length === 0 ? (
            <p className="text-center text-gray-500">Nenhum serviço encontrado.</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              {servicos.map((servico) => (
                <div
                  key={servico.id}
                  className="bg-white p-4 rounded shadow hover:shadow-lg transition"
                >
                  <h3 className="text-xl font-semibold text-green-800">{servico.tipo}</h3>

                  {servico.fotos && servico.fotos.length > 0 ? (
                    <img {...getCardImageProps(servico.fotos[0])} />
                  ) : (
                    <div className="text-gray-400 italic mt-2 mb-3">Sem fotos disponíveis</div>
                  )}

                  <p className="text-gray-700">{servico.descricao}</p>
                  <p className="text-sm text-gray-500 mt-2">Categoria: {servico.categoria}</p>
                  <p className="text-sm text-gray-500">Local: {servico.localizacao}</p>
                  <p className="text-sm text-gray-500">
                    Preço: <span className="font-semibold text-green-900">
                      {servico.preco ? `R$ ${Number(servico.preco).toLocaleString("pt-BR", { minimumFractionDigits: 2 })}` : "-"}
                    </span>
                  </p>
                  <p className="text-sm text-gray-500">
                    Telefone: <span className="font-semibold text-green-900">
                      {servico.telefone || "-"}
                    </span>
                  </p>
                  <p className="text-sm text-gray-500">
                    Criado em: {servico.data_criacao
                      ? new Date(servico.data_criacao).toLocaleDateString("pt-BR")
                      : "—"}
                  </p>


                  {servico.id_usuario === usuarioLogadoId ? (
                    <div className="flex gap-2 mt-4">
                      <button
                        onClick={() => handleEditarServico(servico)}
                        className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
                      >
                        Editar
                      </button>
                      <button
                        onClick={() => handleExcluirServico(servico.id)}
                        className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
                      >
                        Excluir
                      </button>
                    </div>
                  ) : (
                    <div className="flex gap-2 mt-4">
                      <button
                        onClick={() => handleEntrarEmContato(servico)}
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

export default Servicos;
