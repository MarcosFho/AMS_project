import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import SocialLoginButtons from "../components/SocialLoginButtons";
import api from "../services/api"; // Conectado ao backend

function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [lembrar, setLembrar] = useState(false);
  const [mensagem, setMensagem] = useState("");
  const [tipoMensagem, setTipoMensagem] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const resposta = await api.post("/login", {
        email,
        senha,
      });

      const { access_token } = resposta.data;
      localStorage.setItem("token", access_token);
      api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;

      setMensagem("Login realizado com sucesso!");
      setTipoMensagem("sucesso");

      navigate("/");
    } catch (error) {
      setMensagem("Erro ao fazer login. Verifique usuário e senha.");
      setTipoMensagem("erro");
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex flex-col"
      style={{ backgroundImage: "url('/bg.jpg')" }}
    >
      <Header />

      <main className="flex-grow flex items-center justify-center bg-black bg-opacity-40 px-4">
        <div className="bg-white/90 backdrop-blur-md shadow-xl rounded-2xl p-8 w-full max-w-md transition-all duration-300">
          <h1 className="text-3xl font-semibold text-green-700 text-center mb-6">
            Bem-vindo ao AMS
          </h1>

          {mensagem && (
            <div
              className={`text-center font-medium p-2 rounded mb-4 ${
                tipoMensagem === "sucesso"
                  ? "bg-green-100 text-green-800"
                  : "bg-red-100 text-red-800"
              }`}
            >
              {mensagem}
            </div>
          )}

          <p className="text-center text-sm text-gray-600 mb-6">
            Ainda não tem cadastro?{" "}
            <Link to="/cadastro" className="text-green-700 hover:underline font-medium">
              Cadastre-se aqui
            </Link>
          </p>

          <form onSubmit={handleSubmit} className="space-y-4 text-left">
            <div>
              <label htmlFor="email" className="text-sm font-medium text-gray-700">
                E-mail
              </label>
              <input
                id="email"
                type="email"
                className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-green-500 focus:outline-none transition"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div>
              <label htmlFor="senha" className="text-sm font-medium text-gray-700">
                Senha
              </label>
              <input
                id="senha"
                type="password"
                className="w-full border rounded-md px-3 py-2 mt-1 focus:ring-2 focus:ring-green-500 focus:outline-none transition"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
              />
            </div>

            <div className="flex items-center gap-2 text-sm text-gray-600">
              <input
                id="lembrar"
                type="checkbox"
                checked={lembrar}
                onChange={(e) => setLembrar(e.target.checked)}
              />
              <label htmlFor="lembrar">Lembrar-me</label>
            </div>

            <button
              type="submit"
              className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded-lg shadow-sm transition-all duration-200 hover:shadow-md"
            >
              Entrar
            </button>
          </form>

          <div className="mt-4 text-center">
            <Link to="/esqueceu-senha" className="text-sm text-green-700 hover:underline transition">
              Esqueceu a senha?
            </Link>
          </div>

          <div className="mt-6">
            <SocialLoginButtons />
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default Login;
