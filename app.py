from pathlib import Path
import re
import unicodedata

import pandas as pd
import plotly.express as px
import streamlit as st


# ------------------------------------------------------------
# CONFIGURAÇÃO
# ------------------------------------------------------------
st.set_page_config(
    page_title="Londrina Recicla | Comercialização",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

VERDE_ESCURO = "#14532D"
VERDE = "#16A34A"
VERDE_CLARO = "#86EFAC"
TURQUESA = "#2DD4BF"
AZUL = "#38BDF8"
AZUL_ESCURO = "#1D4ED8"
CINZA = "#64748B"
PALETA = [VERDE, TURQUESA, AZUL, VERDE_CLARO, AZUL_ESCURO, "#A3E635", "#0F766E"]

ARQUIVO_PADRAO = Path(__file__).parent / "dados_comercializacao_cooperativas.csv"


# ------------------------------------------------------------
# ESTILO
# ------------------------------------------------------------
st.markdown(
    f"""
    <style>
      .stApp {{
        background: #F7FAF8;
      }}
      [data-testid="stSidebar"] {{
        background: #F0F7F2;
        border-right: 1px solid #DCE9DF;
      }}
      h1, h2, h3 {{
        color: {VERDE_ESCURO};
      }}
      div[data-testid="stMetric"] {{
        background: #FFFFFF;
        border: 1px solid #DCE9DF;
        padding: 16px 18px;
        border-radius: 12px;
      }}
      div[data-testid="stMetricLabel"] p {{
        color: #475569;
      }}
      .subtle {{
        color: #64748B;
        font-size: 0.9rem;
      }}
      .section-note {{
        color: #64748B;
        font-size: 0.88rem;
        margin-top: -8px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# FUNÇÕES DE TRATAMENTO
# ------------------------------------------------------------
def normalizar_texto(valor):
    if pd.isna(valor):
        return None
    texto = re.sub(r"\s+", " ", str(valor)).strip().upper()
    return texto if texto else None


def converter_numero_br(valor):
    """Converte números em padrão brasileiro para float."""
    if pd.isna(valor):
        return None

    texto = str(valor).strip()
    if not texto or texto.lower() in {"nan", "none", "-"}:
        return None

    texto = texto.replace("R$", "").replace(" ", "")

    # Quando há vírgula, ela é considerada separador decimal.
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    # Sem vírgula: ponto com três casas à direita é tratado como milhar,
    # exceto quando o número começa com zero (ex.: 0.3).
    elif "." in texto:
        partes = texto.split(".")
        if len(partes) == 2 and len(partes[1]) == 3 and partes[0] != "0":
            texto = texto.replace(".", "")

    try:
        return float(texto)
    except (TypeError, ValueError):
        return None


def preparar_base(arquivo):
    df = pd.read_csv(arquivo, sep=None, engine="python", encoding="utf-8-sig")
    df.columns = df.columns.astype(str).str.strip()

    obrigatorias = [
        "COOPERATIVA",
        "MÊS DE EMISSÃO DA DANFE",
        "TIPO DE MATERIAL",
        "DESCRIÇÃO MATERIAL",
        "PESO (kg)",
        "VALOR UNITÁRIO (R$)",
        "TOTAL (R$)",
    ]
    faltantes = [col for col in obrigatorias if col not in df.columns]
    if faltantes:
        raise ValueError(
            "Não encontrei estas colunas obrigatórias: " + ", ".join(faltantes)
        )

    # Mantém uma cópia da base original para rastreabilidade.
    df["Cooperativa"] = df["COOPERATIVA"].map(normalizar_texto).fillna("NÃO INFORMADA")
    df["Comprador"] = (
        df["COMPRADOR"].map(normalizar_texto)
        if "COMPRADOR" in df.columns
        else "NÃO INFORMADO"
    )
    if isinstance(df["Comprador"], pd.Series):
        df["Comprador"] = df["Comprador"].fillna("NÃO INFORMADO")

    df["Tipo de material"] = (
        df["TIPO DE MATERIAL"].map(normalizar_texto).fillna("NÃO INFORMADO")
    )
    df["Descrição do material"] = (
        df["DESCRIÇÃO MATERIAL"].map(normalizar_texto).fillna("NÃO INFORMADA")
    )

    df["Data"] = pd.to_datetime(
        df["MÊS DE EMISSÃO DA DANFE"], dayfirst=True, errors="coerce"
    )
    df["Ano"] = df["Data"].dt.year
    df["Mês"] = df["Data"].dt.to_period("M").dt.to_timestamp()

    df["Peso (kg)"] = df["PESO (kg)"].map(converter_numero_br)
    df["Valor unitário (R$/kg)"] = df["VALOR UNITÁRIO (R$)"].map(converter_numero_br)
    df["Valor total (R$)"] = df["TOTAL (R$)"].map(converter_numero_br)

    # Campos auxiliares para visualização.
    df["Peso (ton)"] = df["Peso (kg)"] / 1000
    df["Valor por tonelada (R$/ton)"] = df["Valor unitário (R$/kg)"] * 1000

    return df


def moeda_br(valor):
    if pd.isna(valor):
        return "—"
    return (
        "R$ "
        + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )


def numero_br(valor, casas=0):
    if pd.isna(valor):
        return "—"
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def aplicar_layout(fig, titulo=None):
    fig.update_layout(
        template="plotly_white",
        title=titulo,
        colorway=PALETA,
        font=dict(family="Arial", color="#334155"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=55, b=25),
        legend_title_text="",
        hoverlabel=dict(bgcolor="white"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#E2E8F0", zeroline=False)
    return fig


def formatar_eixo_moeda(fig):
    fig.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
    return fig


# ------------------------------------------------------------
# CABEÇALHO
# ------------------------------------------------------------
st.title("♻️ Londrina Recicla")
st.subheader("Painel de comercialização de materiais recicláveis")
st.markdown(
    """
    Explore os registros de comercialização por período, cooperativa,
    comprador e categoria de material.
    """
)
st.caption(
    "Protótipo acadêmico de análise de dados. A visualização utiliza a base "
    "de comercialização disponibilizada para este projeto; confira as notas "
    "de qualidade e cobertura antes de interpretar os indicadores."
)


# ------------------------------------------------------------
# CARREGAMENTO DA BASE
# ------------------------------------------------------------
st.sidebar.header("Base de dados")
arquivo_upload = st.sidebar.file_uploader(
    "Substituir arquivo CSV",
    type=["csv"],
    help="Se não enviar outro arquivo, o aplicativo procura "
         "'dados_comercializacao_cooperativas.csv' na pasta do projeto.",
)

try:
    if arquivo_upload is not None:
        df = preparar_base(arquivo_upload)
        origem_base = arquivo_upload.name
    elif ARQUIVO_PADRAO.exists():
        df = preparar_base(ARQUIVO_PADRAO)
        origem_base = ARQUIVO_PADRAO.name
    else:
        st.warning(
            "O arquivo CSV não foi encontrado. Adicione "
            "'dados_comercializacao_cooperativas.csv' à pasta do app "
            "ou envie a base pelo campo da barra lateral."
        )
        st.stop()
except Exception as erro:
    st.error(f"Não foi possível carregar a base: {erro}")
    st.stop()

if df.empty:
    st.warning("A base não possui registros.")
    st.stop()

# Registros com data válida são necessários para os filtros temporais.
df = df[df["Data"].notna()].copy()
if df.empty:
    st.error("Não há datas válidas na coluna de emissão.")
    st.stop()

st.sidebar.caption(f"Arquivo em uso: {origem_base}")
st.sidebar.caption(f"{len(df):,} registros carregados".replace(",", "."))


# ------------------------------------------------------------
# FILTROS
# ------------------------------------------------------------
st.sidebar.divider()
st.sidebar.header("Filtros")

data_min = df["Data"].min().date()
data_max = df["Data"].max().date()
periodo = st.sidebar.date_input(
    "Período de emissão",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max,
    format="DD/MM/YYYY",
)

if isinstance(periodo, (tuple, list)) and len(periodo) == 2:
    inicio, fim = periodo
else:
    inicio = fim = periodo

cooperativas = sorted(df["Cooperativa"].dropna().unique().tolist())
materiais = sorted(df["Tipo de material"].dropna().unique().tolist())
compradores = sorted(df["Comprador"].dropna().unique().tolist())

sel_coop = st.sidebar.multiselect(
    "Cooperativa", cooperativas, placeholder="Todas as cooperativas"
)
sel_material = st.sidebar.multiselect(
    "Tipo de material", materiais, placeholder="Todos os materiais"
)
sel_comprador = st.sidebar.multiselect(
    "Comprador", compradores, placeholder="Todos os compradores"
)

df_filtrado = df[
    (df["Data"].dt.date >= inicio) & (df["Data"].dt.date <= fim)
].copy()

if sel_coop:
    df_filtrado = df_filtrado[df_filtrado["Cooperativa"].isin(sel_coop)]
if sel_material:
    df_filtrado = df_filtrado[df_filtrado["Tipo de material"].isin(sel_material)]
if sel_comprador:
    df_filtrado = df_filtrado[df_filtrado["Comprador"].isin(sel_comprador)]

if df_filtrado.empty:
    st.info("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()


# ------------------------------------------------------------
# INDICADORES GERAIS
# ------------------------------------------------------------
st.markdown("## Visão geral")
peso_total = df_filtrado["Peso (kg)"].sum(min_count=1)
valor_total = df_filtrado["Valor total (R$)"].sum(min_count=1)
qtd_registros = len(df_filtrado)
qtd_coops = df_filtrado["Cooperativa"].nunique()
qtd_compradores = df_filtrado.loc[
    df_filtrado["Comprador"] != "NÃO INFORMADO", "Comprador"
].nunique()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Peso comercializado", f"{numero_br(peso_total / 1000)} ton")
k2.metric("Valor registrado", moeda_br(valor_total))
k3.metric("Registros", numero_br(qtd_registros))
k4.metric("Cooperativas", numero_br(qtd_coops))
k5.metric("Compradores", numero_br(qtd_compradores))

st.caption(
    "Os totais financeiros consideram apenas registros com valor preenchido. "
    "O peso considera os registros com peso válido."
)


# ------------------------------------------------------------
# EVOLUÇÃO TEMPORAL
# ------------------------------------------------------------
st.markdown("---")
st.markdown("## Evolução ao longo do tempo")
st.markdown(
    '<p class="section-note">A série é agregada por mês de emissão da DANFE.</p>',
    unsafe_allow_html=True,
)

serie = (
    df_filtrado.groupby("Mês", as_index=False)
    .agg(
        **{
            "Peso (ton)": ("Peso (ton)", "sum"),
            "Valor total (R$)": ("Valor total (R$)", "sum"),
            "Registros": ("Data", "size"),
        }
    )
    .sort_values("Mês")
)

col1, col2 = st.columns(2)
with col1:
    fig_peso = px.line(
        serie,
        x="Mês",
        y="Peso (ton)",
        markers=True,
        title="Volume comercializado (toneladas)",
    )
    fig_peso.update_traces(line=dict(color=VERDE, width=3))
    st.plotly_chart(aplicar_layout(fig_peso), use_container_width=True)

with col2:
    serie_valor = serie.dropna(subset=["Valor total (R$)"])
    fig_valor = px.area(
        serie_valor,
        x="Mês",
        y="Valor total (R$)",
        title="Valor total registrado por mês",
    )
    fig_valor.update_traces(line=dict(color=TURQUESA), fillcolor="rgba(45,212,191,0.22)")
    formatar_eixo_moeda(fig_valor)
    st.plotly_chart(aplicar_layout(fig_valor), use_container_width=True)


# ------------------------------------------------------------
# MATERIAIS
# ------------------------------------------------------------
st.markdown("---")
st.markdown("## Perfil dos materiais")

material = (
    df_filtrado.groupby("Tipo de material", as_index=False)
    .agg(
        **{
            "Peso (ton)": ("Peso (ton)", "sum"),
            "Valor total (R$)": ("Valor total (R$)", "sum"),
            "Registros": ("Tipo de material", "size"),
        }
    )
    .sort_values("Peso (ton)", ascending=False)
)

c1, c2 = st.columns(2)
with c1:
    fig_material = px.pie(
        material,
        names="Tipo de material",
        values="Peso (ton)",
        hole=0.55,
        title="Participação por tipo de material (peso)",
        color_discrete_sequence=PALETA,
    )
    fig_material.update_traces(textposition="inside", textinfo="percent")
    st.plotly_chart(aplicar_layout(fig_material), use_container_width=True)

with c2:
    fig_material_valor = px.bar(
        material.sort_values("Valor total (R$)", ascending=True),
        x="Valor total (R$)",
        y="Tipo de material",
        orientation="h",
        title="Valor registrado por tipo de material",
        color="Tipo de material",
        color_discrete_sequence=PALETA,
    )
    formatar_eixo_moeda(fig_material_valor)
    fig_material_valor.update_layout(showlegend=False)
    st.plotly_chart(aplicar_layout(fig_material_valor), use_container_width=True)

st.markdown("### Detalhamento por descrição")
descricao = (
    df_filtrado.groupby(
        ["Tipo de material", "Descrição do material"], as_index=False
    )
    .agg(
        **{
            "Peso (ton)": ("Peso (ton)", "sum"),
            "Valor total (R$)": ("Valor total (R$)", "sum"),
            "Registros": ("Descrição do material", "size"),
        }
    )
    .sort_values("Peso (ton)", ascending=False)
)
st.dataframe(
    descricao,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Peso (ton)": st.column_config.NumberColumn(format="%.2f ton"),
        "Valor total (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
        "Registros": st.column_config.NumberColumn(format="%d"),
    },
)


# ------------------------------------------------------------
# COOPERATIVAS E COMPRADORES
# ------------------------------------------------------------
st.markdown("---")
st.markdown("## Cooperativas e compradores")

coop = (
    df_filtrado.groupby("Cooperativa", as_index=False)
    .agg(
        **{
            "Peso (ton)": ("Peso (ton)", "sum"),
            "Valor total (R$)": ("Valor total (R$)", "sum"),
            "Registros": ("Cooperativa", "size"),
        }
    )
    .sort_values("Peso (ton)", ascending=False)
)

comprador = (
    df_filtrado[df_filtrado["Comprador"] != "NÃO INFORMADO"]
    .groupby("Comprador", as_index=False)
    .agg(
        **{
            "Peso (ton)": ("Peso (ton)", "sum"),
            "Valor total (R$)": ("Valor total (R$)", "sum"),
            "Registros": ("Comprador", "size"),
        }
    )
    .sort_values("Valor total (R$)", ascending=False)
)

c3, c4 = st.columns(2)
with c3:
    top_coop = coop.head(10).sort_values("Peso (ton)", ascending=True)
    fig_coop = px.bar(
        top_coop,
        x="Peso (ton)",
        y="Cooperativa",
        orientation="h",
        title="Top 10 cooperativas por volume",
        color="Peso (ton)",
        color_continuous_scale=["#BBF7D0", VERDE_ESCURO],
    )
    st.plotly_chart(aplicar_layout(fig_coop), use_container_width=True)

with c4:
    top_comprador = comprador.head(10).sort_values("Valor total (R$)", ascending=True)
    fig_comprador = px.bar(
        top_comprador,
        x="Valor total (R$)",
        y="Comprador",
        orientation="h",
        title="Top 10 compradores por valor registrado",
        color="Valor total (R$)",
        color_continuous_scale=["#BAE6FD", AZUL_ESCURO],
    )
    formatar_eixo_moeda(fig_comprador)
    st.plotly_chart(aplicar_layout(fig_comprador), use_container_width=True)

c5, c6 = st.columns(2)
with c5:
    st.markdown("### Ranking de cooperativas")
    st.dataframe(
        coop,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Peso (ton)": st.column_config.NumberColumn(format="%.2f ton"),
            "Valor total (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
            "Registros": st.column_config.NumberColumn(format="%d"),
        },
    )
with c6:
    st.markdown("### Ranking de compradores")
    st.dataframe(
        comprador,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Peso (ton)": st.column_config.NumberColumn(format="%.2f ton"),
            "Valor total (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
            "Registros": st.column_config.NumberColumn(format="%d"),
        },
    )


# ------------------------------------------------------------
# PREÇO MÉDIO POR MATERIAL
# ------------------------------------------------------------
st.markdown("---")
st.markdown("## Valores unitários por material")
precos = (
    df_filtrado.dropna(subset=["Valor unitário (R$/kg)"])
    .groupby("Tipo de material", as_index=False)
    .agg(
        **{
            "Preço médio (R$/kg)": ("Valor unitário (R$/kg)", "mean"),
            "Preço mediano (R$/kg)": ("Valor unitário (R$/kg)", "median"),
            "Registros com preço": ("Valor unitário (R$/kg)", "count"),
        }
    )
    .sort_values("Preço médio (R$/kg)", ascending=False)
)
if not precos.empty:
    fig_preco = px.bar(
        precos,
        x="Tipo de material",
        y="Preço médio (R$/kg)",
        color="Tipo de material",
        color_discrete_sequence=PALETA,
        title="Preço médio registrado por quilograma",
        hover_data=["Preço mediano (R$/kg)", "Registros com preço"],
    )
    fig_preco.update_layout(showlegend=False)
    st.plotly_chart(aplicar_layout(fig_preco), use_container_width=True)
    st.caption(
        "O preço médio é calculado a partir dos valores unitários preenchidos. "
        "Ele não representa necessariamente uma cotação atual de mercado."
    )
else:
    st.info("Não há valores unitários preenchidos para os filtros selecionados.")


# ------------------------------------------------------------
# EXPLORAÇÃO DOS REGISTROS
# ------------------------------------------------------------
st.markdown("---")
st.markdown("## Explorar registros")
st.markdown(
    '<p class="section-note">CNPJ e número de DANFE não são exibidos nesta tabela.</p>',
    unsafe_allow_html=True,
)

colunas_exibicao = [
    "Data",
    "Cooperativa",
    "Comprador",
    "Tipo de material",
    "Descrição do material",
    "Peso (kg)",
    "Valor unitário (R$/kg)",
    "Valor total (R$)",
]
tabela = df_filtrado[colunas_exibicao].sort_values("Data", ascending=False)
st.dataframe(
    tabela,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Data": st.column_config.DateColumn(format="DD/MM/YYYY"),
        "Peso (kg)": st.column_config.NumberColumn(format="%.2f kg"),
        "Valor unitário (R$/kg)": st.column_config.NumberColumn(format="R$ %.2f"),
        "Valor total (R$)": st.column_config.NumberColumn(format="R$ %.2f"),
    },
)

csv_export = tabela.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
st.download_button(
    "⬇️ Baixar registros filtrados (CSV)",
    data=csv_export,
    file_name="londrina_recicla_registros_filtrados.csv",
    mime="text/csv",
)


# ------------------------------------------------------------
# QUALIDADE E LIMITAÇÕES DA BASE
# ------------------------------------------------------------
st.markdown("---")
with st.expander("Qualidade e cobertura dos dados", expanded=False):
    original_total = len(df)
    sem_comprador = int((df["Comprador"] == "NÃO INFORMADO").sum())
    sem_preco = int(df["Valor unitário (R$/kg)"].isna().sum())
    sem_valor = int(df["Valor total (R$)"].isna().sum())
    duplicados = int(df.duplicated().sum())
    sem_danfe = (
        int(df["DANFE"].isna().sum()) if "DANFE" in df.columns else None
    )

    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Sem comprador", numero_br(sem_comprador))
    q2.metric("Sem preço unitário", numero_br(sem_preco))
    q3.metric("Sem valor total", numero_br(sem_valor))
    q4.metric("Linhas duplicadas exatas", numero_br(duplicados))

    if sem_danfe is not None:
        st.write(f"Registros sem DANFE preenchida: **{numero_br(sem_danfe)}**.")

    st.write(
        f"Período identificado na base: **{data_min.strftime('%d/%m/%Y')} a "
        f"{data_max.strftime('%d/%m/%Y')}**."
    )
    st.write(
        "Os registros duplicados foram mantidos nesta versão, pois não é "
        "possível afirmar apenas pela igualdade das colunas se representam "
        "duplicidade de lançamento ou transações distintas."
    )
    st.write(
        "Os campos financeiros ausentes são ignorados nas somas e médias "
        "(não são convertidos em zero)."
    )
    st.write(
        "A padronização de texto é aplicada para consolidar diferenças de "
        "maiúsculas/minúsculas e espaços; os dados originais permanecem no CSV."
    )


# ------------------------------------------------------------
# RODAPÉ
# ------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div class="subtle">
      <b>Londrina Recicla</b> · Protótipo acadêmico de visualização e análise de dados.<br>
      Referência institucional: CMTU-LD ·
      <a href="https://sites.google.com/cmtuld.com.br/londrina-recicla"
         target="_blank">Londrina Recicla</a>
    </div>
    """,
    unsafe_allow_html=True,
)
