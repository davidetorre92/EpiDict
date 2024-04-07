import numpy as np
import igraph as ig
from scipy.sparse import csr_matrix
from .Compartments import TransitionRule
from .measurements_graph import Measure
from .initialize_data import initialize_compartments, initialize_graph

def sparse_adj_matrix(G: ig.Graph, undirected = False):
    E = G.get_edgelist()
    row = [e[0] for e in E]
    col = [e[1] for e in E]
    data = [1 for _ in E]
    
    if undirected is False:
        row, col = row + col, col + row
        data = data + data

    V = G.vcount()        
    A_sparse = csr_matrix((data, (row, col)), shape = (V, V))
    return A_sparse

def get_updated_indices_to_update(G: ig.Graph, A: csr_matrix, transition: TransitionRule):
    V = G.vcount()
    if transition.mode == 'neighbor':
        # Query nodes with the initial state
        initial_attribute_indices = [v.index for v in G.vs() if v[transition.attribute] == transition.initial_state]
        if len(initial_attribute_indices) == 0:
            return []
        # Query nodes with the triggering state
        triggering_attribute_indices = [v.index for v in G.vs() if v[transition.attribute] == transition.triggering_state]
        if len(triggering_attribute_indices) == 0:
            return []
        
        init_vec = np.zeros(V)
        init_vec[initial_attribute_indices] = 1
        trigger_vec = np.zeros(V)
        trigger_vec[triggering_attribute_indices] = 1
        # Count for each node how many neighbors are in the trigger state
        neighbor_trigger_attribute_count = A.dot(trigger_vec)
        # Apply a mask to get the vector containing the number of neighbors given the initial state
        neigh_given_init = np.where(init_vec == 1, neighbor_trigger_attribute_count, 0)
        # Apply the function
        transition_prob = 1 - np.power(1 - transition.prob, neigh_given_init)
        sample = np.random.random(V)
        indices = list(np.where(sample < transition_prob)[0])
        return indices
    
    elif transition.mode == 'rate':
        # Query nodes with the initial state
        initial_attribute_indices = [v.index for v in G.vs() if v[transition.attribute] == transition.initial_state]
        if len(initial_attribute_indices) == 0:
            return []
        init_vec = np.zeros(V)
        init_vec[initial_attribute_indices] = 1

        # Apply the function
        transition_prob = transition.prob * init_vec
        sample = np.random.random(V)
        indices = list(np.where(sample < transition_prob)[0])
        return indices

    else: raise ValueError(f"transition.mode {transition.mode} not implemented yet.")

def initialize_simulation(G: ig.Graph, attributes, dynamics, initial_conditions):
    c = initialize_compartments(attributes, dynamics, initial_conditions)
    A = sparse_adj_matrix(G)
    G_t = initialize_graph(G, initial_conditions)
    return c, A, G_t

def simulate_epidemic(c, A, G_t, time_steps, measure, verbosity = True):
    
    for time in range(0, time_steps):
        if verbosity: print(f"Time: {time+1} / {time_steps}")
        measure.append_experiment(G_t, 'compartment', time)
        G_t_plus_1 = G_t.copy()
        nodes_t_plus_1 = G_t_plus_1.vs()
        for transition in c.transition_rules:
            node_update_index = get_updated_indices_to_update(G_t, A, transition)
            nodes_t_plus_1[node_update_index][transition.attribute] = transition.final_state
        G_t = G_t_plus_1.copy()
    measure.append_experiment(G_t, 'compartment', time)
    return measure.concatenate_experiment()
