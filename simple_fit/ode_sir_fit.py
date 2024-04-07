import numpy as np
import pickle
from scipy.integrate import odeint
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from preprocess_epidemic_data import aggregate_epidemic_data

experiment_path = '/home/davide/ai/Projects/Epidemics/simulation_results/er_10k_subcrit_experiment.pickle'
experiment_df = pd.read_pickle(experiment_path)

def sir_model_eq(y, t, beta, gamma, N):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

def sir_model(beta, gamma, N, initial_infected, days):
    # SIR model differential equations.

    # Initial number of infected and recovered individuals, everyone else is susceptible to infection initially.
    I0 = initial_infected
    R0 = 0
    S0 = N - I0

    # Initial conditions vector
    y0 = S0, I0, R0

    # Time grid (in days)
    t = np.linspace(0, days, days)

    # Integrate the SIR equations over the time grid using odeint.
    result = odeint(sir_model_eq, y0, t, args=(beta, gamma, N))

    # Extract S, I, R from the result
    S, I, R = result.T

    # Create a DataFrame with the results
    sir_df = pd.DataFrame({'time': t, 'susceptible': S, 'infected': I, 'removed': R})

    return sir_df

def loss_sir(result_df, integration_df):
    def mse_sir(result_df, integration_df):
        def mse_timeseries(series_result, series_integration):
            delta = series_result - series_integration
            delta_2 = delta * delta
            mse = np.mean(delta_2)
            return mse
        
        mae_S = mse_timeseries(result_df['susceptible'], integration_df['susceptible'])
        mae_I = mse_timeseries(result_df['infected'], integration_df['infected'])
        mae_R = mse_timeseries(result_df['removed'], integration_df['removed'])
        return mae_S, mae_I, mae_R

    return np.sum(mse_sir(result_df, integration_df))

def optimize_parameters(result_df, N, initial_params=(0.2, 0.1)):
    def loss_function(params):
        beta, gamma = params
        # Simulate SIR model with current parameters
        sir_df = sir_model(beta, gamma, N, initial_infected, days)
        # Calculate the combined loss
        loss = loss_sir(result_df, sir_df)
        return loss

    # Bounds for beta and gamma (modify based on your context)
    bounds = [(0, 1), (0, 1)]
    initial_infected = float(result_df['infected'].iloc[0])
    days = result_df.shape[0]
    # Minimize the loss function using the L-BFGS-B optimization algorithm
    result = minimize(loss_function, initial_params, bounds=bounds, method='L-BFGS-B')

    optimal_params = result.x
    return optimal_params

N = 10000
result_df = aggregate_epidemic_data(experiment_df)
beta, gamma = optimize_parameters(result_df, N, initial_params=(0.8, 0.09))
days = result_df.shape[0]
initial_infected = float(result_df['infected'].iloc[0])
integration_df = sir_model(beta, gamma, N, initial_infected, days)

plt.scatter(result_df['time'], result_df['susceptible'], marker = 'o', c = 'r')
plt.plot(integration_df['time'], integration_df['susceptible'], c = 'r', label = 'susceptible')
plt.scatter(result_df['time'], result_df['infected'], marker = 'o', c = 'g')
plt.plot(integration_df['time'], integration_df['infected'], c = 'g', label = 'infected')
plt.scatter(result_df['time'], result_df['removed'], marker = 'o', c = 'b')
plt.plot(integration_df['time'], integration_df['removed'], c = 'b', label = 'removed')
plt.legend()
plt.text(0.7,0.8, f'beta = {beta:.4f}\ngamma = {gamma:.4f}\nSMSQ={loss_sir(result_df, integration_df):.4f}', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
plt.grid()
plt.title("Fit SIR - Barabasi Albert")
plt.savefig(experiment_path + '.png')
plt.show()

print(f"beta = {beta:.4f}, gamma = {gamma:.4f}")
