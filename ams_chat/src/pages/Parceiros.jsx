import Header from "../components/Header";
import Footer from "../components/Footer";
import SidebarDestaques from "../components/SidebarDestaques";
import { useEffect, useState } from "react";
import api from "../services/api";

function Parceiros() {
  const [lojas, setLojas] = useState([]);
  const [erro, setErro] = useState("");

  useEffect(() => {
    const carregarLojas = async () => {
      try {
        const response = await api.get("/lojas");
        setLojas(response.data);
      } catch (error) {
        setErro("Erro ao carregar lojas parceiras.");
      }
    };

    carregarLojas();
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      {/* Banner elegante */}
      <section
        className="h-[60vh] bg-cover bg-center relative flex items-center justify-center"
        style={{ backgroundImage: "url('/bg.jpg')" }}
      >
        <div className="absolute top-6 left-6">
          <img src="/logo.png" alt="AMS Logo" className="h-24 drop-shadow-lg" />
        </div>
        <h1 className="text-3xl sm:text-5xl font-bold text-white bg-black/40 px-6 py-3 rounded shadow-lg">
          NOSSOS PARCEIROS
        </h1>
      </section>

      {/* Campo de busca */}
      <div className="bg-white py-8 px-4 text-center shadow">
        <input
          type="text"
          placeholder="🔍 Pesquise por parceiros..."
          className="w-full max-w-xl border-2 border-gray-300 rounded-full px-6 py-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 shadow-sm transition"
        />
      </div>

      {/* Conteúdo principal */}
      <section className="flex flex-col lg:flex-row gap-6 px-4 py-12 bg-gray-50 flex-1">
        <SidebarDestaques />

        <div className="flex-1 space-y-8">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-green-700 mb-2">
              Lojas Parceiras
            </h2>
            {erro && <p className="text-red-600">{erro}</p>}
          </div>

          {lojas.length === 0 ? (
            <p className="text-center text-gray-500">Nenhuma loja encontrada.</p>
          ) : (
            lojas.map((loja) => (
              <div
                key={loja.id}
                className="bg-white p-4 rounded shadow hover:shadow-lg transition"
              >
                <h3 className="text-lg font-semibold text-green-800">{loja.nome}</h3>
                <p className="text-gray-700 mt-1">{loja.descricao || "Sem descrição."}</p>
                <p className="text-sm text-gray-500 mt-1">CNPJ: {loja.cnpj}</p>
              </div>
            ))
          )}
        </div>
      </section>

      <Footer />
    </div>
  );
}

export default Parceiros;
