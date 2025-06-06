function SidebarDestaques({ onFiltrarCategoria }) {
  const categorias = [
    "Todos os Serviços",
    "Agrônomo",
    "Consultoria",
    "Serviço Agrícola",
    "Tecnologia",
    "Transporte",
    "Veterinário",
    "Outros",
  ];

  return (
    <aside className="hidden lg:block w-64 p-4 bg-green-700 text-white rounded-lg shadow-lg min-h-[650px] -mt-32">
      <h2 className="text-xl font-bold mb-6 text-center">DESTAQUES</h2>
      <ul className="space-y-3">
        {categorias.map((item, index) => (
          <li
            key={index}
            onClick={() => onFiltrarCategoria(item === "Todos os Serviços" ? "" : item)}
            className="bg-green-600 hover:bg-green-500 px-6 py-3 rounded-lg cursor-pointer transition text-base text-center font-medium"
          >
            {item}
          </li>
        ))}
      </ul>
    </aside>
  );
}

export default SidebarDestaques;
