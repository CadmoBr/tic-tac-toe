# Jogo da Velha

Exemplo educativo de aplicação web containerizada para ensino de DevOps.

## Tech Stack

- **Frontend:** Streamlit (Python)
- **Container:** Docker

## Rodando Localmente

### Com Docker Compose

```bash
docker-compose up --build
# Acesse: http://localhost:8501
```

### Directamente com Python

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura do Projeto

```
├── app.py              # Aplicação Streamlit
├── requirements.txt    # Dependências Python
├── Dockerfile         # Imagem Docker
└── docker-compose.yml # Composição local
```

## Funcionalidades

- ✅ Jogo vs Humano (2 jogadores)
- ✅ Jogo vs Bot (IA simples)
- ✅ Placar persistente
- ✅ Interface interativa
