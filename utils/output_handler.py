import numpy as np
import igraph as ig
import os
from collections import Counter
from .Compartments import *

def save_simulation_df(experiment_df, output_path):
    """
    Save the simulation results DataFrame to a specified file.

    Parameters:
        - experiment_df: pandas DataFrame
            The DataFrame containing simulation results.
        - output_path: str or None
            The path to save the output file. If None, a default path is used.

    Returns:
        - bool
            True if the saving process was successful, False otherwise.
    """
    try:
        # Check if the output_path is None
        if output_path is None:
            # Use a default path if not specified
            output_path = './output_experiment.pickle'
            experiment_df.to_pickle('./output_experiment.pickle')
        else:
            # Check the file extension and save accordingly
            if output_path.endswith('.pickle'):
                experiment_df.to_pickle(output_path)
            elif output_path.endswith('.csv'):
                experiment_df.to_csv(output_path)
            else:
                # Handle unimplemented extensions by defaulting to .pickle
                extension = output_path.split('.')[-1]
                name = '.'.join(output_path.split('.')[:-1])
                print(f'Warning: Extension {extension} not implemented yet. Changing it to .pickle')
                output_path = f'{name}.pickle'
                experiment_df.to_pickle(output_path)
        
        print(f'Experiment data saved in {output_path}')
        return True
    except Exception as e:
        # Catch any exception during writing and return False
        print(f'Error during saving: {e}')
        return False


def write_initial_conditions_report(G_init: ig.Graph, C: Compartment, output_path):
    if output_path is None:
        output_path = './report.dat'
    try:
        # Open the output file in write mode
        with open(output_path, 'w') as output_file:
            # Write graph summary to the file
            output_file.write("Graph Summary:\n")
            output_file.write(f"Graph name: {G_init['name']}")
            output_file.write(G_init.summary() + "\n")
            output_file.write("Mean: " + f'{np.mean(G_init.degree()): .2f}')
            output_file.write("\n\n")

            # Write initial graph conditions
            output_file.write("Compartment initial conditions:\n")

            for attribute in C.attributes:
                output_file.write(str(Counter(G_init.vs[attribute])))
                output_file.write('\n\n')
            
            # Write compartment information to the file
            output_file.write("Compartment Information:\n")
            output_file.write(str(C) + "\n")

        # Return True if the operation was successful
        print(f"Report with simulation initialization parameter saved in {output_path}")
        return True
    except Exception as e:
        # Print or log the exception for debugging purposes
        print(f"Error: {e}")
        # Return False if there was an error
        return False
    