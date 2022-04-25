# general libraries
import numpy as np
import pandas as pd
import folium
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

data = pd.read_csv("areas_of_delivery_lat_longs.csv")
unique_states = data.State.unique()

def colorPicker(state_list):
        for state in state_list:
            if state == 'Maharashtra':
                return 'green'
            elif state == 'Gujarat':
                return 'blue'
            elif state == 'Tamilnadu':
                return 'orange'
            else:
                return 'red'

def generate_html(state_list):
        print(state_list)
        data = pd.read_csv("areas_of_delivery_lat_longs.csv")
        sanfran_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

        place = folium.map.FeatureGroup()
        data = data[data.State.isin(state_list)]
        print(data)

        for lat, lng in zip(data['Latitude'], data['Longitude']):
            place.add_child(
            folium.features.CircleMarker(
            [lat, lng],
            radius=5,
            color='yellow',
            fill=True,
            fill_color='red',
            fill_opacity=0.6
                     
           )
         )
                
        latitudes = list(data['Latitude'])
        longitudes = list(data['Longitude'])
        state = list(data.State)
        labels = list(data['Branch Name'])
        icon = folium.Icon(color='red', icon='info-sign')
        for lat, lng, label in zip(latitudes, longitudes, labels):
             folium.Marker([lat, lng], popup=label).add_to(sanfran_map) 
                
        for lat, lng, label, state in zip(latitudes, longitudes, labels, state):
            if state == 'Maharashtra':
                folium.Marker([lat, lng],
                    icon=folium.Icon(color='red'),
                    popup='Coming Soon',
                    Categoria=state
                ).add_to(sanfran_map)

        sanfran_map.fit_bounds([[data['Latitude'][i], data['Longitude'][i]]  for i in data.index])
        sanfran_map.add_child(place)
        # folium.GeoJson(style_function = lambda x: {'fillColor': colorPicker(state_list)},
        #        tooltip = folium.GeoJsonTooltip(fields=('State', 'Branch Name',),
        #                                        aliases=('State','Branch Name')),
        #        show = True).add_to(sanfran_map)

        return sanfran_map.save('{}.html'.format(state_list))


app.layout = html.Div([
    dcc.Dropdown(id="dropdown_state",options=[
            {'label': i, 'value': i} for i in unique_states
            ],placeholder="Choose State",
            multi=True,
            clearable=True,
            style={"width": "15vw", "height": "5vh", "fontSize": "1.1vw",
                   "marginTop": "5px", "marginLeft": "10px"}),
    html.Iframe(id='map',
            style={"width": "90vw", "height": "90vh", "fontSize": "1.1vw","marginTop": "15px", "marginLeft": "50px"})])


@app.callback(Output('map', 'srcDoc'),
              [Input('dropdown_state', 'value')])
def update_map(dropdown_state):
        print(dropdown_state)
        if dropdown_state is None or len(dropdown_state)<1:
                return open('presence_map.html','r').read()
        
        generate_html(dropdown_state)
        return open("{}.html".format(dropdown_state), 'r').read()

        
if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
