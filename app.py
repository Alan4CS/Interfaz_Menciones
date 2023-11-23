from db_data_menciones import menciones_database
from db_data_menciones_general import menciones_general__database
import dash
from dash import html, dcc, Output, Input, dash_table
import pandas as pd
from dash.exceptions import PreventUpdate
import time

# ------------------ Funciones --------------------



# ------------------- Main ----------------


app = dash.Dash(__name__)

df,opciones_usuario = menciones_database()

df_general = menciones_general__database()

interval_time = 120000
# ------------------------------- Dash ------------------------------------------------------- 

# Estilo para los Dropdowns
dropdown_style = {
    'width': '80%',
    'borderRadius': '10px',
    'color': '#000000',
}


app.layout = html.Div([
    html.H1("DashBoard Menciones-Twitter Scraper",style={"textAlign": "center", "color": "black" }),
    html.H2("Pool",style={'padding': '10px'}),
    html.Div( id='tabla-users-general', style={'padding': '20px'} ),
    dcc.Dropdown(
        id='dropdown-usuario',
        options=opciones_usuario,
        value=None,
        placeholder="Selecciona un usuario",
        style=dropdown_style
    ),
    dcc.Loading(
        id="loading-data",
        type="default",
        children=[
            html.Div(id='tabla-menciones-general',style={'padding':'20px'}),
            html.Div(id='tabla-menciones-container', style={'padding': '20px'}),
        ],
    ),
    dcc.Interval(
                    id='interval-component',
                    interval=interval_time,  # Intervalo de actualización
                    n_intervals=0
                ),
], style={
    'background': 'linear-gradient(to bottom, #87CEEB, #ADD8E6)', 
    'height': '180vh',
    'overflow': 'auto'
})

@app.callback(
    Output('tabla-menciones-general', 'children'),
    Output('tabla-menciones-container','children'),
    Input('dropdown-usuario', 'value')
)
def actualizar_pagina(selected_user):
    df,opciones_usuario = menciones_database()

    df_general = menciones_general__database()

    if selected_user is not None:

        filtered_df_general = df_general[df_general['usuario_twitter'] == selected_user].copy()
        # Filtrar el DataFrame por el usuario seleccionado
        filtered_df = df[df['usuario_twitter'] == selected_user].copy()  # Copia el DataFrame filtrado

        menciones_general__table = dash.dash_table.DataTable(
            columns=[
                {'name': col, 'id': col} for col in filtered_df_general.columns
            ],
            data=filtered_df_general.to_dict('records'),
            style_table={'width': '100%', 'margin': '10px auto'},
            style_cell={'padding': '10px', 'textAlign': 'left', 'whiteSpace': 'normal', 'color': 'black'},
            style_header={'backgroundColor': 'lightgrey'}
        )

        for index, row in filtered_df.iterrows():
            filtered_df.at[index, 'link_mencion'] = f"[Ver mención]({row['link_mencion']})"

        # Crear una tabla Dash para mostrar las menciones
        menciones_table = dash_table.DataTable(
            columns=[
                {'name': 'Mención', 'id': 'mencion'},
                {'name': 'Usuario mención', 'id': 'user_mencion'},
                {'name': 'sentimiento', 'id': 'sentimiento'},
                {'name': 'Link mención', 'id': 'link_mencion','presentation': 'markdown'},
                {'name': 'Fecha mención', 'id': 'fecha_mencion'},
            ],
            data=filtered_df.to_dict('records'),
            style_table={'width': '100%', 'margin': '10px auto'},
            style_cell={'padding': '10px', 'textAlign': 'left', 'whiteSpace': 'normal', 'color': 'black'},
            style_header={'backgroundColor': 'lightgrey'},
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                                {
                    'if': {'column_id': 'sentimiento', 'filter_query': '{sentimiento} eq "POS"'},
                    'backgroundColor': '#4CAF50',
                    'color': 'white'
                },
                {
                    'if': {'column_id': 'sentimiento', 'filter_query': '{sentimiento} eq "NEU"'},
                    'backgroundColor': 'gray',
                    'color': 'black'
                },
                {
                    'if': {'column_id': 'sentimiento', 'filter_query': '{sentimiento} eq "NEG"'},
                    'backgroundColor': 'red',
                    'color': 'white'
                },
            ],
        )
        return menciones_general__table,menciones_table  # html.Div() se utiliza para eliminar el contador de tiempo de la página
    else:
        return html.Div(),html.Div()

# Callback para recargar la página
@app.callback(Output('interval-component', 'disabled'),
              Output('dropdown-usuario', 'options'),
               Output('tabla-users-general', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    
    if n is None:
        raise PreventUpdate
    
    # Imprime el tiempo actual para verificar
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"Recargando la página a las {current_time}")

    df,opciones_usuario = menciones_database()

    df_general =  menciones_general__database()

    # Crear la tabla
    table = dash_table.DataTable(
        id='tabla',
        columns=[
            {'name': 'Usuario', 'id': 'usuario_twitter'},
            {'name': 'Total Menciones', 'id': 'total_menciones'},
            {'name': 'Menciones Positivas', 'id': 'menciones_positivas'},
            {'name': 'Menciones Negativas', 'id': 'menciones_negativas'},
            {'name': 'Menciones Neutras', 'id': 'menciones_neutras'}
        ],
        data=df_general.to_dict('records'),
        style_table={'width': '100%'},
        style_cell={'textAlign': 'left'},
        style_header={'backgroundColor': 'lightgrey'},
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}
        ],
    )
    
    return False,opciones_usuario,[table]


if __name__ == '__main__':
    app.run(debug=True,port=8055)


