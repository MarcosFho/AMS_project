import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

const categorias = [
  "Agronômicos", "Veterinários", "Nutrição",
  "Serviços Gerais", "Fretes", "Recondicionadores", "Técnicos"
];

const tipos = [
  "Serviço Agrícola", "Transporte", "Veterinário", "Consultoria", "Outro"
];

function CadastroServico() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    tipo: "",
    descricao: "",
    preco: "",
    categoria: "",
    localizacao: "",
  });

  const [fotos, setFotos] = useState([]);
  const [erro, setErro] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleFotosChange = (e) => {
    const arquivos = Array.from(e.target.files);

    if (arquivos.length > 6) {
      setErro("Você pode enviar no máximo 6 fotos.");
    } else {
      setErro("");
      setFotos(arquivos);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErro("");

    // Validação mínima
    if (!form.tipo || !form.descricao || !form.categoria || !form.localizacao) {
      setErro("Preencha todos os campos obrigatórios.");
      return;
    }

    const formData = new FormData();
    formData.append("tipo", form.tipo);
    formData.append("descricao", form.descricao);
    formData.append("categoria", form.categoria);
    formData.append("localizacao", form.localizacao);
    if (form.preco) formData.append("preco", form.preco);

    fotos.forEach((foto) => {
      formData.append("fotos", foto);
    });

    try {
      await api.post("/servicos", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      alert("Serviço cadastrado com sucesso!");
      navigate("/servicos");
    } catch (err) {
      setErro(
        err?.response?.data?.erro ||
        "Erro ao cadastrar serviço. Verifique os dados e se está logado."
      );
    }
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-50 pt-8">
      <div className="bg-white shadow rounded p-8 w-full max-w-lg">
        <h2 className="text-2xl font-bold text-green-700 mb-6">Cadastrar Serviço</h2>

        {erro && <div className="text-red-600 mb-4">{erro}</div>}

        <form className="space-y-4" onSubmit={handleSubmit} encType="multipart/form-data">
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
            </select>
          </div>

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

          <div>
            <label className="block font-medium">Fotos (até 6 imagens)</label>
            <input
              type="file"
              accept="image/*"
              multiple
              onChange={handleFotosChange}
              className="w-full"
            />
          </div>

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
              Cadastrar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CadastroServico;
