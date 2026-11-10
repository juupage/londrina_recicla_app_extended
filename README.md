# ♻️ Recicla Londrina | Data Analytics & Interactive Dashboard

> Projeto acadêmico de Ciência de Dados voltado à análise, organização e visualização de dados relacionados à comercialização de materiais recicláveis por cooperativas.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com/)
[![Status](https://img.shields.io/badge/Status-Em_desenvolvimento-yellow?style=flat-square)]()

---

## 📋 Overview

O **Recicla Londrina** é um projeto acadêmico que aplica conceitos de Ciência de Dados para explorar informações relacionadas à cadeia de reciclagem e à atuação de cooperativas de materiais recicláveis.

A versão estendida apresenta uma aplicação interativa desenvolvida em Python e Streamlit, utilizando dados de comercialização de cooperativas para estruturar indicadores e facilitar a exploração das informações.

A proposta é transformar dados brutos em informações organizadas e visualizações acessíveis, contribuindo para a compreensão de aspectos econômicos e operacionais da reciclagem.

## 🎯 Project Goals

- Organizar e estruturar bases de dados relacionadas à reciclagem.
- Realizar limpeza, tratamento e padronização das informações.
- Desenvolver indicadores relacionados à comercialização de materiais recicláveis.
- Facilitar a exploração dos dados por meio de filtros interativos.
- Construir visualizações para apoiar a interpretação dos resultados.
- Promover o uso de dados como instrumento de transparência e compreensão da gestão de resíduos.

## ⚙️ Tech Stack

| Tecnologia | Finalidade |
|---|---|
| Python | Desenvolvimento e processamento |
| Pandas | Manipulação e tratamento de dados |
| Streamlit | Desenvolvimento da aplicação interativa |
| Plotly | Visualização e construção de gráficos |
| Git | Versionamento de código |
| GitHub | Gerenciamento e colaboração |

## 🗂️ Project Structure

```bash
londrina_recicla_extended/
│
├── app.py
├── dados_comercializacao_cooperativas.csv
├── requirements.txt
│
├── .streamlit/
│   └── config.toml
│
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Git
- Visual Studio Code (recomendado)

### Installation

Clone o repositório:

```bash
git clone https://github.com/juupage/londrina_recicla_app_extended.git
```

Acesse o diretório:

```bash
cd londrina_recicla_app_extended
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

### Running the Application

Execute o dashboard localmente:

```bash
python -m streamlit run app.py
```

A aplicação será disponibilizada no navegador, normalmente em:

```text
http://localhost:8501
```

## 📊 Data & Processing

O dashboard utiliza como base o arquivo:

`dados_comercializacao_cooperativas.csv`

A aplicação contempla alguns procedimentos de tratamento e validação, incluindo:

- Padronização de textos.
- Conversão de valores numéricos no formato brasileiro.
- Tratamento de informações financeiras ausentes.
- Identificação e sinalização de duplicidades exatas.
- Ocultação de informações como CNPJ e DANFE na tabela principal.

Também é possível substituir a base de dados por meio do uploader disponível na barra lateral da aplicação.

**Nota sobre os dados:** o projeto possui finalidade acadêmica e exploratória. A origem, a cobertura e o significado dos campos devem ser validados com a documentação da base antes da divulgação de conclusões.

## 🔄 Development Workflow

O desenvolvimento é realizado de forma colaborativa utilizando Git e GitHub.

Fluxo básico de contribuição:

```bash
# Atualizar o repositório local
git pull origin main

# Adicionar alterações
git add .

# Registrar alterações
git commit -m "feat: descrição da implementação"

# Enviar alterações
git push origin main
```

Para novas funcionalidades, recomenda-se utilizar branches e Pull Requests.

## 📊 Project Status

**Status atual:** Em desenvolvimento.

A versão estendida contempla uma aplicação interativa para exploração de dados de comercialização de cooperativas. Novas melhorias, análises e funcionalidades poderão ser incorporadas progressivamente.

## 🌐 Project Website

Acesse a aplicação:

[Recicla Londrina — Interactive Dashboard](https://dashboard-python-recicla-londrina-pr.streamlit.app/)

## 👩‍💻 Contributors

Projeto acadêmico desenvolvido colaborativamente por estudantes de Ciência de Dados.

- Júlia Ribeiro Montá
- Irys de Carvalho Rodrigues
- Denise Teodoro Ferreira
- Ana Carolina dos Santos Riodades
- Rebecca Brandão Fraiha

---

<p align="center">
  <strong>RECICLA LONDRINA</strong><br>
  Data Science • Data Analytics • Sustainability
</p>
