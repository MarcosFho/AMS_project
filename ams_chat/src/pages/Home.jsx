import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import api from "../services/api";

function Home() {
  const navigate = useNavigate();
  const [prestadores, setPrestadores] = useState([]);
  const [servicos, setServicos] = useState([]);
  const [fazendas, setFazendas] = useState([]);
  const [erro, setErro] = useState("");

  const scrollRefPrestadores = useRef(null);
  const scrollRefServicos = useRef(null);
  const scrollRefFazendas = useRef(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const [resPrestadores, resServicos, resFazendas] = await Promise.all([
          api.get("/prestadores"),
          api.get("/servicos"),
          api.get("/fazendas"),
        ]);
        setPrestadores(resPrestadores.data);
        setServicos(resServicos.data);
        setFazendas(resFazendas.data);
      } catch (error) {
        setErro("Erro ao buscar dados do servidor. Tente novamente mais tarde.");
        console.error("Erro ao buscar dados:", error);
      }
    }

    fetchData();
  }, []);

  const scrollLeft = (ref) => {
    if (ref.current) ref.current.scrollBy({ left: -300, behavior: "smooth" });
  };
  const scrollRight = (ref) => {
    if (ref.current) ref.current.scrollBy({ left: 300, behavior: "smooth" });
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      {/* Banner */}
      <section
        className="h-[60vh] bg-cover bg-center relative flex items-center justify-center"
        style={{ backgroundImage: "url('/bg.jpg')" }}
      >
        <div className="absolute top-6 left-6">
          <img src="/logo.png" alt="AMS Logo" className="h-24 drop-shadow-lg" />
        </div>
        <h1 className="text-3xl sm:text-5xl font-bold text-white bg-black/40 px-6 py-3 rounded shadow-lg">
          O SERVIÇO DO AGRO MAIS PERTO DE VOCÊ
        </h1>
      </section>

      {/* Busca */}
      <div className="bg-white py-8 px-4 text-center shadow">
        <input
          type="text"
          placeholder="🔍 Pesquise a prestação de serviço..."
          className="w-full max-w-xl border-2 border-gray-300 rounded-full px-6 py-3 text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 shadow-sm transition"
        />
      </div>

      {erro && <p className="text-center text-red-600 mt-4">{erro}</p>}

      {/* Como Funciona */}
      <section className="py-12 bg-green-50 text-center">
        <h2 className="text-2xl font-bold text-green-700 mb-8">Como Funciona</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-5xl mx-auto px-4">
          <div className="p-6 bg-white rounded-lg shadow">
            <div className="text-4xl">👨🏼‍🌾</div>
            <h3 className="mt-4 font-semibold text-lg">Cadastre-se</h3>
            <p className="text-sm text-gray-600">Crie seu perfil como produtor ou prestador de serviços.</p>
          </div>
          <div className="p-6 bg-white rounded-lg shadow">
            <div className="text-4xl">📢</div>
            <h3 className="mt-4 font-semibold text-lg">Anuncie</h3>
            <p className="text-sm text-gray-600">Publique seus serviços ou fazendas disponíveis.</p>
          </div>
          <div className="p-6 bg-white rounded-lg shadow">
            <div className="text-4xl">🫱🏻‍🫲🏻</div>
            <h3 className="mt-4 font-semibold text-lg">Conecte-se</h3>
            <p className="text-sm text-gray-600">Encontre clientes e feche negócios de forma direta.</p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-12 bg-green-100 text-center">
        <h2 className="text-2xl font-bold text-green-800">Tem um serviço ou fazenda para oferecer?</h2>
        <p className="mt-2 text-gray-700">Cadastre-se agora e comece a faturar com o AMS!</p>
        <button
          onClick={() => navigate("/cadastro")}
          className="mt-4 bg-green-600 text-white px-6 py-3 rounded-full hover:bg-green-700 transition"
        >
          Quero Anunciar
        </button>
      </section>

      {/* Carrossel Prestadores */}
      <section className="px-4 py-12 bg-gray-50">
        <h2 className="text-2xl font-bold text-green-700 mb-6 text-center">Prestadores de Serviço</h2>
        {prestadores.length === 0 ? (
          <p className="text-center text-gray-500 italic">Nenhum prestador cadastrado ainda.</p>
        ) : (
          <div className="relative">
            <button onClick={() => scrollLeft(scrollRefPrestadores)} className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded shadow">◀</button>
            <div ref={scrollRefPrestadores} className="flex overflow-x-auto space-x-6 p-4 scroll-smooth">
              {prestadores.map((p) => (
                <div key={p.id} className="min-w-[200px] bg-white p-4 rounded shadow hover:shadow-md transition flex-shrink-0">
                  <img
                    src={p.foto ? `http://localhost:5000${p.foto}` : "/default-user.png"}
                    alt={p.nome}
                    className="h-20 w-20 mx-auto rounded-full border object-cover"
                  />
                  <p className="mt-3 font-semibold text-center">{p.nome}</p>
                </div>
              ))}
            </div>
            <button onClick={() => scrollRight(scrollRefPrestadores)} className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded shadow">▶</button>
          </div>
        )}
      </section>

      {/* Carrossel Serviços */}
      <section className="px-4 py-12 bg-white">
        <h2 className="text-2xl font-bold text-green-700 mb-6 text-center">Serviços Disponíveis</h2>
        {servicos.length === 0 ? (
          <p className="text-center text-gray-500 italic">Nenhum serviço cadastrado ainda.</p>
        ) : (
          <div className="relative">
            <button onClick={() => scrollLeft(scrollRefServicos)} className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded shadow">◀</button>
            <div ref={scrollRefServicos} className="flex overflow-x-auto space-x-6 p-4 scroll-smooth">
              {servicos.map((s) => (
                <div key={s.id} className="min-w-[250px] bg-white p-4 rounded shadow hover:shadow-md transition flex-shrink-0">
                  <h3 className="text-xl font-semibold text-green-700">{s.tipo}</h3>
                  <p className="text-sm italic text-gray-500 mt-1">
                    {s.fotos?.length ? "Com foto" : "Sem fotos disponíveis"}
                  </p>
                  <p className="text-gray-700 mt-2">{s.descricao}</p>
                  <p className="text-sm text-gray-600 mt-2">
                    <strong>Categoria:</strong> {s.categoria} <br />
                    <strong>Local:</strong> {s.localizacao} <br />
                    <strong>Criado em:</strong> {new Date(s.data_criacao).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
            <button onClick={() => scrollRight(scrollRefServicos)} className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded shadow">▶</button>
          </div>
        )}
      </section>

      {/* Carrossel Fazendas */}
      <section className="px-4 py-12 bg-gray-50">
        <h2 className="text-2xl font-bold text-green-700 mb-6 text-center">Fazendas Disponíveis</h2>
        {fazendas.length === 0 ? (
          <p className="text-center text-gray-500 italic">Nenhuma fazenda cadastrada ainda.</p>
        ) : (
          <div className="relative">
            <button onClick={() => scrollLeft(scrollRefFazendas)} className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded shadow">◀</button>
            <div ref={scrollRefFazendas} className="flex overflow-x-auto space-x-6 p-4 scroll-smooth">
              {fazendas.map((f) => (
                <div key={f.id} className="min-w-[250px] bg-white p-4 rounded shadow hover:shadow-md transition flex-shrink-0">
                  {/* Imagem de capa se houver */}
                  {f.fotos?.length > 0 ? (
                    <img
                      src={f.fotos[0].url_foto}
                      alt={`Foto da fazenda ${f.nome}`}
                      className="h-40 w-full object-cover rounded mb-3"
                    />
                  ) : (
                    <div className="h-40 w-full bg-gray-200 flex items-center justify-center text-gray-500 rounded mb-3">
                      Sem imagem
                    </div>
                  )}
                  <h3 className="text-lg font-semibold text-green-800">{f.nome}</h3>
                  <p className="text-sm text-gray-700 mt-1">{f.descricao}</p>
                  <p className="text-sm text-gray-600 mt-2">
                    <strong>Local:</strong> {f.localizacao} <br />
                    <strong>Atividade:</strong> {f.tipo_atividade} <br />
                    <strong>Área:</strong> {f.area_total} ha <br />
                    <strong>Criado em:</strong> {new Date(f.data_criacao).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
            <button onClick={() => scrollRight(scrollRefFazendas)} className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded shadow">▶</button>
          </div>
        )}
      </section>


      {/* Depoimentos */}
      <section className="py-12 bg-green-50">
        <h2 className="text-2xl font-bold text-green-700 text-center mb-6">O que dizem nossos usuários</h2>
        <div className="max-w-4xl mx-auto px-4 grid sm:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded shadow">
            <p className="text-sm text-gray-700 italic">"Consegui alugar minha fazenda em menos de uma semana! Muito fácil e direto."</p>
            <p className="mt-4 font-semibold text-green-800">José da Silva - GO</p>
          </div>
          <div className="bg-white p-6 rounded shadow">
            <p className="text-sm text-gray-700 italic">"Excelente plataforma para divulgar meu serviço de tratorista. Recomendo!"</p>
            <p className="mt-4 font-semibold text-green-800">Luciana Oliveira - MG</p>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}

export default Home;
