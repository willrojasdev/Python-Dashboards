from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Login supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
if not url or not key:
    raise ValueError("Variáveis SUPABASE_URL ou SUPABASE_KEY não foram carregadas.")
supabase = create_client(url, key)

from dash_bootstrap_templates import ThemeSwitchAIO
import dash

# Import from folders/theme changer
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
app.scripts.config.serve_locally = True
server = app.server

# Styles
tab_card = {'height': '100%'}

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

# Função de importação de tabelas
def load_data_from_supabase(table: str) -> pd.DataFrame:
    path = f"{table}"
    res = supabase.table(path).select("*").execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

# Importando tabelas
df_veiculos = load_data_from_supabase("view_dados_veiculos")
df_pecas = load_data_from_supabase("view_tipos_pecas")
df_m2 = load_data_from_supabase("view_metro_quadrado")


# ========== Tratamentos das tabelas ==========



# ========== Filtros ==========
# Opções


# Funções



# ========== Layout ==========
app.layout = dbc.Container(children=[], fluid=True, style={'height': '100vh'})



# ========== Callbacks ==========



# ========== Run server ==========
if __name__ == '__main__':
    app.run(debug=False, port=8050)