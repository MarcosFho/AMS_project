import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import { jwtDecode } from "jwt-decode";
import api from "../services/api";

function Header() {
  const navigate = useNavigate();
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [mostrarMenu, setMostrarMenu] = useState(false);
  const [perfil, setPerfil] = useState(null);
  const [fotoUrl, setFotoUrl] = useState("/default-user.png");
  const menuRef = useRef();

  function isAdmin(perfil) {
    if (!perfil) return false;
    if (perfil.tipo_usuario) return perfil.tipo_usuario === "ADMIN";
    if (perfil.tipo_usuario_id) return perfil.tipo_usuario_id === 1;
    return false;
  }

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      try {
        const decoded = jwtDecode(storedToken);
        setPerfil(decoded);
        setToken(storedToken);
      } catch (e) {
        localStorage.removeItem("token");
        setToken(null);
        setPerfil(null);
      }
    }
  }, []);

  useEffect(() => {
    async function fetchFoto() {
      if (!token) {
        setFotoUrl("/default-user.png");
        return;
      }
      try {
        const res = await api.get("/usuarios/me", {
          headers: { Authorization: `Bearer ${token}` }
        });
        let url = res.data?.foto_url;

        // Verifica se existe, se é string válida e não é 'null'
        if (!url || typeof url !== "string" || url.trim() === "" || url === "null") {
          setFotoUrl("/default-user.png");
          return;
        }

        // Remove espaços
        url = url.trim();

        // Corrige caminhos relativos do backend (funciona para "fotos_usuarios/...", "/fotos_usuarios/..." etc)
        if (!url.startsWith("http")) {
          url = `http://localhost:5000/uploads/${url.replace(/^\/+/, "")}`;
        }

        setFotoUrl(url); // Corrigido: seta sempre!
      } catch {
        setFotoUrl("/default-user.png");
      }
    }
    fetchFoto();
  }, [token]);


  useEffect(() => {
    function handleClick(e) {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMostrarMenu(false);
      }
    }
    if (mostrarMenu) {
      window.addEventListener("mousedown", handleClick);
    }
    return () => window.removeEventListener("mousedown", handleClick);
  }, [mostrarMenu]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setPerfil(null);
    setFotoUrl("/default-user.png");
    navigate("/login");
  };

  const links = [
    { nome: "Início", path: "/" },
    { nome: "Serviços", path: "/servicos" },
    { nome: "Fazendas", path: "/fazendas" },
    { nome: "Parceiros", path: "/parceiros" },
    { nome: "Descontos", path: "/descontos" },
    { nome: "Contato", path: "/contato" },
    { nome: "Sobre", path: "/sobre" },
  ];

  // Função para tratar erro de imagem (uma vez só)
  function handleImgError(e) {
    if (e.target.src !== window.location.origin + "/default-user.png") {
      e.target.src = "/default-user.png";
    }
  }

  return (
    <header className="bg-white shadow sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <Link to="/">
          <img src="/logo.png" alt="AMS Logo" className="h-10" />
        </Link>
        <nav className="space-x-6 text-sm font-medium text-green-800 flex items-center">
          {links.map((item) => (
            <Link
              key={item.nome}
              to={item.path}
              className="hover:shadow-md hover:shadow-green-300 transition px-2 py-1 rounded"
            >
              {item.nome}
            </Link>
          ))}

          {isAdmin(perfil) && (
            <button
              onClick={() => navigate("/mensagemfaleconosco")}
              className="hover:shadow-md hover:shadow-green-300 transition px-2 py-1 rounded"
            >
              Mensagens
            </button>
          )}

          {!token ? (
            // --- DESLOGADO: SÓ botão Entrar ---
            <Link
              to="/login"
              className="bg-green-600 text-white px-4 py-1 rounded hover:bg-green-700 hover:shadow-md hover:shadow-green-300 transition flex items-center gap-2"
            >
              Entrar
            </Link>
          ) : (
            // --- LOGADO: botão Perfil e foto ---
            <div className="relative flex items-center gap-4" ref={menuRef}>
              <button
                onClick={() => setMostrarMenu((v) => !v)}
                className="bg-green-600 text-white px-5 py-1 rounded shadow-lg hover:bg-green-700 transition-all focus:outline-none font-semibold relative z-20"
                style={{
                  boxShadow: mostrarMenu
                    ? "0 4px 12px rgba(16,100,48,0.18)"
                    : undefined
                }}
              >
                Perfil
              </button>
              <img
                src={fotoUrl}
                alt="Perfil"
                className="h-12 w-12 rounded-full border object-cover"
                onError={handleImgError}
                title="Foto do usuário"
              />
              {/* MENU: dropdown colado e alinhado com o botão Perfil */}
              {mostrarMenu && (
                <div
                  className="absolute top-[105%] left-0 min-w-[160px] bg-white border shadow-xl rounded-xl py-2 transition-all duration-150 animate-fade-in z-30"
                  style={{
                    boxShadow: "0 8px 32px 0 rgba(34,197,94,.13)",
                  }}
                >
                  <button
                    onClick={() => {
                      setMostrarMenu(false);
                      navigate("/painelusuario");
                    }}
                    className="block w-full text-left px-6 py-3 hover:bg-green-50 hover:shadow-md hover:shadow-green-300 transition rounded-t-xl font-medium text-green-800"
                  >
                    Editar Dados
                  </button>
                  <button
                    onClick={handleLogout}
                    className="block w-full text-left px-6 py-3 hover:bg-red-50 hover:shadow-md hover:shadow-green-300 transition rounded-b-xl font-medium text-red-700"
                  >
                    Sair
                  </button>
                </div>
              )}
            </div>
          )}
        </nav>
      </div>
      <style>
        {`
        @keyframes fade-in {
          0% { opacity: 0; transform: translateY(-15px);}
          100% { opacity: 1; transform: translateY(0);}
        }
        .animate-fade-in {
          animation: fade-in 0.18s cubic-bezier(.37,1.12,.64,1) both;
        }
        `}
      </style>
    </header>
  );
}

export default Header;
