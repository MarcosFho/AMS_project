import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import api from "../services/api";

// ATUALIZADA: Suporta 'prestador' com foto_url ou fotos[0].url_foto
function getCardImageProps(foto, tipo) {
  if (!foto) return {};
  let src = "";
  if (tipo === "servico") {
    src = foto.url_foto.startsWith("/")
      ? `http://localhost:5000${foto.url_foto}`
      : `http://localhost:5000/uploads/servico_fotos/${foto.url_foto}`;
  } else if (tipo === "fazenda") {
    src = foto.url_foto.startsWith("/")
      ? `http://localhost:5000${foto.url_foto}`
      : `http://localhost:5000/uploads/fazenda_fotos/${foto.url_foto}`;
  } else if (tipo === "prestador") {
    // Permite tanto 'foto_url' como 'url_foto'
    const url = foto.foto_url || foto.url_foto;
    src = url?.startsWith("/")
      ? `http://localhost:5000${url}`
      : `http://localhost:5000/uploads/fotos_usuarios/${url}`;
  }
  return {
    src,
    alt:
      tipo === "servico"
        ? "Foto do serviço"
        : tipo === "fazenda"
          ? "Foto da fazenda"
          : "Foto do prestador",
    width: 140,
    height: 140,
    style: { width: 140, height: 140, objectFit: "cover" },
    className: "rounded-full mt-2 mb-3 mx-auto border object-cover"
  };
}

function Home() {
  const navigate = useNavigate();
  const [prestadores, setPrestadores] = useState([]);
  const [servicos, setServicos] = useState([]);
  const [fazendas, setFazendas] = useState([]);
  const [erro, setErro] = useState("");

  const scrollRefPrestadores = useRef(null);
  const scrollRefServicos = useRef(null);
  const scrollRefFazendas = useRef(null);

  const isLogged = !!localStorage.getItem("token");

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
        <h2 className="text-2xl font-bold text-green-800">
          Tem um serviço ou fazenda para oferecer?
        </h2>
        <p className="mt-2 text-gray-700">
          Cadastre-se agora e comece a faturar com o AMS!
        </p>
        {!isLogged ? (
          <button
            onClick={() => navigate("/cadastro")}
            className="mt-4 bg-green-600 text-white px-6 py-3 rounded-full hover:bg-green-700 transition"
          >
            Quero Anunciar
          </button>
        ) : (
          <div className="flex flex-col sm:flex-row gap-4 justify-center mt-4">
            <button
              onClick={() => navigate("/cadastroservico")}
              className="bg-green-600 text-white px-6 py-3 rounded-full hover:bg-green-700 transition"
            >
              Anunciar Serviço
            </button>
            <button
              onClick={() => navigate("/cadastrofazenda")}
              className="bg-green-700 text-white px-6 py-3 rounded-full hover:bg-green-800 transition"
            >
              Anunciar Propriedade
            </button>
          </div>
        )}
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
              {prestadores.map((p) => {
                // Suporta foto_url direto ou array fotos[0].url_foto
                const fotoPrestador =
                  (Array.isArray(p.fotos) && p.fotos.length > 0 && p.fotos[0]) ||
                  (p.foto_url ? { foto_url: p.foto_url } : null);

                return (
                  <div key={p.id} className="min-w-[200px] bg-white p-4 rounded shadow hover:shadow-md transition flex-shrink-0">
                    {fotoPrestador ? (
                      <img {...getCardImageProps(fotoPrestador, "prestador")} />
                    ) : (
                      <img
                        src="/default-user.png"
                        alt={p.nome}
                        className="h-20 w-20 mx-auto rounded-full border object-cover"
                      />
                    )}
                    <p className="mt-3 font-semibold text-center">{p.nome}</p>
                  </div>
                );
              })}
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
              {servicos.map((servico) => (
                <div key={servico.id} className="min-w-[270px] bg-white p-4 rounded shadow hover:shadow-md transition flex-shrink-0">
                  <h3 className="text-xl font-semibold text-green-800">{servico.tipo}</h3>
                  {servico.fotos && servico.fotos.length > 0 ? (
                    <img {...getCardImageProps(servico.fotos[0], "servico")} />
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
                </div>
              ))}
            </div>
            <button onClick={() => scrollRight(scrollRefServicos)} className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded shadow">▶</button>
          </div>
        )}
      </section>


      {/* Carrossel Fazendas */}
      <section className="px-4 py-12 bg-gray-50">
        <h2 className="text-2xl font-bold text-green-700 mb-6 text-center">Áreas de Fazenda</h2>
        {fazendas.length === 0 ? (
          <p className="text-center text-gray-500 italic">Nenhuma fazenda cadastrada ainda.</p>
        ) : (
          <div className="relative">
            <button onClick={() => scrollLeft(scrollRefFazendas)} className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded shadow">◀</button>
            <div ref={scrollRefFazendas} className="flex overflow-x-auto space-x-6 p-4 scroll-smooth">
              {fazendas.map((f) => (
                <div key={f.id} className="min-w-[250px] bg-white p-5 rounded-xl shadow hover:shadow-md transition flex-shrink-0">
                  <h3 className="text-lg font-semibold text-green-800 mb-2">{f.nome}</h3>
                  {f.fotos && f.fotos.length > 0 ? (
                    <img {...getCardImageProps(f.fotos[0], "fazenda")} />
                  ) : (
                    <div className="text-gray-400 italic mt-2 mb-3">Sem fotos disponíveis</div>
                  )}
                  <p className="text-gray-700">{f.descricao}</p>
                  <p className="text-sm text-gray-600 mt-2">
                    {f.area_total && (
                      <>
                        <strong>Área Total:</strong> {f.area_total} ha <br />
                      </>
                    )}
                    <strong>Local:</strong> {f.localizacao || "—"} <br />
                    <strong>Criado em:</strong>{" "}
                    {f.data_criacao
                      ? new Date(f.data_criacao).toLocaleDateString("pt-BR")
                      : "—"}
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
