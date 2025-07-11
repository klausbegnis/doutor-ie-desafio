# Solução Desafio Técnico Doutor-IE

**Autor:** [@klausbegnis](https://github.com/klausbegnis)

## Descrição do Problema

Este projeto implementa uma API de busca semântica que permite realizar consultas em documentos utilizando embeddings e similaridade de cosseno. O sistema é capaz de processar perguntas dos usuários e retornar as respostas mais relevantes baseadas no conteúdo indexado.

## Proposta da Solução

### Ferramentas escolhidas

A API foi desenvolvida com FastAPI e utiliza:
- **PostgreSQL** com extensão pgvector para armazenamento de embeddings
- **Sentence Transformers** (modelo [multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large)) para geração de embeddings
- **SQLModel** para mapeamento objeto-relacional
- **Docker** para containerização e orquestração dos serviços

### API

Para o desenvolvimento da API, segui-se o padrão de criação de [APIRouters](https://fastapi.tiangolo.com/reference/apirouter/) que implementam cada endpoint da aplicação. Com a classe [FastAPI](https://fastapi.tiangolo.com/reference/fastapi/) cria-se de fato a aplicação e são adicionados todos os routers desenvolvidos. Além disso, utilizou-se de lifespan para definir inicialização correta da aplicação e também injeção de dependências, de modo a utilizar sessões ou métodos definidos sem a necessidade de reimplementação de código.

Para a modelagem dos objetos, utilizou-se a biblioteca pydantic para poder compartilhar entre diversas partes do código especificaçãoes de tipos de dados. Isso permitiu facilmente integrar o endpoint desenvolvido com a segementação semântica.

### RAG

A estratégia de segmentação semântica utilizada foi projetada para otimizar a precisão do sistema de busca RAG (Retrieval-Augmented Generation). Inicialmente, o conteúdo de cada documento foi dividido em blocos autocontidos, usando os marcadores de tópico (linhas iniciadas com "-") como delimitadores. Em seguida, cada bloco foi segmentado em duas partes distintas: a linha do tópico foi extraída como a "pergunta" pesquisável, e o texto subsequente foi definido como o "payload" (a resposta completa). Para a vetorização, a abordagem final e mais eficaz foi concatenar a "pergunta" e o "payload", gerando um único embedding a partir do texto combinado. Este método cria um vetor denso e rico em contexto para cada chunk, garantindo que a busca por similaridade capture nuances e detalhes específicos, o que melhora drasticamente a relevância dos documentos recuperados. Este resultado foi obtido a partir de intensos testes de adequação, a estratégia inicial foi de apenas separar cada linha em chunks separados, apenas para fins de testes de integração.

## Estrutura do Projeto

Para desenvolver este projeto, segui-se as recomendações fornecidas pela [FastAPI - Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#an-example-file-structure), de modo a permitir fácil integração com projetos existentes que utilize este mesmo framework.

```
doutor-ie-api/
├── src/
│   ├── datamodels/           # Modelos de dados Pydantic/SQLModel
│   │   ├── consulta_models.py
│   │   └── embedded_model.py
│   ├── dependencies/         # Dependências de injeção
│   │   └── postgre_depedency.py
│   ├── embeddings/          # Módulo de embeddings
│   │   └── embedder.py
│   ├── lifespan/            # Configuração de inicialização
│   │   └── postgre_startup.py
│   ├── routes/              # Rotas da API
│   │   └── consulta_router.py
│   ├── main.py              # Aplicação principal
│   └── env.py               # Variáveis de ambiente
├── docker/                  # Configurações Docker
│   ├── grafana/
│   │   └── compose.yaml
│   └── postgre/
│       └── compose.yaml
├── data/                    # Dados de origem
│   ├── funcionalidades_plataforma_doutorie.txt
│   └── quem-somos.txt
├── Dockerfile
├── README.md
└── requirements.txt
```

## Endpoints da API

### POST /consulta

Realiza uma busca semântica baseada na pergunta fornecida.

**Request Body:**
```json
{
  "question": "string"
}
```

**Response:**
```json
{
  "docs": [
    {
      "payload": "string",
      "sources": [
        {
          "id": "string",
          "url": "string"
        }
      ]
    }
  ]
}
```

## Modelos de Dados

### Consulta
Modelo para receber perguntas do usuário:
```python
class Consulta(BaseModel):
    question: str
```

### Embedded
Modelo de dados para armazenamento no banco:
```python
class Embedded(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    source_id: int = Field(index=True)
    url: str
    question: str
    payload: str
    embedding: Annotated[list[float], Field(sa_column=Column(Vector(1024)))]
```

### ResponseItems
Modelo para itens de resposta:
```python
class ResponseItems(BaseModel):
    payload: str
    sources: list[SourceItem]
```

### SourceItem
Modelo para fontes de dados:
```python
class SourceItem(BaseModel):
    id: str
    url: str
```

### Response
Modelo de resposta final:
```python
class Response(BaseModel):
    docs: list[ResponseItems]
```

## Como Utilizar

### Pré-requisitos
- Docker
- Docker Compose

### Executando os Serviços

1. **Iniciar PostgreSQL:**
```bash
cd docker/postgre
docker-compose up -d
```

2. **Iniciar Grafana (opcional):**
```bash
cd docker/grafana
docker-compose up -d
```

3. **Construir e executar a API:**
```bash
# Construir a imagem
docker build -t doutor-ie-api .

# Executar o container na mesma rede dos outros serviços
docker run -d --network doutor_ie_desafio -p 8081:8081 doutor-ie-api
```

### Testando a API

```bash
curl -X POST "http://localhost:8081/consulta" \
-H "Content-Type: application/json" \
-d '{"question": "Qual é a missão da Doutor-IE?"}'
```

## Funcionalidades Técnicas

### Embeddings
- Utiliza o modelo `intfloat/multilingual-e5-large` para geração de embeddings
- Suporte a textos em português
- Otimização através de prefixos de task ("passage" e "query")

### Banco de Dados
- PostgreSQL com extensão pgvector
- Busca por [similaridade de cosseno](https://en.wikipedia.org/wiki/Cosine_similarity)
- Indexação automática de embeddings
- Limitação de 2 resultados mais relevantes por consulta

### Inicialização Automática
- Criação automática de tabelas
- Processamento e indexação de documentos na inicialização
- Verificação de duplicatas antes da inserção

## Rede Docker

Todos os containers executam na mesma rede Docker (`doutor_ie_desafio`), permitindo comunicação entre serviços através de nomes de containers:

- **PostgreSQL:** `postgresql:5432`
- **API:** `doutor-ie-api:8081`
- **Grafana:** `grafana:3000`

## Fontes de Dados

O sistema indexa automaticamente os seguintes documentos:
- `data/funcionalidades_plataforma_doutorie.txt`
- `data/quem-somos.txt`

## Conclusões e Aprimoramentos

### Implementado
- API REST funcional com FastAPI
- Busca semântica com embeddings
- Armazenamento vetorial com PostgreSQL + pgvector
- Containerização com Docker
- Inicialização automática de dados

### Possíveis Melhorias
- Implementar cache de embeddings
- Adicionar autenticação e autorização
- Implementar logging estruturado
- Implementar monitoramento com Grafana

### Maiores desafios

Criação da estratégia de segmentação semântica e adequação do modelo para resultados ótimos.

## Tecnologias Utilizadas

- **FastAPI** - Framework web
- **SQLModel** - ORM e validação de dados
- **PostgreSQL** - Banco de dados
- **pgvector** - Extensão para vetores
- **Sentence Transformers** - Geração de embeddings
- **Docker** - Containerização
- **Pydantic** - Validação de dados