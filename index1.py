from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash()
df = pd.read_excel("BaseFuncionarios.xlsx", sheet_name="Plan1")

func_por_area = df["Área"].value_counts().reset_index()
func_por_area.columns = ["Area", "Quantidade"]

fig1 = px.bar(func_por_area, x="Area", y="Quantidade", title="Funcionários por Área")

func_por_sexo = df["Genero"].value_counts().reset_index()
func_por_sexo.columns = ["Genero", "Quantidade"]

fig2 = px.pie(func_por_sexo, names="Genero", values="Quantidade",title="Homes vs Mulheres")

fig3 = px.histogram(df, x="Salario", nbins=20, title="Distribuição de Salários")

fig4 = px.box(df, x="Área", y="Salario", title="Distribuição de Salários por Área")

df["Ano_Contratacao"] = pd.DatetimeIndex(df["Data de Contratacao"]).year
contratacoes_por_ano = df["Ano_Contratacao"].value_counts().sort_index().reset_index()
contratacoes_por_ano.columns = ["Ano", "Quantidade"]

fig5 = px.line(contratacoes_por_ano, x="Ano", y="Quantidade", title="Contratações por Ano")

app.layout = html.Div(children=[
   html.H1(style={"text-align": "center"},children="Dashboard De RH"),
   
   html.Div(style={"display": "flex", "gap": "20px", "padding": "20px"}, children=[
       dcc.Graph(
        id="grafico-barra",
        figure=fig1,
        style={"flex": "1"}
      ),
      
      dcc.Graph(
       id="grafico-pizza",
       figure=fig2,
       style={"flex": "1"}
      )     
    ]),
    
    html.Div(style={"display": "flex", "gap": "20px", "padding": "20px"},
    children=[
       dcc.Graph(
          id="grafico-histograma",
          figure=fig3,
          style={"flex": "1"}
         ),
         
         dcc.Graph(
             id="grafico-box",
             figure=fig4,
             style={"flex": "1"}
           )
      ]),
      
      dcc.Graph(
          id="grafico-linha",
          figure=fig5
        )
  ])

if __name__ == "__main__":
  app.run(debug=True)