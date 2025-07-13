#!/usr/bin/env python3
"""
Dashboard Application for Visualizing Telecom Network KPI and Congestion

This Dash application performs the following:
• Connects to ArangoDB to fetch nodes (from "traffic_data") and edges (from "cell_edges").
• Constructs a Cytoscape graph where each node’s color reflects the latest congestion state.
• Periodically refreshes the graph (every 60 seconds) using an Interval component.
• When a node (cell) is clicked, a detailed table of its attributes appears.
"""

from dash import Dash, dcc, html, Input, Output, dash_table
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import json
import time

from arango import ArangoClient
from arango.exceptions import DocumentGetError

# -------------------------------------------
# ArangoDB Connection Configuration
# -------------------------------------------
ARANGO_URL = "http://localhost:8529"
DB_NAME = "_system"
USERNAME = "root"
PASSWORD = "yourpassword"

# Collection names (must exist already)
TRAFFIC_COLLECTION = "traffic_data"  # Node collection
EDGE_COLLECTION = "cell_edges"       # Edge collection (cell-to-cell connections)

# Connect to ArangoDB
client = ArangoClient(hosts=ARANGO_URL)
db = client.db(DB_NAME, username=USERNAME, password=PASSWORD)

if not db.has_collection(TRAFFIC_COLLECTION):
    raise Exception(f"Collection {TRAFFIC_COLLECTION} not found! Ensure your data generator/updater has been run.")
traffic_col = db.collection(TRAFFIC_COLLECTION)
if not db.has_collection(EDGE_COLLECTION):
    raise Exception(f"Collection {EDGE_COLLECTION} not found! Ensure your edge generation has been run.")
edge_col = db.collection(EDGE_COLLECTION)

# -------------------------------------------
# Helper Function: Fetch Graph Data from ArangoDB
# -------------------------------------------
def get_graph_elements():
    """
    Fetch nodes from traffic_data and edges from cell_edges.
    Returns a list of elements formatted for Dash Cytoscape.
    Each node's data includes its _key, cell_id, congestion, color, and timestamp.
    """
    elements = []
    # Fetch all cell nodes
    try:
        for doc in traffic_col.all():
            node_data = {
                'id': doc['_key'],
                'label': f"Cell {doc.get('cell_id', doc['_key'])}",
                'color': doc.get('color', 'grey'),
                'device_congestion': doc.get('device_congestion', "N/A"),
                'call_drop_rate': doc.get('call_drop_rate', "N/A"),
                'handover_success_rate': doc.get('handover_success_rate', "N/A"),
                'packet_loss_rate': doc.get('packet_loss_rate', "N/A"),
                'latency_ms': doc.get('latency_ms', "N/A"),
                'resource_utilization': doc.get('resource_utilization', "N/A"),
                'last_congestion_update': doc.get('last_congestion_update', "N/A")
            }
            elements.append({'data': node_data})
    except Exception as e:
        print("Error fetching nodes:", e)

    # Fetch all edges; assume _from and _to use the format "traffic_data/<key>"
    try:
        for doc in edge_col.all():
            source = doc.get('_from', "").split('/')[1]
            target = doc.get('_to', "").split('/')[1]
            edge_data = {
                'source': source,
                'target': target,
                'relation': doc.get('relation', '')
            }
            elements.append({'data': edge_data})
    except Exception as e:
        print("Error fetching edges:", e)

    return elements

# -------------------------------------------
# Dash App Setup
# -------------------------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # For deployment if needed

# Define a stable Cytoscape layout. In this configuration:
# - 'randomize' is False, so nodes start in consistent positions.
# - 'numIter' is lowered for a quick, static layout.
# - 'animate' is False to prevent continuous re-layout.
layout = {
    'name': 'cose',
    'idealEdgeLength': 150,
    'nodeOverlap': 20,
    'padding': 50,
    'randomize': False,
    'componentSpacing': 150,
    'nodeRepulsion': 450000,
    'edgeElasticity': 100,
    'nestingFactor': 5,
    'gravity': 80,
    'numIter': 250,
    'animate': False
}

# Define Cytoscape stylesheet
cyto_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'label': 'data(label)',
            'background-color': 'data(color)',
            'width': '40px',
            'height': '40px',
            'font-size': '12px',
            'text-valign': 'center',
            'color': 'white'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#ccc',
            'target-arrow-color': '#ccc',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'width': 2
        }
    }
]

# App Layout:
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H3("Telecom Network Dashboard: KPI & Congestion Visualization"), width=12),
        className="my-3"
    ),
    dbc.Row(
        dbc.Col(
            cyto.Cytoscape(
                id='cytoscape-graph',
                layout=layout,
                style={'width': '100%', 'height': '500px'},
                stylesheet=cyto_stylesheet,
                elements=get_graph_elements()
            ),
            width=12
        ),
        className="my-2"
    ),
    dbc.Row(
        dbc.Col(html.H5("Selected Node Details:"), width=12)
    ),
    dbc.Row(
        dbc.Col(
            dash_table.DataTable(
                id='node-details',
                columns=[
                    {"name": "Attribute", "id": "Attribute"},
                    {"name": "Value", "id": "Value"}
                ],
                data=[],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            ),
            width=12
        )
    ),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # 60 seconds
        n_intervals=0
    )
], fluid=True)

# -------------------------------------------
# Callbacks
# -------------------------------------------
@app.callback(
    Output('cytoscape-graph', 'elements'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n_intervals):
    """
    Update the Cytoscape graph elements every 60 seconds by refetching the latest data.
    """
    return get_graph_elements()

@app.callback(
    Output('node-details', 'data'),
    Input('cytoscape-graph', 'tapNodeData')
)
def display_node_details(data):
    """
    When a node is clicked, display its attributes in a table.
    """
    if data is None:
        return []
    details = [{"Attribute": str(key), "Value": str(value)} for key, value in data.items()]
    return details

# -------------------------------------------
# Run the Application
# -------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
