import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";

const tiposAtividade = [
  "Cultivo Agrícola", "Pecuária", "Silvicultura", "Uso de Máquinas Agrícolas",
  "Aplicação com Drones", "Transporte de Cargas", "Irrigação",
  "Aragem e Preparo de Solo", "Colheita", "Consultoria Técnica",
  "Manejo Integrado", "Outro"
];

function EditarFazenda() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    nome: "",
    descricao: "",
    area_total: "",
    localizacao: "",
    tipo_atividade: "",
  });
  const [tipoOutro, setTipoOutro] = useState("");
  const [fotos, setFotos] = useState([]);
  const [erro, setErro] = useState("");

  useEffect(() => {
    async function carregarFazenda() {
      try {
        const res = await api.get(`/fazendas/${id}`);
        const f = res.data;
        setForm({
          nome: f.nome || "",
          descricao: f.descricao || "",
          area_total: f.area_total || "",
          localizacao: f.localizacao || "",
          tipo_atividade: f.tipo_atividade || "",
        });
        if (!tiposAtividade.includes(f.tipo_atividade)) {
          setForm((prev) => ({ ...prev, tipo_atividade: "Outro" }));
          setTipoOutro(f.tipo_atividade);
        }
      } catch (err) {
        console.error("Erro ao carregar fazenda:", err);
        setErro("Erro ao carregar dados da fazenda.");
      }
    }

    carregarFazenda();
  }, [id]);

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

    const tipoFinal = form.tipo_atividade === "Outro" ? tipoOutro : form.tipo_atividade;

    if (!form.nome || !form.descricao || !form.area_total || !form.localizacao || !tipoFinal) {
      setErro("Preencha todos os campos obrigatórios.");
      return;
    }

    const formData = new FormData();
    formData.append("nome", form.nome);
    formData.append("descricao", form.descricao);
    formData.append("area_total", form.area_total);
    formData.append("localizacao", form.localizacao);
    formData.append("tipo_atividade", tipoFinal);

    fotos.forEach((foto) => {
      formData.append("fotos", foto);
    });

    try {
      await api.put(`/fazendas/${id}`, formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      alert("Fazenda atualizada com sucesso!");
      navigate("/fazendas");
    } catch (err) {
      console.error(err);
      setErro("Erro ao atualizar a fazenda.");
    }
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-50 pt-8">
      <div className="bg-white shadow rounded p-8 w-full max-w-lg">
        <h2 className="text-2xl font-bold text-green-700 mb-6">Editar Fazenda</h2>

        {erro && <div className="text-red-600 mb-4">{erro}</div>}

        <form className="space-y-4" onSubmit={handleSubmit} encType="multipart/form-data">
          <div>
            <label className="block font-medium">Nome da Fazenda</label>
            <input
              name="nome"
              value={form.nome}
              onChange={handleChange}
              required
              className="w-full border rounded px-3 py-2"
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
            />
          </div>

          <div>
            <label className="block font-medium">Área Total (ha)</label>
            <input
              type="number"
              name="area_total"
              value={form.area_total}
              onChange={handleChange}
              required
              min="0"
              step="0.1"
              className="w-full border rounded px-3 py-2"
            />
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
            <label className="block font-medium">Tipo de Atividade</label>
            <select
              name="tipo_atividade"
              value={form.tipo_atividade}
              onChange={handleChange}
              required
              className="w-full border rounded px-3 py-2"
            >
              <option value="">Selecione</option>
              {tiposAtividade.map((tipo) => (
                <option key={tipo} value={tipo}>{tipo}</option>
              ))}
            </select>
          </div>

          {form.tipo_atividade === "Outro" && (
            <div>
              <label className="block font-medium">Informe o Tipo de Atividade</label>
              <input
                type="text"
                value={tipoOutro}
                onChange={(e) => setTipoOutro(e.target.value)}
                required
                placeholder="Descreva a atividade"
                className="w-full border rounded px-3 py-2"
              />
            </div>
          )}

          <div>
            <label className="block font-medium">Atualizar Fotos (opcional)</label>
            <input
              type="file"
              accept="image/*"
              multiple
              onChange={handleFotosChange}
              className="w-full"
            />
            <p className="text-xs text-gray-500 mt-1">Se nada for enviado, fotos atuais serão mantidas.</p>
          </div>

          <div className="flex justify-between pt-4">
            <button
              type="button"
              onClick={() => navigate("/fazendas")}
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

export default EditarFazenda;
