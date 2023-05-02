import dash
#import dash_html_components as html
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import time
import os, json
import dash_table
import pyarrow.parquet as pq
from PIL import Image

Azuloscuro='#1f2c56'
CardBackground = "White"
PaperBackground = 'White'
Texclaro= 'White'
TextOscuro = 'Black'
Total_txt= "#7FDBFF"
Resolved_txt = "#ff9705"
Bluelight="#7FDBFF"

app = dash.Dash(__name__, meta_tags = [{"name": "viewport", "content": "width=device-width"}])

markdown_text = '''
### Help
Please contact : Big Data Team'''

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'backgroundColor': '#242a44',
    'color': Texclaro,
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#b5b5b5',
    'color': 'Black',
    'padding': '6px'
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "height": "100%",
    'textColor':Texclaro,
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 0.5rem",
    "background-color": Azuloscuro,
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
#    "background-color": "#f8f9fa",
}# Create dict of list

CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "16rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
#    "background-color": "#f8f9fa",
}
def make_clickable(row):
    return '[{}]({})'.format(row["URL"], row["URL"])

def clean_alt_list(list_):
    list_ = list_.replace(', ', '","')
    list_ = list_.replace('[', '["')
    list_ = list_.replace(']', '"]')
    return list_

def drop_duplicates(row):
    # Split string by ', ', drop duplicates and join back.
    words = row.split('; ')
    return ', '.join(np.unique(words).tolist())
def match_filter(mdata, team, match):
    #print(type(match))
    if (team!='All')&(match!='All'):
        match_data = mdata[((mdata['home_team.home_team_name'] == team) | (mdata['away_team.away_team_name'] == team)) & (mdata['match_id']==match)]
    elif (team!='All')&(match=='All'):
        match_data = mdata[((mdata['home_team.home_team_name'] == team) | (mdata['away_team.away_team_name'] == team))]
    elif (team=='All')&(match!='All'):
        match_data = mdata[(mdata['match_id']==match)]
    elif (team=='All')&(match=='All'):
        match_data = mdata       
    return match_data

def datafilter_report(datos, team, typo, match, possession, player, outcome, pass_shot):
    if (team!='All')&(typo!='All')&(match!='All')&(possession!='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['match_id']==match) & (datos['possession'] == possession) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo!='All')&(match!='All')&(possession!='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['match_id']==match) & (datos['possession'] == possession) & (datos['player.name'] == player)]
    elif (team!='All')&(typo!='All')&(match!='All')&(possession!='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['match_id']==match) & (datos['possession'] == possession) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo!='All')&(match!='All')&(possession!='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['match_id']==match) & (datos['possession'] == possession)]
    elif (team!='All')&(typo!='All')&(match!='All')&(possession=='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['match_id']==match) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo!='All')&(match!='All')&(possession=='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['match_id']==match) & (datos['player.name'] == player)]
    elif (team!='All')&(typo!='All')&(match!='All')&(possession=='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['match_id']==match) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo!='All')&(match!='All')&(possession=='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['match_id']==match)]
    elif (team!='All')&(typo!='All')&(match=='All')&(possession!='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['possession'] == possession) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo!='All')&(match=='All')&(possession!='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['possession'] == possession) & (datos['player.name'] == player)]
    elif (team!='All')&(typo!='All')&(match=='All')&(possession!='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['possession'] == possession) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo!='All')&(match=='All')&(possession!='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['possession'] == possession)]
    elif (team!='All')&(typo!='All')&(match=='All')&(possession=='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo!='All')&(match=='All')&(possession=='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['player.name'] == player)]
    elif (team!='All')&(typo!='All')&(match=='All')&(possession=='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo!='All')&(match=='All')&(possession=='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['type.name'] == typo)]
    elif (team!='All')&(typo=='All')&(match!='All')&(possession!='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['match_id']==match) & (datos['possession'] == possession) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo=='All')&(match!='All')&(possession!='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['match_id']==match) & (datos['possession'] == possession) & (datos['player.name'] == player)]
    elif (team!='All')&(typo=='All')&(match!='All')&(possession!='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['match_id']==match) & (datos['possession'] == possession) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo=='All')&(match!='All')&(possession!='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['match_id']==match) & (datos['possession'] == possession)]
    elif (team!='All')&(typo=='All')&(match!='All')&(possession=='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['match_id']==match) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo=='All')&(match!='All')&(possession=='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['match_id']==match) & (datos['player.name'] == player)]
    elif (team!='All')&(typo=='All')&(match!='All')&(possession=='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['match_id']==match) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo=='All')&(match!='All')&(possession=='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['match_id']==match)]
    elif (team!='All')&(typo=='All')&(match=='All')&(possession!='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['possession'] == possession) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo=='All')&(match=='All')&(possession!='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['possession'] == possession) & (datos['player.name'] == player)]
    elif (team!='All')&(typo=='All')&(match=='All')&(possession!='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['possession'] == possession) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo=='All')&(match=='All')&(possession!='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['possession'] == possession)]
    elif (team!='All')&(typo=='All')&(match=='All')&(possession=='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo=='All')&(match=='All')&(possession=='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team) & (datos['player.name'] == player)]
    elif (team!='All')&(typo=='All')&(match=='All')&(possession=='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['team.name'] == team) &  (datos['shot.outcome.name'] == outcome)]
    elif (team!='All')&(typo=='All')&(match=='All')&(possession=='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['team.name'] == team)]
    elif (team=='All')&(typo!='All')&(match!='All')&(possession!='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['match_id']==match) & (datos['possession'] == possession) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo!='All')&(match!='All')&(possession!='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['match_id']==match) & (datos['possession'] == possession) & (datos['player.name'] == player)]
    elif (team=='All')&(typo!='All')&(match!='All')&(possession!='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['match_id']==match) & (datos['possession'] == possession) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo!='All')&(match!='All')&(possession!='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['match_id']==match) & (datos['possession'] == possession)]
    elif (team=='All')&(typo!='All')&(match!='All')&(possession=='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['match_id']==match) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo!='All')&(match!='All')&(possession=='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['match_id']==match) & (datos['player.name'] == player)]
    elif (team=='All')&(typo!='All')&(match!='All')&(possession=='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['match_id']==match) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo!='All')&(match!='All')&(possession=='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['match_id']==match)]
    elif (team=='All')&(typo!='All')&(match=='All')&(possession!='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['possession'] == possession) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo!='All')&(match=='All')&(possession!='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['possession'] == possession) & (datos['player.name'] == player)]
    elif (team=='All')&(typo!='All')&(match=='All')&(possession!='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['possession'] == possession) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo!='All')&(match=='All')&(possession!='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['possession'] == possession)]
    elif (team=='All')&(typo!='All')&(match=='All')&(possession=='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo!='All')&(match=='All')&(possession=='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['player.name'] == player)]
    elif (team=='All')&(typo!='All')&(match=='All')&(possession=='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['type.name'] == typo) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo!='All')&(match=='All')&(possession=='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['type.name'] == typo)]
    elif (team=='All')&(typo=='All')&(match!='All')&(possession!='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['match_id']==match) & (datos['possession'] == possession) & (datos['player.name'] == player)]
    elif (team=='All')&(typo=='All')&(match!='All')&(possession!='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['match_id']==match) & (datos['possession'] == possession) & (datos['player.name'] == player)]
    elif (team=='All')&(typo=='All')&(match!='All')&(possession!='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['match_id']==match) & (datos['possession'] == possession) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo=='All')&(match!='All')&(possession!='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['match_id']==match) & (datos['possession'] == possession)]
    elif (team=='All')&(typo=='All')&(match!='All')&(possession=='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['match_id']==match) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo=='All')&(match!='All')&(possession=='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['match_id']==match) & (datos['player.name'] == player)]
    elif (team=='All')&(typo=='All')&(match!='All')&(possession=='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['match_id']==match) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo=='All')&(match!='All')&(possession=='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['match_id']==match)]
    elif (team=='All')&(typo=='All')&(match=='All')&(possession!='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['possession'] == possession) & (datos['player.name'] == player) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo=='All')&(match=='All')&(possession!='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['possession'] == possession) & (datos['player.name'] == player)]
    elif (team=='All')&(typo=='All')&(match=='All')&(possession!='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['possession'] == possession) & (datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo=='All')&(match=='All')&(possession!='All')&(player=='All')&(outcome=='All'):
        filtered_opt=datos[(datos['possession'] == possession)]
    elif (team=='All')&(typo=='All')&(match=='All')&(possession=='All')&(player!='All')&(outcome!='All'):
        filtered_opt=datos[(datos['player.name'] == player)&(datos['shot.outcome.name'] == outcome)]
    elif (team=='All')&(typo=='All')&(match=='All')&(possession=='All')&(player!='All')&(outcome=='All'):
        filtered_opt=datos[(datos['player.name'] == player)]
    elif (team=='All')&(typo=='All')&(match=='All')&(possession=='All')&(player=='All')&(outcome!='All'):
        filtered_opt=datos[(datos['shot.outcome.name'] == outcome)]
    else:
        filtered_opt=datos
    return filtered_opt

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

colors = [Resolved_txt, "#dd1e35", "green", "#e55467"]
color_discrete={'Complete':'PaleGreen',
                 'Analyze':Resolved_txt,
                 'Verify Source':"#8080ff",
                 'New':"#dd1e35",
                 'Idea':"Pink",
                 'On-Hold':'#e55467',
                 'Request CV Data':'Aqua',
                 'Requirement': "#e55467",
                 'To Do':"#ff8000",
                 'In Progress':"green",
                 'Closed':"white",
                 'Goal': 'Red',
                 'Post': 'Green'}



try:
    Match=pd.read_csv('matchesDf.csv',sep=',', na_values=' ')
    events=pq.read_table('eventsDf_V7_newFormat.parquet').to_pandas()
    img = Image.open('Football_field.svg.png') #my background image
    print('From NAS')
except:
    Match=pd.read_csv('matchesDf.csv',sep=',', na_values=' ')
    events=pq.read_table('eventsDf_V7_newFormat.parquet').to_pandas()
    img = Image.open('Football_field.svg.png') #my background image
    print('From GIT')

events['gol_x']=events['gol_x'].astype(float)
events['gol_y']=events['gol_y'].astype(float)
events['gol_z']=events['gol_z'].astype(float)
events['loc_x']=events['loc_x'].astype(float)
events['loc_y']=events['loc_y'].astype(float)
events['match_id']=events['match_id'].astype(int)
events['match_id']=events['match_id'].astype(int)
events['shot.statsbomb_xg']=events['shot.statsbomb_xg'].fillna(0)

Total_home_team=pd.concat([Match['home_team.home_team_name'],Match['away_team.away_team_name']]).unique()
optionslist_teams=[{'label': i, 'value': i} for i in Total_home_team]
optionslist_teams.insert(0,{'label': 'All', 'value': 'All'})
Total_type=events['type.name'].unique()
optionslist_type=[{'label': i, 'value': i} for i in Total_type]
optionslist_type.insert(0,{'label': 'All', 'value': 'All'})
Total_Match=Match['match_id'].unique()
optionslist_Match=[{'label': i, 'value': i} for i in Total_Match]
optionslist_Match.insert(0,{'label': 'All', 'value': 'All'})
Total_possession=events['possession'].unique()
optionslist_possession=[{'label': i, 'value': i} for i in Total_possession]
optionslist_possession.insert(0,{'label': 'All', 'value': 'All'})
Total_player=events['player.name'].unique()
optionslist_player=[{'label': i, 'value': i} for i in Total_player]
optionslist_player.insert(0,{'label': 'All', 'value': 'All'})

Total_outcome=events['shot.outcome.name'].unique()
optionslist_outcome=[{'label': i, 'value': i} for i in Total_outcome]
optionslist_outcome.insert(0,{'label': 'All', 'value': 'All'})



sidebar = html.Div(
    [
        #dcc.Button(id='show_hide'),
        html.H3("Filters", className="lead", style = {"color": Texclaro, "textAlign": "center"}),
        html.Hr(),
        #html.P(children ="VPSE Team Only: ", style = {"color": Texclaro}),
        #dcc.RadioItems( id='CPDI_ONLY', options=[{'label':'Yes', 'value':'Yes'}, {'label':'No', 'value':'No'},], value='No', style ={"color":Texclaro}, labelStyle={'display':'inline-block'}),
        #html.Hr(),
        html.P(
            children = "Team: ",
            style = {"color": Texclaro}
            ),
        dcc.Dropdown(
            id = "dropdown_team",
            multi = False,
            searchable = True,
            value = "All",
            clearable=False,
            disabled= False,
            options=optionslist_teams,
            className = "dcc_compon"
        ),
        html.P(
            children = "Event Type: ",
            style = {"color": Texclaro}
        ),
        dcc.Dropdown(
            id='dropdown_type',
            options=optionslist_type,
            value='All',
            clearable=False,
            searchable=False,
        ),

        html.P(
            children = "Match: ",
            style = {"color": Texclaro}
        ),
        dcc.Dropdown(
            id='dropdown_match',
            options=optionslist_Match,
                value='All',
                multi = False,
                clearable=True,
                searchable = True,
            ),
        html.P(
            children = "Possession: ",
            style = {"color": Texclaro}
        ),
        dcc.Dropdown(
            id='dropdown_possession',
            options=optionslist_possession,
                value='All',
                clearable=False,
                searchable=False,
            ),
        html.P(
            children = "Player: ",
            style = {"color": Texclaro}
        ),
        dcc.Dropdown(
            id='dropdown_player',
            options=optionslist_player,
                value='All',
                clearable=False,
                searchable=True,
            ),
        html.P(
            children = "Outcome: ",
            style = {"color": Texclaro}
        ),
   		dcc.Dropdown(
        		id = "dropdown_shot_outcome_name",
        		multi = False,
        		searchable = True,
        		value = "All",
                clearable=False,
                options=optionslist_outcome,
                className = "dcc_compon"
        	),
        html.Hr(),       
        html.Footer(
        className="mr-6"),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

# Instanciate the app
app = dash.Dash(__name__, meta_tags = [{"name": "viewport", "content": "width=device-width"}])
#server = app.server

def server_layout():

    return html.Div([
    html.Div(
    			children = [
    				# Logo
    				html.Div(
    					children = [
    					],
    					className = "one column"
    				),
    				html.Div(
    					children = [
    						# Title and subtitle
    						html.Div(
    							children = [
    								html.H3(
    									children = "Football Data Analytics",
    									style = {
    										"margin-bottom": "0",
                                            "textAlign": "center",
            								"color": TextOscuro
    									}
    								),
    								html.H5(
    									children = "Track Innovation Progress",
    									style = {
    										"margin-bottom": "0",
    										"textAlign": "center",
            								"color": TextOscuro
    									}
    								)
    							]
    						)
    					],
    					className = "ten columns",
    					id = 'title'
    				),
    				# Last updated
    				html.Div(
    					children = [
    						html.H6(
    							children = "Last Updated: " + " (UTC)",
    							style = {
                                    "textAlign": "right",
    								"color": Resolved_txt
    							}
    						)
    					],
    					className = "one column",
    					id = "title1"
    				)
    			],
    			id = "header",
    			className = "row flex-display",
    			style = {
    				"margin-bottom": "25px"
    			}
    		),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='General Metrics', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Metricas por jugador', value='tab-2', style=tab_style, selected_style=tab_selected_style),
    ]),
    html.Div(id='tabs-content')
], style=CONTENT_STYLE)
app.layout = server_layout

# Build the layout
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div(
	       children = [
		html.Div(id='KPI_CARD_GLOBALS',
			children = [
                    html.Div(
                        children = [
                            # Title
                            html.H6(
                                children = "Match Total",
                                style = {
                                    "textAlign": "center",
                                    "color": TextOscuro
                                }
                            ),
                            html.H2(
                                children = "(Unique)",
                                style = {
                                    "textAlign": "center",
                                    "color": "gray"
                                }
                            ),

                       
                            html.P(id='Total_KPI',
                                children = [],
                                style = {
                                    "textAlign": "center",
                                    "color": TextOscuro,
                                    "fontSize": 40
                                }
                            ),
                            
                            html.P(id='Total_year_KPI',
                                children = [],
                                style = {
                                    "textAlign": "center",
                                    "color": TextOscuro,
                                    "fontSize": 20,
                                    "margin-top": "-18px"
                                }
                            )
                        ],
                        className = "card_container two columns"
                    ),
                    # (Column 2): Global
                    html.Div(
                        children = [
                            # Title
                            html.H6(
                                children = "Score",
                                style = {
                                    "textAlign": "center",
                                    "color": TextOscuro
                                }
                            ),
                            html.H2(
                                children = "(Date)",
                                style = {
                                    "textAlign": "center",
                                    "color": "gray"
                                }
                            ),
                            # Total value
                            html.P(id='Res_KPI',
                                children = [],
                                style = {
                                    "textAlign": "center",
                                    "color": Resolved_txt,
                                    "fontSize": 40
                                }
                            ),
                            html.P(id='Res_year_KPI',
                                children = [],
                                style = {
                                    "textAlign": "center",
                                    "color": Resolved_txt,
                                    "fontSize": 20,
                                    "margin-top": "-18px"
                                }
                            ),
                        ],
                        className = "card_container two columns"
                    ),
                    # (Column 3): Global closed
                    html.Div(
                        children = [
                            # Title
                            html.H6(
                                children = "Teams",
                                style = {
                                    "textAlign": "center",
                                    "color": TextOscuro
                                }
                            ),
                            html.H2(
                                children = "(Date)",
                                style = {
                                    "textAlign": "center",
                                    "color": "gray"
                                }
                            ),
                            # Total closed
                            html.P(id='Clo_KPI',
                                children = [],
                                style = {
                                    "textAlign": "center",
                                    "color": "#e55467",
                                    "fontSize": 40
                                }
                            ),
                            # New closed
                            html.P(id='Clo_year_KPI',
                                children = [],
                                style = {
                                    "textAlign": "center",
                                    "color": "#e55467",
                                    "fontSize": 20,
                                    "margin-top": "-18px"
                                }
                            )
                        ],
                        className = "two columns"
                    ),
                    # (Column 4): Global active
                    html.Div(
                        children = [
                            # Title
                            html.H6(
                                children = "Stadium",
                                style = {
                                    "textAlign": "center",
                                    "color": TextOscuro
                                }
                            ),
                            html.H2(
                                children = "(Countries)",
                                style = {
                                    "textAlign": "center",
                                    "color": "gray"
                                }
                            ),
                            # Total v
                            html.P(id='Act_KPI',
                                children = [],
                                style = {
                                    "textAlign": "center",
                                    "color": "green",
                                    "fontSize": 40
                                }
                            ),
                            # New active
                            html.P(id='Act_year_KPI',
                                children = [],
                                style = {
                                    "textAlign": "center",
                                    "color": "green",
                                    "fontSize": 20,
                                    "margin-top": "-18px"
                                }
                            )
                        ],
                        className = "two columns"
                    ),
                    html.Div(
                        children = [
                            # Title
                            html.H6(
                                children = "Penalti",
                                style = {
                                    "textAlign": "center",
                                    "color": TextOscuro
                                }
                            ),
                            html.H2(
                                children = "(Gol)",
                                style = {
                                    "textAlign": "center",
                                    "color": "gray"
                                }
                            ),
                            # Total v
                            html.P(id='Penalti_KPI',
                                children = [],
                                style = {
                                    "textAlign": "center",
                                    "color": "green",
                                    "fontSize": 40
                                }
                            ),
                            # New active
                            html.P(id='Penlati_D_KPI',
                                children = [],
                                style = {
                                    "textAlign": "center",
                                    "color": "green",
                                    "fontSize": 20,
                                    "margin-top": "-18px"
                                }
                            )
                        ],
                        className = "two columns"
                    ),
                    html.Div(
                        children = [
                            # Title
                            html.H6(
                                children = "Faltas",
                                style = {
                                    "textAlign": "center",
                                    "color": TextOscuro
                                }
                            ),
                            html.H2(
                                children = "(Directa)",
                                style = {
                                    "textAlign": "center",
                                    "color": "gray"
                                }
                            ),
                            # Total v
                            html.P(id='Fault_KPI',
                                children = [],
                                style = {
                                    "textAlign": "center",
                                    "color": "green",
                                    "fontSize": 40
                                }
                            ),
                            # New active
                            html.P(id='Fault_D_KPI',
                                children = [],
                                style = {
                                    "textAlign": "center",
                                    "color": "green",
                                    "fontSize": 20,
                                    "margin-top": "-18px"
                                }
                            )
                        ],
                        className = "two columns"
                    )
                    ],
			className = "row flex-display",
		),
		html.Div(
			children = [
				html.Div(
					children = [
						dcc.Graph(
							id = "pie_chart_global",
							config = {
								"displayModeBar": "hover"
							},
                            style = {"height": "250px"}
						)
					],
					className = "four columns",
					style = {
						"maxWidth": "400px"
					}
				),
				html.Div(
					children = [
						dcc.Graph(
							id = "Event_type",
							config = {
								"displayModeBar": "hover"
							},
                            style = {"height": "250px"}
						)
					],
					className = "four columns"
				),
				html.Div(
					children = [
						dcc.Graph(
							id = "Event_score",
							config = {
								"displayModeBar": "hover"
							},
                            style = {"height": "250px"}
						)
					],
					className = "four columns"
				),

			],
			className = "row flex-display"
		),
		html.Div(
			children = [
				html.Div(
					children = [
						dcc.Graph(
							id = "mountain_global_chart",
							config = {
								"displayModeBar": "hover"
							}
						)
					],
					className = "six columns"
				),
				html.Div(
					children = [
						dcc.Graph(
							id = "bar_chart_global",
							config = {
								"displayModeBar": "hover"
							}
						)
					],
					className = "six columns"
				),

			],
			className = "row flex-display"
		),
		html.Div(
			children = [
				html.Div(
					children = [
						dcc.Graph(
							id = "Porteria",
							config = {
								"displayModeBar": "hover"
							}
						)
					],
					className = "six columns"
				),
				html.Div(
					children = [
						dcc.Graph(
							id = "Body_part",
							config = {
								"displayModeBar": "hover"
							}
						)
					],
					className = "six columns"
				),
			],
			className = "row flex-display"
		),
        html.Div([
            dcc.Markdown(children=markdown_text)
        ]),	sidebar],
	       id = "mainContainer",
	       style = {
		   "display": "flex",
		   "flex-direction": "column"
	       }
           )
    elif tab == 'tab-2':
        return html.Div(
	       children = [html.Div(
			children = [
                                        html.Div(
                                            children = [
                                            dash_table.DataTable(
                                                id='Shot_performance',
                                                    columns=[

                                                        dict(name='Player/Outcome', id='Player/Outcome', type='text'),
                                                        dict(name='Goal', id='Goal', type='text'),
                                                        dict(name='Blocked', id='Blocked', type='text'),
                                                        dict(name='Off T', id='Off T', type='text'),
                                                        dict(name='Post', id='Post', type='text'),
                                                        dict(name='Saved', id='Saved', type='text'),
                                                        dict(name='Saved Off Target', id='Saved Off Target', type='text', presentation='markdown'),
                                                        dict(name='Saved to Post', id='Saved to Post', type='text'),
                                                        dict(name='Total', id='All', type='text'),
                                                        ],
                                                    page_action='native',
                                                    page_size=12,
                                                    style_table ={'height': '400px', 'overflowY': 'auto'},
                                                    #filter_action="native",
                                                    sort_action="native",
                                                    style_cell={
                                                        'backgroundColor': 'rgb(50, 50, 50)',
                                                        'textAlign': 'left',
                                                        'color': 'white',
                                                        'passing': '5px',
                                                        'height': 'auto',
                                                        # all three widths are needed
                                                        'minWidth': '20px', 'width': '50px', 'maxWidth': '100px',
                                                        'whiteSpace': 'normal'},
                                                    style_as_list_view = True,
                                                    style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                                                    style_data={'whiteSpace': 'normal',
                                                        'height': 'auto',
                                                        'lineHeight': '15px',
                                                        },
                                                    
                                                )
                                            ],
                                            className = "nine columns"
                                        ),
                                        html.Div(
                                            children = [
                                                dcc.Graph(
                                                    id = "bar_player",
                                                    config = {
                                                        "displayModeBar": "hover"
                                                    }
                                                )
                                            ],
                                            className = "six columns"
                                        ),


			],
			className = "row flex-display"
		),
		sidebar],
	       id = "mainContainer",
	       style = {
		   "display": "flex",
		   "flex-direction": "column"
	       }
           )



@app.callback(
    [Output('Total_KPI', 'children'),
    Output('Res_KPI', 'children'),
	Output('Clo_KPI', 'children'),
	Output('Act_KPI', 'children'),
    Output('Total_year_KPI', 'children'),
    Output('Res_year_KPI', 'children'),
    Output('Clo_year_KPI', 'children'),
    Output('Act_year_KPI', 'children')],
	[Input(component_id = "dropdown_team",	component_property = "value"),
    Input(component_id = "dropdown_match",	component_property = "value")]
)
def update_KPI_CARDS_GLOBAL(team, match_):
    match_fil=match_filter(Match, team, match_)
    total_unique_match= len(match_fil["match_id"].unique())
    home_score_total=match_fil['home_score'].sum()
    away_score_total=match_fil['away_score'].sum()
    Total_score=home_score_total+away_score_total
    Total_home_team=len(pd.concat([match_fil['home_team.home_team_name'],match_fil['away_team.away_team_name']]).unique())
    Score_by="Home: "+f"{home_score_total} "+  " | " +    "Away: " +f"{away_score_total} "
    total_unique_country= len(match_fil["stadium.country.name"].unique())

    return total_unique_match, Total_score, Total_home_team, total_unique_country, ' ', Score_by, ' ', ' '

@app.callback(
	[Output(component_id = "pie_chart_global",	component_property = "figure"),
    Output(	component_id = "Event_score",	component_property = "figure")],
    [Input(component_id = "dropdown_team",	component_property = "value"),
    Input(component_id = "dropdown_type",	component_property = "value"),
    Input(component_id = "dropdown_match",	component_property = "value"),
    Input(component_id = "dropdown_possession",	component_property = "value"), 
    Input(component_id = "dropdown_player",  component_property = "value"),
    Input(component_id = "dropdown_shot_outcome_name",  component_property = "value")]    
)
def Match_pie_chart_global(team, type, match, possession, player, outcome):
    match_filt=match_filter(Match, team, match)
    
    data_pglo=match_filt.groupby(["stadium.country.name"]).size().nlargest(5).reset_index(name='counts')# Calculate values 
    #print(match_filt.columns)
    fig = px.pie(data_pglo, values='counts', names='stadium.country.name', hover_data=['stadium.country.name'],hole=.5, color="stadium.country.name", color_discrete_map = color_discrete, height= 250)
    fig.update_traces(hoverinfo='label+percent', textinfo='value+label', textfont_size=10, textposition='outside', insidetextorientation= "radial", showlegend=False,
                        marker=dict(colors=colors)) 
    fig1 = px.scatter(match_filt, x = 'home_score',y='away_score')

    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=10,
                      marker=dict(colors=colors))
    fig.update_layout({
    'plot_bgcolor': CardBackground,
    'paper_bgcolor': CardBackground,
    })

    fig.update_layout(
        title_font_color=TextOscuro,
    #    title = f"Year: {year} Status: {component}   -   Current Status",
        uniformtext_minsize=10, uniformtext_mode='hide')
    fig.update_layout(
        legend=dict(
            traceorder="reversed",
            title_font_family="Times New Roman",
            font=dict(
                family="sans serif",
                color=TextOscuro
            ),
        orientation= "h",
        )
    )
    fig.update_layout(
        font_color=TextOscuro,
        title_font_color=TextOscuro,
        legend_title_font_color=TextOscuro
        )
    fig1.update_layout({
    'plot_bgcolor': CardBackground,
    'paper_bgcolor': CardBackground,
    })

    fig1.update_layout(
        title_font_color=TextOscuro,
    #    title = f"Year: {year} Status: {component}   -   Current Status",
        uniformtext_minsize=10, uniformtext_mode='hide')
    fig1.update_layout(
        legend=dict(
            traceorder="reversed",
            title_font_family="Times New Roman",
            font=dict(
                family="sans serif",
                color=TextOscuro
            ),
        orientation= "h",
        )
    )
    fig1.update_layout(
        font_color=TextOscuro,
        title_font_color=TextOscuro,
        legend_title_font_color=TextOscuro
        )
    return fig, fig1

@app.callback(
	[Output(component_id = "mountain_global_chart", component_property = "figure"),
    Output(component_id = "bar_chart_global", component_property = "figure"),
    Output(component_id = "Event_type",	component_property = "figure")], 
	[Input(component_id = "dropdown_team",	component_property = "value"),
    Input(component_id = "dropdown_type",	component_property = "value"),
    Input(component_id = "dropdown_match",	component_property = "value"),
    Input(component_id = "dropdown_possession",	component_property = "value"), 
    Input(component_id = "dropdown_player",  component_property = "value"),
    Input(component_id = "dropdown_shot_outcome_name",  component_property = "value")]    
)
def events_mountain_global_chart(team, typo, match, possession, player, outcome):
	# Filter the data

    #print(events.columns.values)
    
    data_assignee=datafilter_report(events, team, typo, match, possession, player, outcome, 'All')
    datos_barglo=data_assignee.groupby(['player.name']).size().nlargest(10).reset_index(name='counts')
    datos_barglo_pass=data_assignee.groupby(['pase_nombre']).size().nlargest(10).reset_index(name='counts')
    datos_barglo2=data_assignee.groupby(["type.name"], dropna=True).size().reset_index(name='counts')
    #penal=len(data_assignee[(data_assignee['outcome.name']=='Goal')&(data_assignee['type.name']=='Penalty')])
    #falta=len(data_assignee[(data_assignee['outcome.name']=='Goal')&(data_assignee['type.name']=='Free Kick')])
    #print(data_assignee[(data_assignee['outcome.name']=='Goal')&(data_assignee['type.name']=='Penalty')])
    #print(data_assignee[(data_assignee['outcome.name']=='Goal')&(data_assignee['type.name']=='Free Kick')])
    if (typo == 'Shot'):
        fig = px.scatter(data_assignee, x = 'loc_x',y='loc_y',  size='shot.statsbomb_xg', color="shot.dangerous", color_discrete_map = color_discrete)
    else:
        fig = px.scatter(data_assignee, x = 'loc_x',y='loc_y', color="type.name", color_discrete_map = color_discrete)
    fig.update_layout(font_family="sans-serif",
                        font_color=TextOscuro,
                        title_font_family="sans-serif",
                        title_font_color=TextOscuro,
                        legend_title_font_color=TextOscuro)

    fig.update_layout({
                        'plot_bgcolor': CardBackground,
                        'paper_bgcolor': CardBackground,
                        })
    fig.update_yaxes(showgrid=False)
    fig.update_yaxes(range=[0, 80])
    fig.update_xaxes(range=[0, 120])
    if datos_barglo.empty:
        fig1 = px.scatter(x=[0], y=[0])
        fig1.update_layout({
        'plot_bgcolor': CardBackground,
        'paper_bgcolor': CardBackground,
        })

        fig1.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {
                    "text": "NO DATA",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )

    else:
        fig1 = px.bar(datos_barglo, x='counts', y='player.name')
    fig1.update_layout({
        'plot_bgcolor': CardBackground,
        'paper_bgcolor': CardBackground,
        })
    fig1.update_layout(
                title = f"Player Name",
                yaxis={'categoryorder':'total ascending'}),
    fig1.update_layout(
            legend=dict(
                traceorder="reversed",
                title_font_family="Times New Roman",
                font=dict(
                    family="sans serif",
                    color=TextOscuro
                )))
    fig1.update_layout(
        font_color=TextOscuro,
        title_font_color=TextOscuro,
        legend_title_font_color=TextOscuro
        )
    fig1.update_xaxes(showgrid=False)
    fig1.update_yaxes(showgrid=False)
 

    if datos_barglo.empty:
        fig2 = px.scatter(x=[0], y=[0])
        fig2.update_layout({
        'plot_bgcolor': CardBackground,
        'paper_bgcolor': CardBackground,
        })

        fig2.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {
                    "text": "NO DATA",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )

    else:
        if typo=='Shot':
            fig2 = px.bar(datos_barglo_pass, x='counts', y='pase_nombre', color='pase_nombre', hover_data=['pase_nombre'], height= 250)
            fig2.update_layout(
                title = f"Pase hecho por:",
                yaxis={'categoryorder':'total ascending'}),
        else:
            fig2 = px.bar(datos_barglo2, x='counts', y='type.name', color='type.name', hover_data=['type.name'], height= 250)
            fig2.update_layout(
                title = f"Event Types",
                yaxis={'categoryorder':'total ascending'}),

    fig2.update_layout({
        'plot_bgcolor': CardBackground,
        'paper_bgcolor': CardBackground,
        })
    fig2.update_layout(
            legend=dict(
                traceorder="reversed",
                title_font_family="Times New Roman",
                font=dict(
                    family="sans serif",
                    color=TextOscuro
                )))
    fig2.update_layout(
        font_color=TextOscuro,
        title_font_color=TextOscuro,
        legend_title_font_color=TextOscuro
        )
    fig2.update_xaxes(showgrid=False)
    fig2.update_yaxes(showgrid=False)
    fig2.update_layout(showlegend=False)

    return fig, fig1, fig2

@app.callback(
	[Output(component_id = "Porteria", component_property = "figure"),
    Output(component_id = "Body_part",	component_property = "figure")],
	[Input(component_id = "dropdown_team",	component_property = "value"),
    Input(component_id = "dropdown_type",	component_property = "value"),
    Input(component_id = "dropdown_match",	component_property = "value"),
    Input(component_id = "dropdown_possession",	component_property = "value"), 
    Input(component_id = "dropdown_player",  component_property = "value"),
    Input(component_id = "dropdown_shot_outcome_name",  component_property = "value")]    
)
def events_gol(team, typo, match, possession, player, outcome):
	# Filter the data

    data_assignee=datafilter_report(events, team, typo, match, possession, player, outcome, 'All')
    body_part=data_assignee.groupby(['shot.body_part.name', 'shot.outcome.name']).size().nlargest(10).reset_index(name='counts')
    gol=data_assignee[data_assignee['gol_x']>=120]
    #print(gol["shot.outcome.id"].unique())
    gol["shot.outcome.id"] = [float(each) for each in gol["shot.outcome.id"]]
    #print(gol["shot.outcome.id"].unique())
    # 98.  99.  97. 101. 100.  96. 115. 116.
    color = [
    0.1 if v == 98 else 0.2 if v == 99 else 0.3 if v == 97 else 0.4 if v == 96 else 0.5 if v == 101 else 0.6 if v == 100 else 0.7 if v == 115 else 0.8 if v == 116 else 0
    for v in gol["shot.outcome.id"]]
    
    colorscale = [[0, 'gray'], [0.1, 'red'], [0.2, 'green'], [0.3, 'red'], [0.4, 'blue'], [0.5, 'black'], [0.6, 'magenta']]
    fig = go.Figure()   
    if (outcome != 'All'):
        fig.add_trace(go.Scatter(x = gol['gol_y'], y = gol['gol_z'], marker = {'color': 'blue', 'size': 10}, mode="markers",  hovertext=gol["shot.outcome.name"], hoverinfo="text",))
#        fig = px.scatter(gol, x = 'gol_y',y='gol_z', color="shot.dangerous", color_discrete_map = color_discrete)
    else:
        fig.add_trace(go.Scatter(x = gol['gol_y'], y = gol['gol_z'], marker = {'color': color, 'colorscale': colorscale, 'size': 10}, mode="markers", hovertext=gol["shot.outcome.name"], hoverinfo="text",))
#        fig = px.scatter(gol, x = 'gol_y',y='gol_z', color="shot.dangerous", color_discrete_map = color_discrete)
    fig.add_trace(go.Scatter(
        x = [36,36,44,44],
        y = [0,2.67,2.67,0], mode="lines"
    ))
    fig.update_layout(yaxis_range=[0,3])
    fig.update_layout(xaxis_range=[33,46])
    fig.update_layout(font_family="sans-serif",
                        font_color=TextOscuro,
                        title_font_family="sans-serif",
                        title_font_color=TextOscuro,
                        legend_title_font_color=TextOscuro)

    fig.update_layout({
                        'plot_bgcolor': CardBackground,
                        'paper_bgcolor': CardBackground,
                        })
    fig.update_yaxes(showgrid=False)

    if body_part.empty:
        fig1 = px.scatter(x=[0], y=[0])
        fig1.update_layout({
        'plot_bgcolor': CardBackground,
        'paper_bgcolor': CardBackground,
        })

        fig1.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {
                    "text": "NO DATA",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )

    else:
        fig1 = px.bar(body_part, x='counts', y='shot.body_part.name', color='shot.outcome.name')
    fig1.update_layout({
        'plot_bgcolor': CardBackground,
        'paper_bgcolor': CardBackground,
        })
    fig1.update_layout(
                title = f"Body Part",
                yaxis={'categoryorder':'total ascending'}),
    fig1.update_layout(
            legend=dict(
                traceorder="reversed",
                title_font_family="Times New Roman",
                font=dict(
                    family="sans serif",
                    color=TextOscuro
                )))
    fig1.update_layout(
        font_color=TextOscuro,
        title_font_color=TextOscuro,
        legend_title_font_color=TextOscuro
        )
    fig1.update_xaxes(showgrid=False)
    fig1.update_yaxes(showgrid=False)

    return fig, fig1

@app.callback(
    [Output(component_id = 'Penalti_KPI', component_property = 'children'),	Output(component_id = 'Fault_KPI', component_property = 'children')],
	[Input(component_id = "dropdown_team",	component_property = "value"),
    Input(component_id = "dropdown_type",	component_property = "value"),
    Input(component_id = "dropdown_match",	component_property = "value"),
    Input(component_id = "dropdown_possession",	component_property = "value"), 
    Input(component_id = "dropdown_player",  component_property = "value"),
    Input(component_id = "dropdown_shot_outcome_name",  component_property = "value")]    
)
def events_KPI(team, typo, match, possession, player, outcome):
	# Filter the data
    data_assignee=datafilter_report(events, team, typo, match, possession, player, outcome, 'All')
    Penal=len(data_assignee[(data_assignee['shot.outcome.name']=='Goal')&(data_assignee['shot.type.name']=='Penalty')])
    Falt=len(data_assignee[(data_assignee['shot.outcome.name']=='Goal')&(data_assignee['shot.type.name']=='Free Kick')])
    return Penal, Falt

@app.callback(
    [Output("Shot_performance","data"),Output(component_id = "bar_player",	component_property = "figure")],
	[Input(component_id = "dropdown_team",	component_property = "value"),
    Input(component_id = "dropdown_type",	component_property = "value"),
    Input(component_id = "dropdown_match",	component_property = "value"),
    Input(component_id = "dropdown_possession",	component_property = "value"), 
    Input(component_id = "dropdown_player",  component_property = "value"),
    Input(component_id = "dropdown_shot_outcome_name",  component_property = "value")])
def update_data_jira(team, typo, match, possession, player, outcome):
    data_assignee=datafilter_report(events, team, typo, match, possession, player, outcome, 'All')  
    shot_dan=data_assignee[(data_assignee['shot.dangerous']==1)]
    #a = np.unique(shot_dan.to_numpy())
    #print(a)
    cross=pd.crosstab(shot_dan['player.name'], shot_dan['shot.outcome.name'], margins=True)#.reindex(columns=a, index=a, fill_value=0)
    iname = cross.index.name
    cname = cross.columns.name
    cross = cross.reset_index()
    cross.rename(columns={cross.columns[0]: 'Player/Outcome'}, inplace=True)
    cross = cross.sort_values(by='Goal', ascending=False)
    cross=cross[(cross['Goal']>=10)]
    
    cross['Eficiencia']=cross.Goal.div(cross.All).round(2)
    
    
    if cross.empty:
        return []
    else:
        table_details=pd.DataFrame(cross, columns=['Player/Outcome', 'Blocked', 'Goal', 'Off T', 'Post', 'Saved', 'Saved Off Target', 'Saved to Post', 'Wayward', 'All'])
        data_table=table_details.to_dict('records')
    cross = cross.sort_values(by='Eficiencia', ascending=False)

    if cross.empty:
            fig1 = px.scatter(x=[0], y=[0])
            fig1.update_layout({
            'plot_bgcolor': CardBackground,
            'paper_bgcolor': CardBackground,
            })

            fig1.update_layout(
                xaxis =  { "visible": False },
                yaxis = { "visible": False },
                annotations = [
                    {
                        "text": "NO DATA",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 28
                        }
                    }
                ]
            )

    else:
            fig1 = px.bar(cross, x='Player/Outcome', y='Eficiencia')
            fig1.update_layout({
                'plot_bgcolor': CardBackground,
                'paper_bgcolor': CardBackground,
                })
            fig1.update_layout(
                        title = f"Player Name",
                        yaxis={'categoryorder':'total ascending'}),
            fig1.update_layout(
                    legend=dict(
                        traceorder="reversed",
                        title_font_family="Times New Roman",
                        font=dict(
                            family="sans serif",
                            color=TextOscuro
                        )))
            fig1.update_layout(
                font_color=TextOscuro,
                title_font_color=TextOscuro,
                legend_title_font_color=TextOscuro
                )
            fig1.update_xaxes(showgrid=False)
            fig1.update_yaxes(showgrid=False)
            
    return data_table, fig1



if __name__ == "__main__":
  app.run_server()
