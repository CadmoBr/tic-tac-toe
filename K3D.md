# k3d - Cluster Kubernetes local (WSL2)

Guia de uso do [k3d](https://k3d.io/) (k3s rodando em containers Docker) para desenvolver e testar este projeto localmente, dentro do WSL2.

## Pré-requisitos

```bash
docker --version
k3d version
kubectl version --client
```

## Criar o cluster (com a porta do Ingress já publicada)

```bash
k3d cluster create residencia --agents 2 -p "8080:80@loadbalancer"
```

Formato da flag `-p`/`--port`: `[HOST:][HOSTPORT:]CONTAINERPORT[/PROTOCOL]@NODEFILTER`

- `8080` = porta no host (Windows/WSL2)
- `80` = porta do Ingress dentro do container `serverlb`
- `@loadbalancer` = aplica o mapeamento no `serverlb`, que é quem roteia para o Traefik/Ingress

Se também quiser expor o NodePort (`30080` no `service.yaml`) diretamente, sem passar pelo Ingress:

```bash
k3d cluster create residencia --agents 2 -p "8080:80@loadbalancer" -p "30080:30080@server:0"
```

## Aplicar os manifests do projeto

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Verificar status

```bash
kubectl get pods -l app=tic-tac-toe
kubectl get svc tic-tac-toe-service
kubectl get ingress
```

## Acessar a aplicação

- Via Ingress (com a porta publicada acima): http://localhost:8080/
- Alternativa, sem depender de porta publicada no k3d:
  ```bash
  kubectl port-forward svc/tic-tac-toe-service 8080:8080
  ```
  e acessar http://localhost:8080/ enquanto o comando roda em primeiro plano.

## Corrigir um cluster já existente sem a porta publicada

Se o cluster já foi criado sem a flag `-p` (pods/Service/Ingress aparecem OK no `kubectl`, mas o navegador não conecta), dá para adicionar a porta sem recriar o cluster:

```bash
k3d cluster edit residencia --port-add "8080:80@loadbalancer"
```

## Comandos úteis do dia a dia

```bash
k3d cluster list                     # listar clusters e status do loadbalancer
k3d cluster stop residencia          # parar o cluster
k3d cluster start residencia         # subir de novo
k3d cluster delete residencia        # apagar
k3d image import <imagem> -c residencia   # levar uma imagem local para dentro do cluster
kubectl config get-contexts
kubectl config use-context k3d-residencia
```

## Troubleshooting: "os manifests estão OK mas o navegador não acessa"

Sintoma: `kubectl get pods/svc/ingress` mostra tudo certo (pods `Running`, Service, Ingress configurados), mas `http://localhost:...` não conecta.

Causa mais comum: o container `serverlb` do k3d não tem a porta publicada para o host. Diagnóstico:

```bash
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

Se a linha do `k3d-<cluster>-serverlb` mostrar `80/tcp` **sem** um `0.0.0.0:PORTA->80/tcp`, a porta não foi publicada — nada está escutando naquele endereço no host (isso não é um problema de encaminhamento WSL2 ↔ Windows, é ausência de publicação de porta no Docker).

Fix:

```bash
k3d cluster edit <cluster> --port-add "HOSTPORT:80@loadbalancer"
```

Depois, confirmar com `docker ps` que a porta aparece publicada e testar:

> **Nota:** o `k3d cluster edit --port-add` pode reportar `FATA[...] Failed to update the cluster: ... Rolled back` mesmo quando a porta acaba sendo publicada com sucesso (o container novo do `serverlb` sobe e assume a porta antes do rollback ser efetivado). Se isso acontecer, rode `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"` para checar o estado real do `serverlb` antes de tentar de novo — rodar o comando repetidamente pode falhar com `address already in use` por causa de processos `docker-proxy` órfãos da tentativa anterior que ainda seguram a porta.

```bash
curl -o /dev/null -w "%{http_code}\n" http://localhost:HOSTPORT/
```
