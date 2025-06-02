import Header from "../components/Header";
import Footer from "../components/Footer";

function Sobre() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      {/* Banner */}
      <section
        className="h-[60vh] bg-cover bg-center flex flex-col items-center justify-center text-white text-center px-4"
        style={{ backgroundImage: "url('/bg.jpg')" }}
      >
        <h1 className="text-3xl sm:text-5xl font-bold text-white bg-black/40 px-6 py-3 rounded shadow-lg">
          CONHEÇA A NOSSA HISTÓRIA
        </h1>
      </section>

      {/* Título */}
      <div className="text-center py-6 bg-white text-xl font-bold text-green-800 shadow">
        PROJETO ACADÊMICO AMS - AGRO MARKET SERVICE
      </div>

      {/* Conteúdo da história */}
      <section className="bg-white px-6 py-8 text-justify max-w-4xl mx-auto text-gray-700 leading-relaxed">
        <p>
          O projeto <strong>AMS - Agro Market Service</strong> nasceu no contexto de um desafio acadêmico,
          com o objetivo de criar uma plataforma digital que conectasse pequenos e médios produtores rurais a
          consumidores urbanos, promovendo o comércio justo, valorização da agricultura local e dando visibiladade
          aos produtores e prestadores de serviços do agronegócio.
        </p>
        <p className="mt-4">
          Desenvolvido por estudantes dedicados, o AMS busca não apenas facilitar o acesso a produtos
          e serviços, mas também fomentar a economia regional, aproximando campo e cidade
          através da tecnologia. Este sistema é fruto de pesquisa, colaboração e inovação aplicada à
          realidade do agronegócio brasileiro.
        </p>
        <p className="mt-4">
          Durante sua concepção, o projeto foi estruturado com base em metodologias ágeis e ferramentas
          modernas de desenvolvimento web, priorizando a experiência do usuário, a escalabilidade e o
          impacto social positivo.
        </p>
      </section>

      <Footer />
    </div>
  );
}

export default Sobre;
