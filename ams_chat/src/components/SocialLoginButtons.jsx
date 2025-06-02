function SocialLoginButtons() {
    return (
      <div className="flex flex-col space-y-3 mt-6">
        {/* Botão Google */}
        <button className="flex items-center justify-center gap-2 w-full bg-white border border-gray-300 text-sm font-medium text-gray-700 py-2 rounded-lg shadow-sm hover:bg-gray-100 transition">
          <img src="/icons/google.png" alt="Google" className="h-5 w-5" />
          <span>Entrar com Google</span>
        </button>
  
        {/* Botão Facebook */}
        <button className="flex items-center justify-center gap-2 w-full bg-white border border-gray-300 text-sm font-medium text-gray-700 py-2 rounded-lg shadow-sm hover:bg-gray-100 transition">
          <img src="/icons/facebook.png" alt="Facebook" className="h-5 w-5" />
          <span>Entrar com Facebook</span>
        </button>
  
        {/* Botão LinkedIn */}
        <button className="flex items-center justify-center gap-2 w-full bg-white border border-gray-300 text-sm font-medium text-gray-700 py-2 rounded-lg shadow-sm hover:bg-gray-100 transition">
          <img src="/icons/linkedin.png" alt="LinkedIn" className="h-5 w-5" />
          <span>Entrar com LinkedIn</span>
        </button>
      </div>
    );
  }
  
  export default SocialLoginButtons;
  