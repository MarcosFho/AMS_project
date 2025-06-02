import Header from "../components/Header";
import Footer from "../components/Footer";
import SidebarFazenda from "../components/SidebarFazenda";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Fazendas() {
  const [fazendas, setFazendas] = useState([]);
  const [usuarioId, setUsuarioId] = useState(null);
  const [erro, setErro] = useState("");
  const [busca, setBusca] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    buscarUsuarioLogado();
  }, []);

  useEffect(() => {
    fetchFazendas();
  }, [busca]);

  const buscarUsuarioLogado = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const res = await api.get("/usuarios/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsuarioId(res.data.id);
    } catch (err) {
      console.warn("Usuário não logado ou erro na autenticação.");
    }
  };

  const fetchFazendas = async (tipo_atividade = null) => {
    try {
      const response = await api.get("/fazendas", {
        params: tipo_atividade ? { tipo_atividade } : busca ? { busca } : {},
      });

      const dadosTratados = response.data.map((f) => ({
        ...f,
        usuario_id: f.usuario_id ?? f.id_usuario,
      }));

      setFazendas(dadosTratados);
    } catch (error) {
      setErro("Erro ao carregar fazendas.");
    }
  };

  const handleAnunciarFazenda = () => {
    const token = localStorage.getItem("token");
    navigate(token ? "/cadastrofazendas" : "/login");
  };

  const handleFiltrarAtividade = (atividadeSelecionada) => {
    fetchFazendas(atividadeSelecionada);
  };

  const handleEditar = (id) => {
    navigate(`/editarfazenda/${id}`);
  };

  const handleExcluir = async (id) => {
    const confirmar = window.confirm("Tem certeza que deseja excluir esta fazenda?");
    if (!confirmar) return;

    try {
      await api.delete(`/fazendas/${id}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      setFazendas((prev) => prev.filter((f) => f.id !== id));
      alert("Fazenda excluída com sucesso.");
    } catch (err) {
      console.error("Erro ao excluir fazenda:", err);
      alert("Erro ao excluir a fazenda.");
    }
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
          FAZENDAS OU ÁREAS DISPONÍVEIS
        </h1>
      </section>

      <div className="bg-white py-8 px-4 flex flex-col md:flex-row justify-center items-center gap-4 shadow">
        <input
          type="text"
          placeholder="🔍 Pesquise uma fazenda ou área..."
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
          className="w-full max-w-xl border-2 border-gray-300 rounded-full px-6 py-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 shadow-sm transition"
        />
        <button
          onClick={handleAnunciarFazenda}
          className="bg-green-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-green-700 shadow transition"
        >
          Anuncie sua Área
        </button>
      </div>

      <section className="flex flex-col lg:flex-row gap-6 px-4 py-12 bg-gray-50">
        <SidebarFazenda onFiltrarCategoria={handleFiltrarAtividade} />

        <div className="flex-1 space-y-8">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-green-700 mb-2">
              Lista de Fazendas e Áreas
            </h2>
            {erro && <p className="text-red-600">{erro}</p>}
          </div>

          {fazendas.length === 0 ? (
            <p className="text-center text-gray-500">Nenhuma fazenda ou área encontrada.</p>
          ) : (
            fazendas.map((fazenda) => (
              <div
                key={fazenda.id}
                className="bg-white p-4 rounded shadow hover:shadow-lg transition"
              >
                <h3 className="text-xl font-semibold text-green-800">{fazenda.nome}</h3>

                {fazenda.fotos?.length > 0 ? (
                  <img
                    src={`http://localhost:5000${fazenda.fotos[0].url_foto}`}
                    alt="Foto da fazenda"
                    className="w-full h-48 object-cover rounded mt-2 mb-3"
                  />
                ) : (
                  <div className="text-gray-400 italic mt-2 mb-3">Sem fotos disponíveis</div>
                )}

                <p className="text-gray-700">{fazenda.descricao}</p>
                <p className="text-sm text-gray-500 mt-2">Tipo de Atividade: {fazenda.tipo_atividade}</p>
                <p className="text-sm text-gray-500">Local: {fazenda.localizacao}</p>
                <p className="text-sm text-gray-500">Área Total: {fazenda.area_total} ha</p>
                {fazenda.area_utilizada && (
                  <p className="text-sm text-gray-500">Área Utilizada: {fazenda.area_utilizada} ha</p>
                )}
                <p className="text-sm text-gray-500">
                  Criado em:{" "}
                  {fazenda.data_criacao
                    ? new Date(fazenda.data_criacao).toLocaleDateString("pt-BR")
                    : "—"}
                </p>

                {usuarioId && usuarioId === fazenda.usuario_id && (
                  <div className="flex gap-4 mt-4">
                    <button
                      onClick={() => handleEditar(fazenda.id)}
                      className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                    >
                      Editar
                    </button>
                    <button
                      onClick={() => handleExcluir(fazenda.id)}
                      className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                    >
                      Excluir
                    </button>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </section>

      <Footer />
    </div>
  );
}

export default Fazendas;
