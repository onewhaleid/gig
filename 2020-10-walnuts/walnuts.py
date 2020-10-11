import io
import pandas as pd
from lxml import etree, html
import plotly.express as px


def fig_to_html(fig, path):
    """Write plotly figure to HTML without embedding plotly js."""

    # Get html string
    f = io.StringIO()
    fig.write_html(f, include_plotlyjs=False)
    f.seek(0)

    # Add plotly js to HTML
    root = etree.HTML(f.read())
    js = html.Element('script', src="https://cdn.plot.ly/plotly-latest.min.js")
    root.insert(0, js)

    # Write to file
    with open(path, 'wb') as f:
        f.write(html.tostring(root))


df = pd.read_csv('walnuts.csv', parse_dates=['date'])
df = df.sort_values('date').reset_index(drop=True)
df['day'] = (df['date'] - df['date'].min()).dt.days

master = pd.DataFrame()

i = 0
while i <= df['day'].max():
    df1 = df[df['day'] <= i].copy()
    df1['day'] = i
    master = master.append(df1)
    i += 1

master['size'] = master['count']
master.loc[master['size'] > 6, 'count'] = '???'
master.loc[master['size'] > 6, 'size'] = 6

fig = px.scatter_mapbox(
    master,
    lat='lat',
    lon='lon',
    size='size',
    size_max=20,
    hover_data={
        'count': True,
        'location': True,
        'day': False,
        'size': False,
        'lon': False,
        'lat': False,
    },
    color_discrete_sequence=['fuchsia'],
    animation_frame='day',
    zoom=13,
    # height=300,
)

token = open('.mapbox_token').read()
fig.update_layout(mapbox_style='dark', mapbox_accesstoken=token)
fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
fig_to_html(fig, 'walnuts.html')
