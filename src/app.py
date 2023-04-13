from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

df = pd.read_excel("Gas-prices-728.xlsx",sheet_name='PSV MW',usecols=["Data","BoM","BoW","Day ahead","WDNW","Month ahead",])
dff= pd.read_excel("Gas-prices-728.xlsx",sheet_name='TTF MW',usecols=["Data","BoM","BoW","Day ahead","WDNW","Month ahead",])
dfff=pd.merge(df,dff[["Data","BoM","BoW","Day ahead","WDNW","Month ahead"]],on='Data',how='right')
dfff.head()
dfff.rename(columns={'BoM_x': 'BoM_PSV', 'Day ahead_x': 'Day ahead_PSV','WDNW_x':'WDNW_PSV','Month ahead_x':'Month ahead_PSV','BoM_y': 'BoM_TTF', 'Day ahead_y': 'Day ahead_TTF','WDNW_y':'WDNW_TTF','Month ahead_y':'Month ahead_TTF'}, inplace=True)
#print(dfff[:10])

# DATA E ANNO

data_excel=dfff['Data']

anno=data_excel.dt.year
dfff["Anno1"]=anno

dfff.rename(columns={'Anno1':'Anno1','BoM_x': 'BoM_PSV', 'Day ahead_x': 'Day ahead_PSV','WDNW_x':'WDNW_PSV','Month ahead_x':'Month ahead_PSV','BoM_y': 'BoM_TTF', 'Day ahead_y': 'Day ahead_TTF','WDNW_y':'WDNW_TTF','Month ahead_y':'Month ahead_TTF'}, inplace=True)
Test= dfff.query('Anno1==2022')

print(Test)


app = Dash(__name__)
server = app.server


app.layout = html.Div(
    [
        html.H4("Gas Market Spot"),
        dcc.Graph(id="time-series-chart"),
        html.Div([
#SLIDER



            html.Div(id='slider-output-container')
                    ]),
        html.P("Select stock:"),


#DROPDOWN

        dcc.Dropdown(
            id="ticker",
            options=["BoM_PSV", "Day ahead_PSV","WDNW_PSV","Month ahead_PSV","BoM_TTF", "Day ahead_TTF","WDNW_TTF","Month ahead_TTF"],
            multi=True,
            value="Day ahead_PSV",
            clearable=False,
        ),
    ]
)


@app.callback(
    Output('time-series-chart','figure'),
    Input('ticker', 'value'),
   # Input('my_slider','value')
)


def display_time_series(ticker):
    fig = px.line(Test, x="Data", y=ticker)
    fig.update_xaxes(rangeslider_visible=True)


    #filtered_df = dfff[anno == my_slider]
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)