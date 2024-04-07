from utils.input_handler import read_input_config
from utils.infection import initialize_simulation, simulate_epidemic
from utils.output_handler import write_initial_conditions_report, save_simulation_df
import igraph as ig

config_path = './config.ini'

attributes, dynamics, initial_conditions, time_steps, measure_mode = read_input_config(config_path)
G = ig.Graph.Erdos_Renyi(n = 10, p = 0.2)
c, A, G_t = initialize_simulation(G, attributes, dynamics, initial_conditions)
write_initial_conditions_report(G_t, c, None)
experiment_df = simulate_epidemic(c, A, G_t, time_steps, measure_mode)
save_simulation_df(experiment_df, None)


