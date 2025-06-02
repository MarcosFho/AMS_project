import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import SocialLoginButtons from "../components/SocialLoginButtons";
import api from "../services/api";

function Cadastro() {
  const [tipoPessoa, setTipoPessoa] = useState("FISICA");
  const [foto, setFoto] = useState(null);
  const [preview, setPreview] = useState(null);

  const [form, setForm] = useState({
    nome: "",
    email: "",
    telefone: "",
    senha: "",
    confirmarSenha: "",
    tipo_usuario: "PRESTADOR",
  });

  const [pf, setPf] = useState({
    cpf: "",
    rg: "",
    data_nascimento: "",
  });

  const [pj, setPj] = useState({
    razao_social: "",
    cnpj: "",
    cnae: "",
    inscricao_estadual: "",
  });

  const [endereco, setEndereco] = useState({
    cep: "",
    rua: "",
    numero: "",
    bairro: "",
    cidade: "",
    estado: "",
    complemento: "",
  });

  const [carregandoCep, setCarregandoCep] = useState(false);
  const [erro, setErro] = useState("");
  const [enviando, setEnviando] = useState(false);
  const navigate = useNavigate();

  // Manipuladores
  const handleChange = (e) => setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  const handleChangePF = (e) => setPf((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  const handleChangePJ = (e) => setPj((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  const handleChangeEndereco = (e) => setEndereco((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  const handleTipoPessoa = (e) => setTipoPessoa(e.target.value);

  // Preview da foto
  const handleFotoChange = (e) => {
    const file = e.target.files[0];
    setFoto(file);
    if (file) setPreview(URL.createObjectURL(file));
    else setPreview(null);
  };

  // CEP auto-preenchimento
  const buscarEnderecoPorCep = async (cep) => {
    cep = cep.replace(/\D/g, "");
    if (cep.length !== 8) return;
    setCarregandoCep(true);
    try {
      const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
      const data = await response.json();
      setCarregandoCep(false);
      if (data.erro) return;
      setEndereco((prev) => ({
        ...prev,
        rua: data.logradouro || "",
        bairro: data.bairro || "",
        cidade: data.localidade || "",
        estado: data.uf || "",
        complemento: data.complemento || "",
      }));
    } catch {
      setCarregandoCep(false);
    }
  };

  const handleCepBlur = async (e) => {
    await buscarEnderecoPorCep(e.target.value);
  };

  // Envio do formulário
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErro("");
    setEnviando(true);

    // Validações
    if (!form.nome || !form.email || !form.telefone || !form.senha || !form.confirmarSenha) {
      setErro("Preencha todos os campos obrigatórios.");
      setEnviando(false);
      return;
    }
    if (form.senha !== form.confirmarSenha) {
      setErro("As senhas não coincidem.");
      setEnviando(false);
      return;
    }
    if (tipoPessoa === "FISICA" && !pf.cpf) {
      setErro("Preencha o CPF.");
      setEnviando(false);
      return;
    }
    if (tipoPessoa === "JURIDICA" && !pj.cnpj) {
      setErro("Preencha o CNPJ.");
      setEnviando(false);
      return;
    }
    if (!endereco.cep || !endereco.rua || !endereco.numero || !endereco.bairro || !endereco.cidade || !endereco.estado) {
      setErro("Preencha todos os campos de endereço.");
      setEnviando(false);
      return;
    }

    try {
      const resEndereco = await api.post("/enderecos", endereco);
      const id_endereco = resEndereco.data.id;
      // 2. Monta formData para incluir foto
      const formData = new FormData();
      formData.append("nome", form.nome);
      formData.append("email", form.email);
      formData.append("telefone", form.telefone);
      formData.append("senha", form.senha);
      formData.append("tipo_usuario", form.tipo_usuario);
      formData.append("id_endereco", id_endereco);
      if (foto) formData.append("foto", foto);

      // ✅ Debug: verifique os dados antes de enviar
      console.log("📦 Campos enviados no FormData:");
      for (let [key, value] of formData.entries()) {
        console.log(`${key}:`, value);
      }

      // 3. Cria usuário
      const resUsuario = await api.post("/usuarios", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const usuarioId = resUsuario.data.id;

      // 4. PF ou PJ
      if (tipoPessoa === "FISICA") {
        await api.post("/pessoas-fisicas", {
          id_usuario: usuarioId,
          ...pf,
        });
      } else {
        await api.post("/pessoas-juridicas", {
          id_usuario: usuarioId,
          ...pj,
        });
      }

      alert("Cadastro realizado com sucesso!");
      navigate("/login");
    } catch (error) {
      console.error("Erro ao cadastrar:", error);
      setErro("Erro ao cadastrar. Verifique os dados e tente novamente.");
    } finally {
      setEnviando(false);
    }
  };

  return (
    <div className="min-h-screen bg-cover bg-center flex flex-col" style={{ backgroundImage: "url('/bg.jpg')" }}>
      <Header />

      <main className="flex-grow flex items-center justify-center bg-black bg-opacity-40 px-4">
        <div className="bg-white/90 backdrop-blur-md shadow-xl rounded-2xl p-8 w-full max-w-4xl transition-all duration-300">
          <h2 className="text-3xl font-bold mb-6 text-green-700 text-center">Criar Conta</h2>
          {erro && <p className="text-red-600 text-sm mb-4">{erro}</p>}

          <form
            className="grid grid-cols-1 md:grid-cols-2 gap-8"
            onSubmit={handleSubmit}
            encType="multipart/form-data"
            autoComplete="off"
          >
            {/* Coluna Perfil */}
            <div>
              <label className="block text-gray-700">Tipo de Conta:</label>
              <select className="w-full border rounded-md p-2 mb-2" value={form.tipo_usuario} name="tipo_usuario" onChange={handleChange}>
                <option value="PRESTADOR">Prestador de Serviço</option>
                <option value="CLIENTE">Produtor Rural</option>
                <option value="ADMIN">Administrador do Sistema</option>
                <option value="USUARIO">Usuário</option>
              </select>

              <div className="flex gap-4 mb-2">
                <label>
                  <input type="radio" name="tipoPessoa" value="FISICA" checked={tipoPessoa === "FISICA"} onChange={handleTipoPessoa} />
                  <span className="ml-2">Pessoa Física</span>
                </label>
                <label>
                  <input type="radio" name="tipoPessoa" value="JURIDICA" checked={tipoPessoa === "JURIDICA"} onChange={handleTipoPessoa} />
                  <span className="ml-2">Pessoa Jurídica</span>
                </label>
              </div>

              {/* Campos gerais */}
              <input type="text" name="nome" placeholder="Nome completo / Razão Social" className="w-full border rounded-md p-2 mb-2" value={form.nome} onChange={handleChange} required />
              <input type="email" name="email" placeholder="E-mail" className="w-full border rounded-md p-2 mb-2" value={form.email} onChange={handleChange} required />
              <input type="text" name="telefone" placeholder="Telefone" className="w-full border rounded-md p-2 mb-2" value={form.telefone} onChange={handleChange} required />
              <input type="password" name="senha" placeholder="Senha" className="w-full border rounded-md p-2 mb-2" value={form.senha} onChange={handleChange} required autoComplete="new-password" />
              <input type="password" name="confirmarSenha" placeholder="Confirmar senha" className="w-full border rounded-md p-2 mb-2" value={form.confirmarSenha} onChange={handleChange} required autoComplete="new-password" />

              {/* Upload de foto */}
              <label className="block text-gray-700 mb-2">Foto de perfil:</label>
              <input type="file" accept="image/*" onChange={handleFotoChange} className="w-full mb-2" />
              {preview && (
                <div className="mb-2 flex flex-col items-center">
                  <img src={preview} alt="Preview" className="w-24 h-24 object-cover rounded-full border" />
                  <p className="text-xs text-gray-500 text-center">Pré-visualização</p>
                </div>
              )}

              {/* Campos PF ou PJ */}
              {tipoPessoa === "FISICA" ? (
                <>
                  <input type="text" name="cpf" placeholder="CPF" className="w-full border rounded-md p-2 mb-2" value={pf.cpf} onChange={handleChangePF} required />
                  <input type="text" name="rg" placeholder="RG" className="w-full border rounded-md p-2 mb-2" value={pf.rg} onChange={handleChangePF} />
                  <input type="date" name="data_nascimento" placeholder="Data de Nascimento" className="w-full border rounded-md p-2 mb-2" value={pf.data_nascimento} onChange={handleChangePF} />
                </>
              ) : (
                <>
                  <input type="text" name="razao_social" placeholder="Razão Social" className="w-full border rounded-md p-2 mb-2" value={pj.razao_social} onChange={handleChangePJ} required />
                  <input type="text" name="cnpj" placeholder="CNPJ" className="w-full border rounded-md p-2 mb-2" value={pj.cnpj} onChange={handleChangePJ} required />
                  <input type="text" name="cnae" placeholder="CNAE" className="w-full border rounded-md p-2 mb-2" value={pj.cnae} onChange={handleChangePJ} />
                  <input type="text" name="inscricao_estadual" placeholder="Inscrição Estadual" className="w-full border rounded-md p-2 mb-2" value={pj.inscricao_estadual} onChange={handleChangePJ} />
                </>
              )}
            </div>

            {/* Coluna Endereço */}
            <div>
              <h4 className="block text-gray-700 mb-2">Endereço</h4>
              <input type="text" name="cep" placeholder="CEP" className="w-full border rounded-md p-2 mb-2" value={endereco.cep} onChange={handleChangeEndereco} onBlur={handleCepBlur} required maxLength={9} />
              {carregandoCep && <p className="text-gray-500 text-sm mb-2">Buscando endereço...</p>}
              <input type="text" name="rua" placeholder="Rua" className="w-full border rounded-md p-2 mb-2" value={endereco.rua} onChange={handleChangeEndereco} required />
              <input type="text" name="numero" placeholder="Número" className="w-full border rounded-md p-2 mb-2" value={endereco.numero} onChange={handleChangeEndereco} required />
              <input type="text" name="bairro" placeholder="Bairro" className="w-full border rounded-md p-2 mb-2" value={endereco.bairro} onChange={handleChangeEndereco} required />
              <input type="text" name="cidade" placeholder="Cidade" className="w-full border rounded-md p-2 mb-2" value={endereco.cidade} onChange={handleChangeEndereco} required />
              <input type="text" name="estado" placeholder="Estado" className="w-full border rounded-md p-2 mb-2" value={endereco.estado} onChange={handleChangeEndereco} required maxLength={2} />
              <input type="text" name="complemento" placeholder="Complemento" className="w-full border rounded-md p-2 mb-2" value={endereco.complemento} onChange={handleChangeEndereco} />
            </div>

            <div className="md:col-span-2">
              <button
                type="submit"
                className="mt-6 w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded"
                disabled={enviando}
              >
                {enviando ? "Cadastrando..." : "Cadastrar"}
              </button>
            </div>
          </form>

          <div className="mt-6">
            <SocialLoginButtons />
          </div>
          <p className="text-sm text-center mt-4">
            Já tem conta?{" "}
            <Link to="/login" className="text-green-700 underline">
              Entrar
            </Link>
          </p>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default Cadastro;
