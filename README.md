# Desafio DevSecOps - LacreiSaúde

Desafio realizado como parte do desafio técnico de **DevSecOps da LacreiSaúde**, com o objetivo de implementar uma aplicação web simples, com foco em testes automatizados, segurança, containerização e CI/CD.

A aplicação consiste em uma API desenvolvida com **FastAPI**, executada em um container Docker e disponibilizada através de uma VM do Google Compute Engine.

A pipeline de CI/CD é executada através do **GitHub Actions**, realizando automaticamente testes, build da imagem, análise de segurança com OWASP ZAP, publicação das imagens no Docker Hub e Artifact Registry e deploy na própria máquina após uma alteração no código.

# Sobre o projeto

A aplicação possui uma interface web simples com dois endpoints:

* `/`: página inicial da aplicação, com acesso ao endpoint `/status`;
* `/status`: página utilizada para verificar se a aplicação está funcionando corretamente.

# Funcionalidades

* Endpoint de status da aplicação;
* Documentação automática através do Swagger;
* Testes automatizados com Pytest;
* Containerização utilizando Docker;
* Pipeline CI/CD com GitHub Actions;
* Análise de segurança com OWASP ZAP;
* Publicação da imagem no Google Artifact Registry;
* Publicação da imagem no Docker Hub;
* Deploy automático em uma VM do Google Compute Engine;
* Versionamento das imagens utilizando o SHA do commit;
* Autenticação do GitHub Actions no GCP através de Workload Identity Federation.

# Arquitetura

O fluxo implementado no projeto é:

```text
                         ┌─────────────────┐
                         │     GitHub      │
                         │   Repository    │
                         └────────┬────────┘
                                  │
                                  │ Push
                                  ▼
                      ┌───────────────────────┐
                      │    GitHub Actions     │
                      │                       │
                      │  • Pytest             │
                      │  • Docker Build       │
                      │  • API Validation     │
                      │  • OWASP ZAP          │
                      │  • Registry Push      │
                      │  • Deploy             │
                      └───────────┬───────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  │                               │
                  ▼                               ▼
       ┌─────────────────────┐          ┌─────────────────┐
       │ Google Artifact      │          │    Docker Hub   │
       │ Registry             │          │                 │
       │                     │          │ lacreisaudeapi  │
       └──────────┬──────────┘          └─────────────────┘
                  │
                  │ Pull
                  ▼
       ┌─────────────────────────┐
       │ Google Compute Engine   │
       │                         │
       │ VM: lacreisaude-api     │
       └────────────┬────────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Docker Container  │
          │                   │
          │ FastAPI :8000     │
          └─────────┬─────────┘
                    │
                    ▼
             ┌──────────────┐
             │   Usuário    │
             │              │
             │ HTTP :8000   │
             └──────────────┘
```

# Tecnologias utilizadas

## Aplicação

* Python 3.12
* FastAPI
* Uvicorn
* Pytest
* HTTPX

## Containerização

* Docker
* Docker Hub
* Google Artifact Registry

## CI/CD

* GitHub Actions

## Segurança

* OWASP ZAP
* GitHub Secrets
* Google Cloud Workload Identity Federation
* Google Cloud IAM
* OS Login
* Identity-Aware Proxy (IAP)

## Cloud

* Google Cloud Platform
* Google Compute Engine
* Google Artifact Registry

# Rastreabilidade e rollback

Cada imagem publicada recebe uma tag baseada no SHA do commit, permitindo identificar exatamente qual versão foi utilizada em determinado deploy.

Exemplo:

```text
lacreisaudeapi:a1b2c3d...
```

Isso facilita a rastreabilidade das versões e permite realizar um rollback manual para uma imagem anterior caso necessário.

# Segurança no Pipeline

Um dos principais objetivos do projeto foi evitar o uso de credenciais estáticas para autenticação do GitHub Actions no Google Cloud.

Para isso, foi utilizado **Workload Identity Federation**.

## Workload Identity Federation

O GitHub Actions autentica no Google Cloud utilizando **OIDC + Workload Identity Federation**.

Dessa forma, não é necessário armazenar uma chave JSON de Service Account dentro do GitHub.

Fluxo:

```text
GitHub Actions
      │
      │ OIDC Token
      ▼
Workload Identity Federation
      │
      ▼
Google Cloud IAM
      │
      ▼
Service Account
```

Isso reduz o risco associado ao armazenamento e possível vazamento de credenciais estáticas.

# Controle de permissões

Foi aplicado controle de acesso utilizando IAM.

A Service Account utilizada pelo GitHub Actions possui as permissões necessárias para:

* Publicar imagens no Artifact Registry;
* Acessar a VM através do fluxo utilizado pelo deploy;
* Utilizar OS Login;
* Utilizar IAP;
* Realizar a operação necessária sobre a Service Account da VM.

A VM possui permissão de leitura do Artifact Registry para conseguir baixar as imagens utilizadas no deploy.

# Restrição do Workload Identity

O Workload Identity Provider foi configurado para aceitar somente o repositório:

```text
ErickBortoloti/lacreisaudedevsecops
```

Isso restringe a utilização dessa identidade federada ao repositório utilizado no projeto.

# Secrets

As credenciais utilizadas para publicação no Docker Hub não ficam armazenadas diretamente no código.

São configuradas como **GitHub Secrets**:

```text
DOCKER_HUB_USER
DOCKER_HUB_TOKEN
```

As informações relacionadas ao projeto GCP utilizadas pelo workflow são armazenadas como **GitHub Variables**.

# OWASP ZAP

O pipeline utiliza **OWASP ZAP** para realizar uma análise de segurança da aplicação.

O scan é executado contra a aplicação iniciada dentro do ambiente do GitHub Actions:

```text
http://localhost:8000
```

O objetivo é identificar possíveis vulnerabilidades através de testes automatizados de segurança.

O resultado do scan é disponibilizado como artefato do workflow.

# Executando localmente

## 1. Clonar o projeto

```bash
git clone https://github.com/ErickBortoloti/lacreisaudedevsecops.git

cd lacreisaudedevsecops
```

## 2. Criar ambiente virtual

```bash
python3 -m venv .venv
```

## 3. Ativar

Linux:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

## 4. Instalar dependências

```bash
pip install -r requirements.txt
```

## 5. Executar os testes

```bash
pytest
```

## 6. Executar a aplicação

```bash
uvicorn app.main:app --reload
```

A aplicação estará disponível em:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

# Docker

Para criar a imagem:

```bash
docker build -t lacreisaudeapi .
```

Para executar:

```bash
docker run -d \
  --name lacreisaude-api \
  -p 8000:8000 \
  lacreisaudeapi
```

Para validar:

```bash
curl http://localhost:8000/status
```

# Endpoints

| Endpoint  | Descrição                          |
| --------- | ---------------------------------- |
| `/`       | Página inicial da aplicação        |
| `/status` | Verificação do status da aplicação |
| `/docs`   | Documentação Swagger               |

# Deploy

O deploy é realizado automaticamente através do GitHub Actions.

Após um `push` na branch `main`, o pipeline executa:

1. Testes automatizados;
2. Build da imagem Docker;
3. Inicialização e validação da API;
4. Scan de segurança com OWASP ZAP;
5. Push da imagem para o Artifact Registry;
6. Push da imagem para o Docker Hub;
7. Deploy da imagem na VM do Google Compute Engine;
8. Health check do endpoint `/status`.

A imagem utilizada no deploy é identificada pelo SHA do commit, garantindo maior rastreabilidade entre código, imagem e ambiente.
