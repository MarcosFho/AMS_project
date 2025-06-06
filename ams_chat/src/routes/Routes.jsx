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
import CadastroFazenda from "../pages/CadastroFazenda";
import EditarFazenda from "../pages/EditarFazenda";
import EditarServico from "../pages/EditarServico";
import MensagemFaleConosco from "../pages/MensagemFaleConosco";
import Chat from "../pages/Chat";
import Conversas from "../pages/Conversas";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/cadastroservico" element={<CadastroServico />} />
        <Route path="/servicos" element={<Servicos />} />
        <Route path="/contato" element={<Contato />} />
        <Route path="/descontos" element={<Descontos />} />
        <Route path="/parceiros" element={<Parceiros />} />
        <Route path="/painelusuario" element={<PainelUsuario />} />
        <Route path="/sobre" element={<Sobre />} />
        <Route path="/fazendas" element={<Fazendas />} />
        <Route path="/fazendaeditar/:id" element={<EditarFazenda />} />
        <Route path="/cadastrofazenda" element={<CadastroFazenda />} />
        <Route path="/servicoseditar/:id" element={<EditarServico />} />
        <Route path="/mensagemfaleconosco" element={<MensagemFaleConosco />} />
        <Route path="/chat/:idDestinatario" element={<Chat />} />
        <Route path="/conversas" element={<Conversas />} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;
