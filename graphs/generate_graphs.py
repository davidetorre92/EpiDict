import numpy as np
import igraph as ig
import argparse
import re

def parse_function_string(func_str):
    # Use regular expression to extract function name and arguments
    match = re.match(r'([a-zA-Z_]\w*)\((.*)\)', func_str)
    
    if match:
        function_name = match.group(1)
        arguments_str = match.group(2)
        
        # Split the arguments string into a list
        arguments = [float(arg.strip()) for arg in arguments_str.split(',') if arg.strip()]
        
        return function_name, arguments
    else:
        raise ValueError(f"Invalid function string: {func_str}")


def ER(*args):
    N = int(args[0])
    p = args[1]
    return ig.Graph.Erdos_Renyi(n = N, p = p)



def main():
    parser = argparse.ArgumentParser(description="Generate and save a graph based on a specified function.")
    parser.add_argument("--function", "-f", type=str, help="Specify the function and its arguments (e.g., ER(20, 0.1))", required=True)
    parser.add_argument("--output", "-o", type=str, help="Specify the output path for the GraphML file", required=True)

    args = parser.parse_args()

    # Parse the function string to get function name and arguments
    function_str = args.function
    output_path = args.output
    function_name, arguments = parse_function_string(function_str)

    try:
        selected_function = globals()[function_name]
    except:
        print(f"Error: Function {function_name} not found in the script.")

    G = selected_function(*arguments)
    ig.Graph.write_graphml(G, output_path)
    print(f"Graph saved in {output_path}")
    
    return None

if __name__ == '__main__':
    main()