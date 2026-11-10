LONDRINA RECICLA — VERSÃO ESTENDIDA

Arquivos:
- app.py: aplicação Streamlit
- dados_comercializacao_cooperativas.csv: base utilizada pelo aplicativo
- requirements.txt: dependências
- .streamlit/config.toml: tema visual

Como executar:
1. Coloque todos os arquivos na pasta do projeto.
2. Instale as dependências:
   python -m pip install -r requirements.txt
3. Execute:
   python -m streamlit run app.py

A aplicação procura automaticamente o arquivo:
dados_comercializacao_cooperativas.csv

Também é possível substituir a base pelo uploader na barra lateral.

Observações:
- A aplicação padroniza textos e converte números no formato brasileiro.
- CNPJ e DANFE não aparecem na tabela principal.
- Registros sem valor financeiro não são contabilizados como R$ 0,00.
- Duplicidades exatas são sinalizadas, mas não removidas automaticamente.
- O dashboard é um protótipo acadêmico; valide a origem, a cobertura e o significado
  dos campos com a documentação da base antes de publicar conclusões.
