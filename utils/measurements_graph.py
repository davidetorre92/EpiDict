import numpy as np
import pandas as pd
import igraph as ig
from collections import Counter

class Measure:
    def __init__(self, meas_mode_str):
        available_modes = ['aggregate', 'detailed']
        if meas_mode_str not in available_modes:
            raise ValueError(f"Measure function not implemented yet. Choose between {', '.join(available_modes)}")
        if meas_mode_str == 'aggregate':
            self.experiment_data = []
            self.meas_func = measure_aggregate_on_G
            self.append_experiment = self._simple_append
            self.concatenate_experiment = self._simple_concat
        elif meas_mode_str == 'detailed':
            self.experiment_data = []
            self.meas_func = measure_detailed_on_G
            self.append_experiment = self._simple_append
            self.concatenate_experiment = self._simple_concat
            
    def _simple_append(self, G, attribute_string, t):
        results = self.meas_func(G, attribute_string, t)
        self.experiment_data.append(results)
    def _simple_concat(self):
        return pd.concat([data for data in self.experiment_data])
    
def get_measurement_function(meas_mode_str):
    if meas_mode_str == 'aggregate':
        meas_func = measure_aggregate_on_G
    elif meas_mode_str == 'detailed':
        meas_func = measure_detailed_on_G
    else: raise ValueError("Measure function not implemented yet.")
    return meas_func

def measure_detailed_on_G(G: ig.Graph, attribute_name, t:int):
    rows = [(v.index, v[attribute_name], t) for v in G.vs()]
    return pd.DataFrame(rows, columns = ['node_index', attribute_name, 'time'])

def measure_aggregate_on_G(G: ig.Graph, attribute_name, t:int):
    nodes_attribute = [v[attribute_name] for v in G.vs()]
    # Count occurrences of each element in the list
    element_counts = Counter(nodes_attribute)
    
    # Create a list of tuples with element, count, and t
    rows = [(element, count, t) for element, count in element_counts.items()]

    return pd.DataFrame(rows, columns = [attribute_name, 'value', 'time'])