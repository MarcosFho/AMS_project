import Header from "../components/Header";
import Footer from "../components/Footer";
import SidebarDestaques from "../components/SidebarDestaques";
import { useEffect, useState } from "react";
import api from "../services/api";

function Descontos() {
  const [produtos, setProdutos] = useState([]);
  const [erro, setErro] = useState("");

  useEffect(() => {
    const carregarDescontos = async () => {
      try {
        const response = await api.get("/produtos");
        const comDesconto = response.data.filter(p => p.desconto && p.desconto > 0);
        setProdutos(comDesconto);
      } catch (error) {
        setErro("Erro ao carregar descontos.");
      }
    };

    carregarDescontos();
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
          DESCONTOS EXCLUSIVOS PARA O AGRO
        </h1>
      </section>

      {/* Campo de busca */}
      <div className="bg-white py-8 px-4 text-center shadow">
        <input
          type="text"
          placeholder="🔍 Pesquise descontos disponíveis..."
          className="w-full max-w-xl border-2 border-gray-300 rounded-full px-6 py-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 shadow-sm transition"
        />
      </div>

      {/* Conteúdo principal */}
      <section className="flex flex-col lg:flex-row gap-6 px-4 py-12 bg-gray-50">
        <SidebarDestaques />

        <div className="flex-1 text-center space-y-8">
          <h2 className="text-2xl font-bold text-green-700">Produtos com Desconto</h2>
          {erro && <p className="text-red-600">{erro}</p>}

          {produtos.length === 0 ? (
            <p className="text-gray-500">Nenhum desconto disponível no momento.</p>
          ) : (
            produtos.map((produto) => (
              <div
                key={produto.id}
                className="bg-white p-4 rounded shadow max-w-xl mx-auto"
              >
                <h3 className="text-xl font-semibold text-green-800">{produto.nome}</h3>
                <p className="text-gray-700 mt-1">{produto.descricao}</p>
                <p className="mt-2 text-sm text-gray-500">
                  De: <span className="line-through">R$ {produto.preco.toFixed(2)}</span>
                </p>
                <p className="text-lg font-bold text-green-600">
                  Por: R$ {(produto.preco - produto.desconto).toFixed(2)}
                </p>
              </div>
            ))
          )}
        </div>
      </section>

      <Footer />
    </div>
  );
}

export default Descontos;
