import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import api from "../services/api";

function PainelUsuario() {
  const [usuario, setUsuario] = useState(null);
  const [editando, setEditando] = useState(false);

  const [formUsuario, setFormUsuario] = useState({
    nome: "",
    email: "",
    telefone: "",
  });

  const [formEndereco, setFormEndereco] = useState({
    rua: "",
    numero: "",
    bairro: "",
    cidade: "",
    estado: "",
    cep: "",
    complemento: "",
  });

  const navigate = useNavigate();

  useEffect(() => {
    async function fetchDados() {
      try {
        const resUsuario = await api.get("/usuarios/me");
        setUsuario(resUsuario.data);
        setFormUsuario({
          nome: resUsuario.data.nome || "",
          email: resUsuario.data.email || "",
          telefone: resUsuario.data.telefone || "",
        });

        if (resUsuario.data.endereco_id) {
          const resEndereco = await api.get(`/enderecos/${resUsuario.data.endereco_id}`);
          setFormEndereco({
            rua: resEndereco.data.rua || "",
            numero: resEndereco.data.numero || "",
            bairro: resEndereco.data.bairro || "",
            cidade: resEndereco.data.cidade || "",
            estado: resEndereco.data.estado || "",
            cep: resEndereco.data.cep || "",
            complemento: resEndereco.data.complemento || "",
          });
        }
      } catch (err) {
        console.error("Erro ao carregar dados:", err);
        navigate("/login");
      }
    }

    fetchDados();
  }, []);

  const handleChangeUsuario = (e) => {
    const { name, value } = e.target;
    setFormUsuario((prev) => ({ ...prev, [name]: value }));
  };

  const handleChangeEndereco = (e) => {
    const { name, value } = e.target;
    setFormEndereco((prev) => ({ ...prev, [name]: value }));
  };

  const handleSalvar = async () => {
    console.log("ID do usuário para update:", usuario?.id);
    if (!usuario?.id) {
      alert("ID do usuário não encontrado! Faça login novamente.");
      return;
    }

    try {
      // Atualiza usuário
      await api.put(`/usuarios/${usuario.id}`, { ...formUsuario, foto_url: usuario.foto_url || null });

      // Atualiza endereço existente ou cria novo e associa ao usuário
      if (usuario?.endereco_id) {
        await api.put(`/enderecos/${usuario.endereco_id}`, formEndereco);
      } else {
        const res = await api.post("/enderecos", formEndereco);
        const novoEnderecoId = res.data.id;
        await api.put(`/usuarios/${usuario.id}`, { endereco_id: novoEnderecoId });
      }

      alert("Dados atualizados com sucesso!");
      setEditando(false);
    } catch (error) {
      if (error.response) {
        console.error("Erro ao salvar:", error.response.data);
        const mensagem = error.response.data?.message || "Erro desconhecido";
        alert(`Erro ao salvar os dados: ${mensagem}`);
      } else if (error.request) {
        console.error("Erro na requisição:", error.request);
        alert("Erro de rede ou servidor inativo.");
      } else {
        console.error("Erro desconhecido:", error.message);
        alert("Erro inesperado: " + error.message);
      }
    }
  };

  if (!usuario) return null;

  return (
    <>
      <Header />
      <main className="max-w-4xl mx-auto mt-8 p-4">
        <h1 className="text-2xl font-bold text-green-800 mb-4">Meu Perfil</h1>

        <div className="space-y-4">
          {/* Formulário de Usuário */}
          <div>
            <label className="block">Nome:</label>
            <input
              type="text"
              name="nome"
              value={formUsuario.nome}
              onChange={handleChangeUsuario}
              disabled={!editando}
              className="w-full border rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block">Email:</label>
            <input
              type="email"
              name="email"
              value={formUsuario.email}
              onChange={handleChangeUsuario}
              disabled={!editando}
              className="w-full border rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block">Telefone:</label>
            <input
              type="text"
              name="telefone"
              value={formUsuario.telefone}
              onChange={handleChangeUsuario}
              disabled={!editando}
              className="w-full border rounded px-3 py-2"
            />
          </div>

          <hr className="my-4" />
          <h2 className="text-xl font-semibold text-green-700">Endereço</h2>

          {/* Formulário de Endereço */}
          {[
            "rua",
            "numero",
            "bairro",
            "cidade",
            "estado",
            "cep",
            "complemento",
          ].map((campo) => (
            <div key={campo}>
              <label className="block capitalize">{campo}:</label>
              <input
                type="text"
                name={campo}
                value={formEndereco[campo]}
                onChange={handleChangeEndereco}
                disabled={!editando}
                className="w-full border rounded px-3 py-2"
              />
            </div>
          ))}

          {/* Botões de ação */}
          <div className="mt-6">
            {!editando ? (
              <button
                onClick={() => setEditando(true)}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
              >
                Editar Dados
              </button>
            ) : (
              <button
                onClick={handleSalvar}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Salvar Alterações
              </button>
            )}
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}

export default PainelUsuario;
