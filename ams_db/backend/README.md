 # Documentação do projeto
 # AMS Backend API

Este projeto é a API backend do sistema **AMS** (Agro Management System), construída com **Python + Flask**, **SQLAlchemy ORM**, banco de dados **MySQL**, e containerizada com **Docker**.

---

## 🚀 Tecnologias Utilizadas

- Python 3.11
- Flask
- Flask SQLAlchemy
- Pydantic (validação de dados)
- MySQL 8.0
- Docker
- Docker Compose
- Dotenv (variáveis de ambiente)

---

## 🗂️ Estrutura de Pastas

```bash
ams_db/
│
├── backend/
│   ├── controllers/   # Rotas da API
│   ├── services/      # Lógica de negócio
│   ├── schemas/       # Validação de entrada/saída
│   ├── models/        # ORM SQLAlchemy (tabelas)
│   ├── config/        # Configurações (session.py, database.py)
│   └── main.py        # Inicialização do Flask
│
├── Dockerfile
├── docker-compose.yml
├── .env
├── .env.local
├── .env.example
└── README.md
