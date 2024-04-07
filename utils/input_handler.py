from configparser import SafeConfigParser
import ast
import os
from .measurements_graph import *
import igraph as ig

def check_file_existance(path, describer):
    if os.path.exists(path) is False:
        raise FileExistsError(f"{describer} file {path} does not exist.")

def read_input_config(config_path):

    config = SafeConfigParser()
    config.read(config_path)
    check_file_existance(config_path, 'Configuration')

    epidemics_path = config.get('epidemics configuration file path', 'epidemics_path')
    graph_path = config.get('graph file path', 'graph_path')
    report_path = config.get('report and initial conditions output path', 'report_path')
    experiment_output_path = config.get('experiment output path', 'experiment_output_path')
    
    return epidemics_path, graph_path, report_path, experiment_output_path
    
def read_epidemics_config(epidemics_path):
    
    check_file_existance(epidemics_path, 'Epidemics configuration')
    config = SafeConfigParser()
    config.read(epidemics_path)
    print(config.sections())
    # Extract compartments' names
    attributes_str = config.get('attributes', 'attributes')
    attributes = ast.literal_eval(attributes_str)
    # Extract dynamics as a string from the config file
    dynamics_str = config.get('dynamics', 'sir_model')
    dynamics = ast.literal_eval(dynamics_str)
    # Extract initial conditions
    initial_conditions_str = config.get('initial_conditions', 'initial_attributes')
    initial_conditions = ast.literal_eval(initial_conditions_str)
    # Extract simulation time steps
    time_steps_str = config.get('experiment', 'time_steps')
    time_steps = int(time_steps_str)
    # Extract measurement mode
    meas_mode_str = config.get('experiment', 'measurement_mode')
    meas_func = Measure(meas_mode_str)
    
    return attributes, dynamics, initial_conditions, time_steps, meas_func

def read_input_graph(graph_path):
    check_file_existance(graph_path, 'Graph')
    if graph_path.endswith(".graphml"):
        G = ig.Graph.Read_GraphML(graph_path)
    elif graph_path.endswith(".pickle"):
        G = ig.Graph.Read_Pickle(graph_path)
    else:
        raise TypeError("The graph extension is not supported")

    try:
        G['name']
    except:
        graph_name = os.path.basename(graph_path)
        print(f"Warning attribute 'name' not available in the graph. Changing to {graph_name}")
        G['name'] = graph_name
    
    return G
