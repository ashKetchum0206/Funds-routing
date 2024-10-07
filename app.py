from flask import Flask, render_template, request, send_file
import graphviz
import os
from Network_flow import network_flow_api 
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('homepage.html')

@app.route('/solve', methods=['POST'])
def solve():

    node_number = request.form['node_number']
    edge_number = request.form['edge_number']
    edges = request.form['edges']
    sources = request.form['sources']
    sinks = request.form['sinks']
    source_capacities = request.form['source_capacities']
    
    image_path = 'static/Graph_visualization.png'
    network_flow_api(node_number, edge_number, edges, sources, sinks, source_capacities)
    return render_template('result.html', image_path=image_path)

if __name__ == '__main__':
    app.run(port=8080)