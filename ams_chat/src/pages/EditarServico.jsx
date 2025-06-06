import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";
import Header from "../components/Header";
import Footer from "../components/Footer";

function EditarServico() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    tipo: "",
    descricao: "",
    preco: "",
    categoria: "",
    localizacao: ""
  });
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(true);

  // Opções do select de tipo
  const tiposDeServico = [
    "Agronômicos",
    "Drones",
    "Fretes",
    "Maquinários",
    "Nutrição",
    "Recondicionadores",
    "Serviços Gerais",
    "Técnicos",
    "Veterinários",
    "Outros"
  ];


  useEffect(() => {
    async function fetchServico() {
      try {
        const res = await api.get(`/servicos/${id}`);
        setForm({
          tipo: res.data.tipo || "",
          descricao: res.data.descricao || "",
          preco: res.data.preco || "",
          categoria: res.data.categoria || "",
          localizacao: res.data.localizacao || ""
        });
        setCarregando(false);
      } catch (error) {
        setErro("Erro ao carregar serviço.");
        setCarregando(false);
      }
    }
    fetchServico();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSalvar = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/servicos/${id}`, form);
      alert("Serviço atualizado com sucesso!");
      navigate("/servicos");
    } catch (error) {
      setErro("Erro ao salvar alterações.");
    }
  };

  const handleVoltar = () => {
    navigate(-1); // Volta para a página anterior
  };

  if (carregando) return <div>Carregando...</div>;

  return (
    <>
      <Header />
      <main className="max-w-xl mx-auto mt-8 p-4 bg-white rounded shadow">
        <h1 className="text-2xl font-bold text-green-800 mb-4">Editar Serviço</h1>
        {erro && <p className="text-red-600 mb-2">{erro}</p>}

        <form onSubmit={handleSalvar} className="space-y-4">
          <div>
            <label className="block">Tipo:</label>
            <select
              name="tipo"
              value={form.tipo}
              onChange={handleChange}
              className="w-full border rounded px-3 py-2"
              required
            >
              <option value="">Selecione o tipo de serviço</option>
              {tiposDeServico.map((opcao, idx) => (
                <option key={idx} value={opcao}>{opcao}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block">Descrição:</label>
            <textarea
              name="descricao"
              value={form.descricao}
              onChange={handleChange}
              className="w-full border rounded px-3 py-2"
              required
            />
          </div>
          <div>
            <label className="block">Preço:</label>
            <input
              type="number"
              name="preco"
              value={form.preco}
              onChange={handleChange}
              className="w-full border rounded px-3 py-2"
              min="0"
              step="0.01"
            />
          </div>
          <div>
            <label className="block">Categoria:</label>
            <input
              type="text"
              name="categoria"
              value={form.categoria}
              onChange={handleChange}
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div>
            <label className="block">Localização:</label>
            <input
              type="text"
              name="localizacao"
              value={form.localizacao}
              onChange={handleChange}
              className="w-full border rounded px-3 py-2"
            />
          </div>
          <div className="flex gap-4 justify-end mt-6">
            <button
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            >
              Salvar Alterações
            </button>
            <button
              onClick={handleVoltar}
              type="button"
              className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-700 transition"
            >
              Voltar
            </button>
          </div>
        </form>
      </main>
      <Footer />
    </>
  );
}

export default EditarServico;
