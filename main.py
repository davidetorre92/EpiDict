import argparse
import igraph as ig
from utils.input_handler import read_input_config, read_epidemics_config, read_input_graph
from utils.output_handler import write_initial_conditions_report, save_simulation_df
from utils.infection import initialize_simulation, simulate_epidemic
import numpy as np
import pandas as pd

def main():
    
    # Parse arguments
	parser = argparse.ArgumentParser(description = "Simulate a compartmental model on a graph with a preset set of rules.")
	parser.add_argument("--config", "-c", type=str, help="path/to/config.ini", required = True)
	args = parser.parse_args() 
	config_path = args.config 
 
	# Read config data
	epidemics_path, graph_path, report_path, experiment_output_path = read_input_config(config_path)

	# Read and initialize the epidemics configuration
	attributes, dynamics, initial_conditions, time_steps, measure_mode = read_epidemics_config(epidemics_path)
	# Read the Graph
	G = read_input_graph(graph_path)
	print(G.summary())
	print("Mean: ", np.mean(G.degree()))
	# Initialize simulation
	c, A, G_t = initialize_simulation(G, attributes, dynamics, initial_conditions)
 
	# Write initial conditions
	write_initial_conditions_report(G_t, c, report_path)
	# Simulate the epidemic
	experiment_df = simulate_epidemic(c, A, G_t, time_steps, measure_mode)
	# Save the simulation
	save_simulation_df(experiment_df, experiment_output_path)

if __name__ == '__main__':
    main()
