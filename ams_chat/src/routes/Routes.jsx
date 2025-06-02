import { BrowserRouter, Routes, Route } from "react-router-dom";
import PrivateRoute from "../components/PrivateRoute";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Cadastro from "../pages/Cadastro";
import Dashboard from "../pages/Dashboard";
import CadastroServico from "../pages/CadastroServico";
import Servicos from "../pages/Servicos";
import Contato from "../pages/Contato";
import Descontos from "../pages/Descontos";
import Parceiros from "../pages/Parceiros";
import PainelUsuario from "../pages/PainelUsuario";
import Sobre from "../pages/Sobre";
import Fazendas from "../pages/Fazendas";
import CadastroFazenda from "../pages/CadastroFazenda";
import EditarFazenda from "../pages/EditarFazenda";
import EditarServico from "../pages/EditarServico";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
        <Route path="/servicos" element={<Servicos />} />
        <Route path="/contato" element={<Contato />} />
        <Route path="/descontos" element={<Descontos />} />
        <Route path="/parceiros" element={<Parceiros />} />
        <Route path="/sobre" element={<Sobre />} />
        <Route path="/fazendas" element={<Fazendas />} />

        {/* ROTAS PROTEGIDAS */}
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/painel-usuario"
          element={
            <PrivateRoute>
              <PainelUsuario />
            </PrivateRoute>
          }
        />
        <Route
          path="/cadastrofazendas"
          element={
            <PrivateRoute>
              <CadastroFazenda />
            </PrivateRoute>
          }
        />
        <Route
          path="/editarfazenda/:id"
          element={
            <PrivateRoute>
              <EditarFazenda />
            </PrivateRoute>
          }
        />
        <Route
          path="/servicos/novo"
          element={
            <PrivateRoute>
              <CadastroServico />
            </PrivateRoute>
          }
        />
        <Route
          path="/servicos/editar/:id"
          element={
            <PrivateRoute>
              <EditarServico />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;
