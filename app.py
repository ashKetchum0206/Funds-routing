from flask import Flask, render_template, request, send_file
import graphviz
import os
from Network_flow import network_flow_api 
app = Flask(__name__)

# Your Ford-Fulkerson function goes here, which generates a Graphviz image
def solve_max_flow(graph_input):
    network_flow_api(graph_input)
    image_path = 'static/Graph_visualization.png'
    # dot.render(filename=image_path, format='png', cleanup=True)
    return image_path

@app.route('/', methods=['GET'])
def index():
    return render_template('homepage.html')

@app.route('/solve', methods=['POST'])
def solve():
    graph_input = request.form['graphInput']
    image_path = solve_max_flow(graph_input)
    return render_template('result.html', image_path=image_path)

if __name__ == '__main__':
    app.run(port=8080)