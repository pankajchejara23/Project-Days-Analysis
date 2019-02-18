import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import json


# Read project days data file
df = pd.read_csv("Data_16_original.csv")

# Read MFA results file
mf_df = pd.read_csv("mfaresult_16th.csv")

# Add MFA results to df dataframe
df['engagement'] = mf_df.iloc[:,1]
df['techvsphy'] = mf_df.iloc[:,2]

# Fetch group labels
groups = df.group.unique()


# Computer overall engagement by averaging
engagement ={}
for group in groups:
    mdf = df.loc[df.group==group,'engagement']
    engagement[group]=mdf.mean()



# Function to fetch basic info e.g. total number of students, total number of groups
def getInfoProjectDays(df):
# Number of Students and Number of Groups
    total_student=0
    student_group = {}
    groups = df.group.unique()
    group_index = 1
    for group in groups:
        student_group[group_index] = len(list(group))-1
        total_student += len(list(group))-1
        group_index += 1

    return (total_student,len(groups),student_group)


# Function to computer duration of group activity for each group
def getDuration(df,groups):
    duration = {}
    for group in groups:
        tf = df.loc[df.group == group,:]

        # Sorting on basis of timestamp
        sf = tf.sort_values(by="timestamp")

        # Fetch first and last entry for timestamp
        t1 = sf['timestamp'][sf.index[0]]
        t2 = sf['timestamp'][sf.index[-1]]

        # Computer the difference in terms of minutes
        tdf = (pd.to_datetime(t2) - pd.to_datetime(t1))/np.timedelta64(1,'m')

        # Adding duration value in dictionary
        duration[group]=tdf
    return duration

# Get basic information of project days
pd_info = getInfoProjectDays(df)
'''
app = dash.Dash()
app.layout = html.Div([
    html.H1("Project Days Information"),
    html.Div(children=[
        html.H1(style={'fontSize':70,'marginBottom':0},children=pd_info[0]),
        html.P(children=["Students"],style={'fontSize':20,'color':'red','marginTop':0}),
    ],className="six columns"),
    html.Div(children=[
        html.H1(style={'fontSize':70,'marginBottom':0},children=pd_info[1]),
        html.P(children=["Groups"],style={'fontSize':20,'color':'red','marginTop':0}),
    ],className="six columns")
],className='row')

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__=='__main__':
    app.run_server(debug=True)
'''

# Get duration for each group
duration = getDuration(df,groups)

# Creating dashboard
app = dash.Dash()

# Adding external css
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# Adding components to layout
app.layout = html.Div([
    html.H1(children="Project Days Dashboard",style={'textAlign':'center'}),
    html.Div([
        html.Div([
            html.H1(children=pd_info[0],style={'fontSize':60}),
            html.P("Students")
        ], className="two columns",style={'textAlign':'center'}),

        html.Div([
            html.H1(children=pd_info[1],style={'fontSize':60}),
            html.P("Groups")
        ], className="two columns",style={'textAlign':'center'}),
        html.Div([
            html.H5(children = [group+" " for group in groups]),
            html.P("Group's Label")
        ], className="three columns",style={'textAlign':'left'}),

    ], className="row",style={'marginBottom':30}),
    html.Div([
        html.Div([
            html.H3("Duration"),
            dcc.Graph(id='g1', figure={'data': [{'x':duration.values(),'y':duration.keys(),'type':'bar','orientation':'h'}],'layout':{'title':'Duration (min) of group activity'}})
        ], className="six columns",style={'textAlign':'center'}),

        html.Div([
            html.H3('Engagement'),
            dcc.Graph(id='g2',hoverData={'points': [{'group':'1AB'}]}, figure={'data': [{'y':engagement.values(),'x':engagement.keys(),'type':'bar'}],'layout':{'title':'Overall engagement of groups','clickmode':'event+select'}})
        ], className="six columns",style={'textAlign':'center'}),

    ], className="row"),
    html.Div([
        html.Div([
            html.H3("Engagement over time"),
            dcc.Graph(
                id='g3'

            )
        ], className="six columns",style={'textAlign':'center'}),
        html.Div(id='demo')

    ], className="row")
])

# Callback for updating Engagement graph on hover event
@app.callback(
    dash.dependencies.Output('g3','figure'),
    [dash.dependencies.Input('g2','hoverData')]
)
def update_timeseries(hoverData):
    group_name = hoverData['points'][0]['x']
    dff = df[df['group']==group_name]
    dff=dff.sort_values(by="timestamp")
    return {
        'data':[go.Scatter(
            x=dff['timestamp'],
            y=dff['engagement'],
            mode='lines+markers'
        )]
    }






if __name__ == '__main__':
    app.run_server(debug=True)
