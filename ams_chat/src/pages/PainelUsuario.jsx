import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import api from "../services/api";

function PainelUsuario() {
  const [usuario, setUsuario] = useState(null);
  const [editando, setEditando] = useState(false);
  const [foto, setFoto] = useState(null); // Novo: armazena arquivo novo
  const [fotoPreview, setFotoPreview] = useState(null); // Preview instantâneo
  const inputFotoRef = useRef();

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

        // Endereço preenchido direto do objeto usuario.endereco
        if (resUsuario.data.endereco) {
          setFormEndereco({
            rua: resUsuario.data.endereco.rua || "",
            numero: resUsuario.data.endereco.numero || "",
            bairro: resUsuario.data.endereco.bairro || "",
            cidade: resUsuario.data.endereco.cidade || "",
            estado: resUsuario.data.endereco.estado || "",
            cep: resUsuario.data.endereco.cep || "",
            complemento: resUsuario.data.endereco.complemento || "",
          });
        } else {
          setFormEndereco({
            rua: "",
            numero: "",
            bairro: "",
            cidade: "",
            estado: "",
            cep: "",
            complemento: "",
          });
        }
        setFotoPreview(null);
        setFoto(null);
      } catch (err) {
        console.error("Erro ao carregar dados:", err);
        navigate("/login");
      }
    }

    fetchDados();
  }, [navigate]);

  const handleChangeUsuario = (e) => {
    const { name, value } = e.target;
    setFormUsuario((prev) => ({ ...prev, [name]: value }));
  };

  const handleChangeEndereco = (e) => {
    const { name, value } = e.target;
    setFormEndereco((prev) => ({ ...prev, [name]: value }));
  };

  // Novo: ao escolher arquivo de foto
  const handleFotoChange = (e) => {
    const file = e.target.files[0];
    setFoto(file);
    if (file) {
      setFotoPreview(URL.createObjectURL(file));
    } else {
      setFotoPreview(null);
    }
  };

  // Novo: remover foto escolhida (antes do envio)
  const handleRemoverFoto = () => {
    setFoto(null);
    setFotoPreview(null);
    if (inputFotoRef.current) inputFotoRef.current.value = "";
  };

  const handleSalvar = async () => {
    if (!usuario?.id) {
      alert("ID do usuário não encontrado! Faça login novamente.");
      return;
    }
    try {
      // Caso vá atualizar a foto, envia como multipart
      if (foto) {
        const formData = new FormData();
        formData.append("nome", formUsuario.nome);
        formData.append("email", formUsuario.email);
        formData.append("telefone", formUsuario.telefone);
        formData.append("foto", foto);

        await api.put(`/usuarios/${usuario.id}`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
      } else {
        // Atualiza usuário normalmente (JSON)
        await api.put(`/usuarios/${usuario.id}`, { ...formUsuario, foto_url: usuario.foto_url || null });
      }

      // Endereço
      if (usuario.endereco && usuario.endereco.id) {
        await api.put(`/enderecos/${usuario.endereco.id}`, formEndereco);
      } else {
        const res = await api.post("/enderecos", formEndereco);
        const novoEnderecoId = res.data.id;
        await api.put(`/usuarios/${usuario.id}`, { endereco_id: novoEnderecoId });
      }

      alert("Dados atualizados com sucesso!");
      setEditando(false);

      // Recarrega dados
      const resUsuarioAtualizado = await api.get("/usuarios/me");
      setUsuario(resUsuarioAtualizado.data);
      setFormUsuario({
        nome: resUsuarioAtualizado.data.nome || "",
        email: resUsuarioAtualizado.data.email || "",
        telefone: resUsuarioAtualizado.data.telefone || "",
      });
      if (resUsuarioAtualizado.data.endereco) {
        setFormEndereco({
          rua: resUsuarioAtualizado.data.endereco.rua || "",
          numero: resUsuarioAtualizado.data.endereco.numero || "",
          bairro: resUsuarioAtualizado.data.endereco.bairro || "",
          cidade: resUsuarioAtualizado.data.endereco.cidade || "",
          estado: resUsuarioAtualizado.data.endereco.estado || "",
          cep: resUsuarioAtualizado.data.endereco.cep || "",
          complemento: resUsuarioAtualizado.data.endereco.complemento || "",
        });
      } else {
        setFormEndereco({
          rua: "",
          numero: "",
          bairro: "",
          cidade: "",
          estado: "",
          cep: "",
          complemento: "",
        });
      }
      setFoto(null);
      setFotoPreview(null);
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

          {/* FOTO DE PERFIL */}
          <div>
            <label className="block">Foto de Perfil:</label>
            <div className="flex items-center space-x-4">
              <img
                src={
                  fotoPreview ||
                  (usuario.foto_url
                    ? `http://localhost:5000${usuario.foto_url.startsWith('/') ? usuario.foto_url : '/' + usuario.foto_url}`
                    : "/default-avatar.png")
                }
                alt="Foto do perfil"
                className="w-20 h-20 object-cover rounded-full border"
              />
              {editando && (
                <div>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFotoChange}
                    ref={inputFotoRef}
                    className="block"
                  />
                  {fotoPreview && (
                    <button
                      type="button"
                      onClick={handleRemoverFoto}
                      className="text-red-600 mt-1 text-sm"
                    >
                      Remover foto escolhida
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>

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
