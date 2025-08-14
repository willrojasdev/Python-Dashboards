from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client
from dash_bootstrap_templates import ThemeSwitchAIO
import dash

# ==================== Configurações iniciais ====================
load_dotenv()

# Login supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
if not url or not key:
    raise ValueError("Variáveis SUPABASE_URL ou SUPABASE_KEY não foram carregadas.")
supabase = create_client(url, key)

# Import from folders/theme changer
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
app.scripts.config.serve_locally = True
server = app.server

# Styles
tab_card = {
    "padding": "5px",
    "min-width": "0",
    'height': '100%'
}

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top",
               "y":0.9,
               "xanchor":"left",
               "x":0.1,
               "title": {"text": None},
               "font": {"color": "white"},
               "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":10, "r":10, "t":10, "b":10}
}

config_graph={"displayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

# ==================== Tabelas ====================
# Criar tabela de datas
start_date = "2022-01-01"
end_date = pd.Timestamp.today() + pd.Timedelta(days=30)
df_datas = pd.DataFrame({"data": pd.date_range(start=start_date, end=end_date)})

# Criar colunas adicionais
df_datas["ano"] = df_datas["data"].dt.year
df_datas["mes"] = df_datas["data"].dt.month
df_datas["nome_mes"] = df_datas["data"].dt.strftime("%B").str.upper()
df_datas["dia_semana"] = df_datas["data"].dt.weekday + 1
df_datas["nome_semana"] = df_datas["data"].dt.strftime("%A")
df_datas["dia"] = df_datas["data"].dt.day
df_datas["mes_atual"] = df_datas["data"].apply(
    lambda x: "Mês Atual" if (x.year == pd.Timestamp.today().year and x.month == pd.Timestamp.today().month) else "Outros Meses"
)

# Função de importação de tabelas
def load_data_from_supabase(table: str) -> pd.DataFrame:
    path = f"{table}"
    res = supabase.table(path).select("*").execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

# Importando tabelas

df_veiculos = load_data_from_supabase("view_dados_veiculos")
df_pecas = load_data_from_supabase("view_tipos_pecas")
df_m2 = load_data_from_supabase("view_metro_quadrado")

df_PPLUG_Jarinu = load_data_from_supabase("apontamento_pplug_jarinu")
df_PPLUG_Mogi = load_data_from_supabase("apontamento_pplug_mogi")
df_metas = load_data_from_supabase("view_metas_producao")

# ==================== Tratamentos das tabelas ====================
# Substituição de valores
mapeamento_etapa = {
    'ACO': 'AÇO',
    'BUFFER-AUTOCLAVE': 'BUFFER AUTOCLAVE',
    'CORTE': 'CORTE PLANO',
    'CORTE-CURVO': 'CORTE CURVO',
    'CORTE-PACOTE': 'CORTE PACOTE',
    'FORNO-S': 'FORNO',
    'INSPECAO FINAL': 'INSPEÇÃO FINAL',
    'LAPIDACAO': 'LAPIDAÇÃO',
    'POLI': 'POLICARBONATO',
    'POS-FORNO': 'PÓS FORNO',
    'PREMONTAGEM': 'PRÉ MONTAGEM',
    'SINTERIZACAO': 'SINTERIZADO'
}
df_PPLUG_Jarinu['etapa'] = df_PPLUG_Jarinu['etapa'].replace(mapeamento_etapa)
df_PPLUG_Mogi['etapa'] = df_PPLUG_Mogi['etapa'].replace(mapeamento_etapa)

# Alterando o tipo das colunas
df_PPLUG_Jarinu['data'] = pd.to_datetime(df_PPLUG_Jarinu['data']).dt.date
df_PPLUG_Mogi['data'] = pd.to_datetime(df_PPLUG_Mogi['data']).dt.date

# ==================== Filtros ====================
# Opções


# Funções
# Função para criar as opções hierárquicas
def create_hierarchical_date_options(df_datas):
    options = []


# ==================== Layout ====================
app.layout = dbc.Container(children=[

    # Linha 1 - Cabeçalho
    dbc.Row([

        # TÍTULO
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Legend("ANÁLISE POR SETOR")
                ])
            ], style=tab_card)
        ], lg=2, md=3, sm=6),

        # DATA SELECIONADA
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Legend("ANÁLISE POR SETOR")
                ])
            ], style=tab_card)
        ], lg=2, md=3, sm=6),

        # DIA DA SEMANA SELECIONADO
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Legend("ANÁLISE POR SETOR")
                ])
            ], style=tab_card)
        ], lg=2, md=2, sm=6),

        # ÚLTIMA ATUALIZAÇÃO
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Legend("ANÁLISE POR SETOR")
                ])
            ], style=tab_card)
        ], lg=2, md=2, sm=6),

        # FILTRO DE DATA
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("DATA:", style={"font-weight": "bold", "margin-bottom": "10px"}),
                    dcc.Dropdown(
                        id="filtro_data_hierarquico",
                        options=[],
                        value=None,
                        multi=True,
                        placeholder="Selecione período...",
                        style={"font-size": "12px"}
                    ),
                    html.Hr(style={"margin": "10px 0"}),
                    html.Div(id="status_selecao_data", style={"font-size": "11px", "color": "#666"})
                ])
            ], style=tab_card)
        ], lg=4, md=4, sm=12)

    ], className='g-2', align='center', style={'margin-top': '7px', "bgcolor": "rgba(211,211,211,1)"}),

    # Linha 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='graph1', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # Linha 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='graph2', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

], fluid=True, style={'height': '100vh'})



# ==================== Callbacks ====================
@app.callback(
    Output("filtro_data_hierarquico", "options"),
    Input("filtro_data_hierarquico", "id")
)
def populate_hierarchical_options(_):
    return create_hierarchical_date_options(df_datas)

# Callback para processar seleções
@app.callback(
    Output("status_selecao_data", "children"),
    Input("filtro_data_hierarquico", "value")
)
def process_date_selection(selected_values):
    if not selected_values:
        return "Nenhuma data selecionada"
    
    # Processar diferentes tipos de seleção
    periods = []
    for value in selected_values:
        if value.startswith("current_"):
            periods.append("Mês Atual")
        elif value.startswith("year_"):
            year = value.split("_")[1]
            periods.append(f"Todo o ano de {year}")
        elif "_" in value and not value.startswith("current_"):
            year, month = value.split("_")
            month_name = df_datas[(df_datas["ano"] == int(year)) & 
                                 (df_datas["mes"] == int(month))]["nome_mes"].iloc[0]
            periods.append(f"{month_name}/{year}")
    
    return f"Selecionado: {', '.join(periods)}"

# ==================== Run server ====================
if __name__ == '__main__':
    app.run(debug=True, port=8050)