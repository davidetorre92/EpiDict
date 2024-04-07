import numpy as np
import pandas as pd

def aggregate_epidemic_data(df):
    # Group by 'time' and 'compartment' and count occurrences
    result_df = df.groupby(['time', 'compartment']).size().reset_index(name='count')

    # If you want to fill missing compartments with 0 count, you can use pivot
    result_df = result_df.pivot(index='time', columns='compartment', values='count').fillna(0).reset_index().iloc[:-1,:]

    return result_df