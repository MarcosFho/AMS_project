import { Link } from "react-router-dom";

function Footer() {
  return (
    <footer className="bg-green-700 text-white py-8 mt-10">
      <div className="max-w-6xl mx-auto px-4 flex flex-col items-center md:flex-row md:justify-between gap-6">
        {/* Logo e nome */}
        <div className="flex items-center space-x-3">
          <img src="/logo.png" alt="Logo AMS" className="h-10" />
          <span className="text-xl font-bold">AMS</span>
        </div>



        {/* Redes sociais */}
        <div className="flex space-x-4">
          <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">
            <img src="/icons/facebook.png" alt="Facebook" className="h-6 w-6" />
          </a>
          <a href="https://instagram.com" target="_blank" rel="noopener noreferrer">
            <img src="/icons/instagram.png" alt="Instagram" className="h-6 w-6" />
          </a>
          <a href="https://wa.me/5599999999999" target="_blank" rel="noopener noreferrer">
            <img src="/icons/whatsapp.png" alt="WhatsApp" className="h-6 w-6" />
          </a>
        </div>
      </div>

      <p className="text-center text-xs text-white-400 mt-6">
        © {new Date().getFullYear()} AMS - Agro Market Service. Todos os direitos reservados.
      </p>
    </footer>
  );
}

export default Footer;
