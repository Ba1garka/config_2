from dependency import Graph
import json

def load_config(config_path):
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Error: The file '{config_path}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{config_path}' is not valid JSON.")
        return None

def main():
    config = load_config('config.json')
    graphviz_path = config.get('graphviz_path')
    repo_path = config.get('repo_path')
    output_path = config.get('output_path')

    graph = Graph(graphviz_path, repo_path, output_path)
    graph.run()

if __name__ == "__main__":
    main()