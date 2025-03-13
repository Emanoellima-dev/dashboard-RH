from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash_bootstrap_templates import ThemeSwitchAIO

# temas
url_theme1 = dbc.themes.VAPOR
url_theme2 = dbc.themes.FLATLY
template_theme1 = "vapor"
template_theme2 = "flatly"

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_excel("BaseFuncionarios.xlsx", sheet_name="Plan1")

# qtde de funcionarios por cidade
func_por_cidade = df["Cidade"].value_counts().reset_index()
func_por_cidade.columns = ["Cidade", "qtde de Funcionarios"]

# qtde de Funcionarioa por cargo
func_por_cargo = df["Cargo"].value_counts().reset_index()
func_por_cargo.columns = ["Cargo", "qtde de Funcionarios"]

# qtde Funcionarios por area
func_por_area = df["Área"].value_counts().reset_index()
func_por_area.columns = ["Area", "qtde de Funcionarios"]

# Contratação anual
df["Ano_Contratacao"] = pd.DatetimeIndex(df["Data de Contratacao"]).year
contratacoes_por_ano = df["Ano_Contratacao"].value_counts().sort_index().reset_index()
contratacoes_por_ano.columns = ["Ano", "Quantidade"]

#  qtde de funcionarios por sexo
func_por_sexo = df["Genero"].value_counts().reset_index()
func_por_sexo.columns = ["Genero", "Quantidade"]

# layout
app.layout = dbc.Container([
    dbc.Row([
      dbc.Col([
         html.H1("Dashboard De RH", style={"text-align": "center", "font-weight": "bold"}),
         
         ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
         
         dcc.Dropdown(
           id="dropdown",
           options=[
             {"label": "Cidade", "value": "Cidade"},
             {"label": "Cargo", "value": "Cargo"},
             {"label": "Area", "value": "Area"}
            ],
            value="Cidade",
            style={"color": "black", "background-color": "#2b1042"}
           ),
           dcc.Graph(id="graf-bar")
        ])
      ]),
      
    dbc.Row([
      dbc.Col([
        dcc.Graph(
           id="line-graph"
           )
         ]),
         
        dbc.Col([
         dcc.Graph(
            id="graf-pizza"
           )
          ])
      ])
  ], fluid=True)
  
  
@app.callback(
   Output("graf-bar", "figure"),
   Output("line-graph", "figure"),
   Output("graf-pizza", "figure"),
   Input("dropdown", "value"),
   Input(ThemeSwitchAIO.ids.switch("theme"), "value")
  )

def update_graph(value, toggle):
  template = template_theme1 if toggle else template_theme2
  
  fig1 = px.bar(func_por_cidade, x="Cidade", y="qtde de Funcionarios", title="Quantidade De Funcionarios Por Cidade", template=template)
  
  fig2 = px.bar(func_por_area, x="Area", y="qtde de Funcionarios", title="Quantidade De funcionarios Por Area", template=template)
  
  fig3 = px.bar(func_por_cargo, x="Cargo", y="qtde de Funcionarios", title="Quantidade De Funcionarios Por Cargo", template=template)
  
  fig4 = px.line(contratacoes_por_ano, x="Ano", y="Quantidade", title="Contratações por Ano", template=template)
      
  fig5 = px.pie(func_por_sexo, names="Genero", values="Quantidade",title="Homes vs Mulheres", hole=0.5, template=template)
  
  if value == "Cidade":
      return [fig1, fig4, fig5]
      
  elif value == "Area":
    return [fig2, fig4, fig5]
    
  else:
    return [fig3, fig4, fig5]
    
if __name__ == "__main__":
  app.run(debug=False, port=8050)
