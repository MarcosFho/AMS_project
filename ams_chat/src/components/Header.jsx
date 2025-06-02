import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";

function Header() {
  const navigate = useNavigate();
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [mostrarMenu, setMostrarMenu] = useState(false);

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      try {
        const decoded = jwtDecode(storedToken); // ✅ Correto agora
        setToken(storedToken);
      } catch (e) {
        localStorage.removeItem("token");
        setToken(null);
      }
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
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

          {!token ? (
            <Link
              to="/login"
              className="bg-green-600 text-white px-4 py-1 rounded hover:bg-green-700 hover:shadow-md hover:shadow-green-300 transition"
            >
              Entrar
            </Link>
          ) : (
            <div className="relative">
              <button
                onClick={() => setMostrarMenu(!mostrarMenu)}
                className="bg-green-600 text-white px-4 py-1 rounded hover:bg-green-700 hover:shadow-md hover:shadow-green-300 transition"
              >
                Perfil
              </button>
              {mostrarMenu && (
                <div className="absolute right-0 mt-2 w-40 bg-white border shadow-lg rounded z-10">
                  <button
                    onClick={() => {
                      setMostrarMenu(false);
                      navigate("/painel-usuario");
                    }}
                    className="block w-full text-left px-4 py-2 hover:bg-green-50 hover:shadow-md hover:shadow-green-300 transition"
                  >
                    Editar Dados
                  </button>
                  <button
                    onClick={handleLogout}
                    className="block w-full text-left px-4 py-2 hover:bg-red-50 hover:shadow-md hover:shadow-green-300 transition"
                  >
                    Sair
                  </button>
                </div>
              )}
            </div>
          )}
        </nav>
      </div>
    </header>
  );
}

export default Header;
