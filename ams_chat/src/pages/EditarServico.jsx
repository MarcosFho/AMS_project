import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";

const categorias = [
  "Agronômicos", "Veterinários", "Nutrição",
  "Serviços Gerais", "Fretes", "Recondicionadores", "Técnicos"
];

const tipos = [
  "Serviço Agrícola", "Transporte", "Veterinário", "Consultoria", "Outros"
];

function EditarServico() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    tipo: "",
    outroTipo: "",
    descricao: "",
    preco: "",
    categoria: "",
    localizacao: "",
  });
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    async function fetchServico() {
      try {
        const res = await api.get(`/servicos/${id}`);
        setForm({
          tipo: tipos.includes(res.data.tipo) ? res.data.tipo : "Outros",
          outroTipo: !tipos.includes(res.data.tipo) ? res.data.tipo : "",
          descricao: res.data.descricao || "",
          preco: res.data.preco || "",
          categoria: res.data.categoria || "",
          localizacao: res.data.localizacao || "",
        });
        setCarregando(false);
      } catch (err) {
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErro("");
    const tipoFinal = form.tipo === "Outros" ? form.outroTipo.trim() : form.tipo;

    if (!tipoFinal || !form.descricao || !form.categoria || !form.localizacao) {
      setErro("Preencha todos os campos obrigatórios.");
      return;
    }

    try {
      await api.put(`/servicos/${id}`, {
        tipo: tipoFinal,
        descricao: form.descricao,
        categoria: form.categoria,
        localizacao: form.localizacao,
        preco: form.preco,
      });
      alert("Serviço atualizado com sucesso!");
      navigate("/servicos");
    } catch (err) {
      setErro("Erro ao atualizar serviço.");
    }
  };

  if (carregando) return <div className="text-center mt-8">Carregando...</div>;

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-50 pt-8">
      <div className="bg-white shadow rounded p-8 w-full max-w-lg">
        <h2 className="text-2xl font-bold text-green-700 mb-6">Editar Serviço</h2>
        {erro && <div className="text-red-600 mb-4">{erro}</div>}
        <form className="space-y-4" onSubmit={handleSubmit}>
          {/* Tipo */}
          <div>
            <label className="block font-medium">Tipo do Serviço</label>
            <select
              name="tipo"
              value={form.tipo}
              onChange={handleChange}
              required
              className="w-full border rounded px-3 py-2"
            >
              <option value="">Selecione</option>
              {tipos.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
              <option value="Outros">Outros</option>
            </select>
          </div>
          {form.tipo === "Outros" && (
            <div>
              <label className="block font-medium">Informe o Tipo do Serviço</label>
              <input
                name="outroTipo"
                value={form.outroTipo}
                onChange={handleChange}
                required
                className="w-full border rounded px-3 py-2"
                placeholder="Ex: Aplicação com drone, manutenção, etc."
              />
            </div>
          )}
          {/* Categoria */}
          <div>
            <label className="block font-medium">Categoria</label>
            <select
              name="categoria"
              value={form.categoria}
              onChange={handleChange}
              required
              className="w-full border rounded px-3 py-2"
            >
              <option value="">Selecione</option>
              {categorias.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>
          {/* Localização */}
          <div>
            <label className="block font-medium">Localização</label>
            <input
              name="localizacao"
              value={form.localizacao}
              onChange={handleChange}
              required
              className="w-full border rounded px-3 py-2"
              placeholder="Ex: Uberlândia - MG"
            />
          </div>
          {/* Preço */}
          <div>
            <label className="block font-medium">Preço (opcional)</label>
            <input
              type="number"
              name="preco"
              value={form.preco}
              onChange={handleChange}
              min="0"
              step="0.01"
              className="w-full border rounded px-3 py-2"
              placeholder="Ex: 150.00"
            />
          </div>
          {/* Descrição */}
          <div>
            <label className="block font-medium">Descrição</label>
            <textarea
              name="descricao"
              value={form.descricao}
              onChange={handleChange}
              required
              className="w-full border rounded px-3 py-2"
              rows={3}
              placeholder="Detalhe o serviço a ser anunciado"
            />
          </div>
          {/* Ações */}
          <div className="flex justify-between pt-4">
            <button
              type="button"
              onClick={() => navigate("/servicos")}
              className="bg-gray-400 text-white px-4 py-2 rounded"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
            >
              Salvar Alterações
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default EditarServico;
