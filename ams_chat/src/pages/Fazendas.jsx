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
  const navigate = useNavigate();

  useEffect(() => {
    const fetchServicos = async () => {
      try {
        const response = await api.get("/servicos", {
          params: busca ? { busca } : {},
        });
        setServicos(response.data);
      } catch (error) {
        setErro("Erro ao carregar serviços.");
      }
    };
    fetchServicos();
  }, [busca]);

  const handleAnunciarServico = () => {
    const token = localStorage.getItem("token");
    if (token) {
      navigate("/servicos/novo");
    } else {
      navigate("/login");
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
          Anuncie sua área
        </button>
      </div>

      <section className="flex flex-col lg:flex-row gap-6 px-4 py-12 bg-gray-50">
        <SidebarDestaques />

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
                <div key={servico.id} className="bg-white p-4 rounded shadow hover:shadow-lg transition">
                  <h3 className="text-xl font-semibold text-green-800">{servico.tipo}</h3>

                  {servico.fotos && servico.fotos.length > 0 ? (
                    <img
                      src={
                        servico.fotos[0].url_foto.startsWith("/")
                          ? `http://localhost:5000${servico.fotos[0].url_foto}`
                          : `http://localhost:5000/uploads/servico_fotos/${servico.fotos[0].url_foto}`
                      }
                      alt="Foto do serviço"
                      width={180}
                      height={140}
                      style={{ width: 180, height: 140, objectFit: 'cover' }}
                      className="rounded mt-2 mb-3"
                    />
                  ) : (
                    <div className="text-gray-400 italic mt-2 mb-3">Sem fotos disponíveis</div>
                  )}

                  <p className="text-gray-700">{servico.descricao}</p>
                  <p className="text-sm text-gray-500 mt-2">Categoria: {servico.categoria}</p>
                  <p className="text-sm text-gray-500">Local: {servico.localizacao}</p>
                  <p className="text-sm text-gray-500">
                    Criado em: {servico.data_criacao
                      ? new Date(servico.data_criacao).toLocaleDateString("pt-BR")
                      : "—"}
                  </p>
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
