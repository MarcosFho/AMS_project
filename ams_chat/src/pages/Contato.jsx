import { useState } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import api from "../services/api";

function Contato() {
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [telefone, setTelefone] = useState("");
  const [assunto, setAssunto] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [status, setStatus] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await api.post("/fale-conosco", {
        nome,
        email,
        telefone,
        assunto,
        mensagem,
      });

      setStatus("Mensagem enviada com sucesso!");
      setNome("");
      setEmail("");
      setTelefone("");
      setAssunto("");
      setMensagem("");
    } catch (error) {
      const msg = error.response?.data?.message || "Erro ao enviar mensagem.";
      setStatus(msg);
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      {/* Banner */}
      <section
        className="h-[60vh] bg-cover bg-center flex flex-col items-center justify-center text-white text-center px-4"
        style={{ backgroundImage: "url('/bg.jpg')" }}
      >
        <h1 className="text-3xl sm:text-4xl font-bold text-white bg-black/40 px-6 py-3 rounded shadow-lg">
          ENTRE EM CONTATO CONOSCO
        </h1>
        <p className="text-3xl sm:text-4xl font-bold text-white bg-black/40 px-6 py-3 rounded shadow-lg">
          CONHEÇA NOSSAS REDES SOCIAIS
        </p>
      </section>

      {/* Título */}
      <div className="text-center py-6 bg-white text-xl font-bold text-green-800 shadow">
        ENTRE EM CONTATO CONOSCO
      </div>

      {/* Formulário */}
      <main className="flex flex-col items-center bg-gray-100 py-10 px-4">
        <div className="bg-white rounded-xl shadow-md p-8 w-full max-w-xl">
          {status && (
            <div className="mb-4 text-center font-medium text-green-700 bg-green-100 p-2 rounded">
              {status}
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="NOME"
              className="w-full border border-gray-300 p-3 rounded bg-green-100 placeholder-gray-600"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              required
            />
            <input
              type="email"
              placeholder="E-MAIL"
              className="w-full border border-gray-300 p-3 rounded bg-green-100 placeholder-gray-600"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="tel"
              placeholder="TELEFONE"
              className="w-full border border-gray-300 p-3 rounded bg-green-100 placeholder-gray-600"
              value={telefone}
              onChange={(e) => setTelefone(e.target.value)}
            />
            <textarea
              placeholder="Assunto"
              rows="1"
              className="w-full border border-gray-300 p-3 rounded bg-green-100 placeholder-gray-600"
              value={assunto}
              onChange={(e) => setAssunto(e.target.value)}
              required
            />
            <textarea
              placeholder="MENSAGEM"
              rows="5"
              className="w-full border border-gray-300 p-3 rounded bg-green-100 placeholder-gray-600"
              value={mensagem}
              onChange={(e) => setMensagem(e.target.value)}
              required
            />

            <button
              type="submit"
              className="w-full bg-green-600 text-white py-3 rounded hover:bg-green-700 transition"
            >
              ENVIAR MENSAGEM
            </button>
          </form>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default Contato;
