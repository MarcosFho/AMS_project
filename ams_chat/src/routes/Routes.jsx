import { BrowserRouter, Routes, Route } from "react-router-dom";
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
import EditarServico from "../pages/EditarServico";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
        <Route path="/dashboard" element={<Dashboard />} />
        {/* ROTA NOVA para criar serviço */}
        <Route path="/servicos/novo" element={<CadastroServico />} />
        {/* Listagem de serviços */}
        <Route path="/servicos" element={<Servicos />} />
        <Route path="/contato" element={<Contato />} />
        <Route path="/descontos" element={<Descontos />} />
        <Route path="/parceiros" element={<Parceiros />} />
        <Route path="/painel-usuario" element={<PainelUsuario />} />
        <Route path="/sobre" element={<Sobre />} />
        <Route path="/fazendas" element={<Fazendas />} />
        <Route path="/servicos/editar/:id" element={<EditarServico />} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;
