import numpy as np
from .Compartments import *
import igraph as ig

def initialize_compartments(attributes: dict, dynamics: dict, initial_conditions: dict):
    def check_data(c: Compartment, initial_conditions: dict):
        # Check if each attribute in initial_conditions is available in the Compartment
        for attribute, attribute_list in c.attributes.items():
            try:
                initial_conditions[attribute]
            except KeyError:
                print(f"Attribute {attribute} not available in the initial conditions")
            
            # Check if each value in initial_conditions[attribute] is available in the corresponding attribute list
            for attribute_ic in initial_conditions[attribute]:
                if attribute_ic not in attribute_list:
                    raise KeyError(f"{attribute_ic} not available in the {attribute} list {', '.join(map(str, attribute_list))}")

    # Create a Compartment object with the provided attributes
    c = Compartment(attributes)
    
    # Add dynamics to the Compartment object
    for _, item in dynamics.items():
        c.add_dynamic_from_dictionary(**item)
    
    # Check data consistency between Compartment attributes, dynamics, and initial_conditions
    check_data(c, initial_conditions)
    
    return c

def initialize_graph(G_model: ig.Graph, initial_conditions: dict):
    """
    Initialize compartments of nodes in the graph G based on given probabilities.

    Parameters:
        - G_model: Graph object
        - initial_conditions: Dictionary containing initial probabilities for attributes
    Returns:
        G: Graph object with initialized attributes
    """
    def check_normalization(attributes):
            # Check if the probabilities are normalized
            sum = 0
            for _, value in attributes.items():
                sum += value
            if sum != 1: raise ValueError(f"Initial conditions on attributes should sum to 1. Their sum is {sum}")
            
    G = G_model.copy()
    for attribute in initial_conditions.keys():
        if attribute == 'compartment':
            check_normalization(initial_conditions[attribute])
            # Extract compartment names and probabilities
            compartments_names, compartments_probs = zip(*initial_conditions[attribute].items())
            # Initialize compartments for nodes
            initial_nodes_compartments = np.random.choice(compartments_names, G.vcount(), p=compartments_probs)
            # Assign compartments to graph nodes
            G.vs[attribute] = initial_nodes_compartments
        else: raise ValueError(f"Attribute {attribute} not implemented yet.")
    return G