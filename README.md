# OrganizaAí Estudos

Aplicação web em **Python + Streamlit** para planejamento automático de estudos de universitários.

O sistema permite:

- Cadastro de usuário com login e senha;
- Cadastro de disciplinas;
- Cadastro de horários livres da rotina;
- Cadastro de atividades acadêmicas, como provas, trabalhos e listas;
- Geração automática de cronograma semanal;
- Recalcular cronograma;
- Exportar cronograma em PDF;
- Armazenamento dos dados em PostgreSQL externo no Render.

## Estrutura do projeto

```text
organizaai_streamlit/
├── app.py
├── requirements.txt
├── database/
├── repositories/
├── services/
├── utils/
├── pages/
└── .streamlit/secrets.toml.example
```

## Como rodar localmente

1. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/Mac:

```bash
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie o arquivo de segredos:

```bash
mkdir .streamlit
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
```

No Linux/Mac:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

4. Edite `.streamlit/secrets.toml` e coloque a URL externa do PostgreSQL do Render:

```toml
DATABASE_URL = "postgresql://usuario:senha@host/banco?sslmode=require"
```

5. Rode o projeto:

```bash
streamlit run app.py
```

## Como publicar no Streamlit Cloud

1. Suba este projeto para o GitHub.
2. Não suba o arquivo `.streamlit/secrets.toml`.
3. No Streamlit Cloud, vá em **App settings > Secrets**.
4. Cadastre:

```toml
DATABASE_URL = "sua_url_externa_do_postgresql_render"
```

5. Publique usando `app.py` como arquivo principal.

## Observação de segurança

A senha do banco de dados e a URL real do Render devem ficar apenas no **Streamlit Secrets** ou em variável de ambiente. Não coloque a URL real diretamente no código nem no GitHub.
