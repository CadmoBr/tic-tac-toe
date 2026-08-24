# Jogo da Velha - Exemplo Kubernetes

Exemplo educativo de aplicação web containerizada para ensino de DevOps.

## Tech Stack

- **Frontend:** Streamlit (Python)
- **Container:** Docker
- **Orquestração:** Kubernetes

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

## Deploy no Kubernetes

### 1. Build da imagem

```bash
docker build -t tic-tac-toe:latest .
```

### 2. Aplicar manifests

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
# Opcional:
kubectl apply -f k8s/ingress.yaml
```

### 3. Verificar status

```bash
kubectl get pods -l app=tic-tac-toe
kubectl get svc tic-tac-toe-service
```

## Estrutura do Projeto

```
├── app.py              # Aplicação Streamlit
├── requirements.txt    # Dependências Python
├── Dockerfile         # Imagem Docker
├── docker-compose.yml # Composição local
└── k8s/
    ├── deployment.yaml  # Deployment K8s
    ├── service.yaml     # Service K8s
    └── ingress.yaml     # Ingress K8s (opcional)
```

## Funcionalidades

- ✅ Jogo vs Humano (2 jogadores)
- ✅ Jogo vs Bot (IA simples)
- ✅ Placar persistente
- ✅ Interface interativa
- ✅ Health checks para Kubernetes
