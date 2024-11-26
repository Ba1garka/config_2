import subprocess
from git import get_commits

def create_dot(commits):
    dot_content = ["digraph G {"]
    for commit in commits:
        node_line = f'    "{commit["hash"]}" [label="{commit["massage"]}"];'
        dot_content.append(node_line)
        for dep in commit["dependencies"]:
            edge_line = f'    "{dep}" -> "{commit["hash"]}";'
            dot_content.append(edge_line)
    dot_content.append("}")
    return "\n".join(dot_content)

class Graph:
    def __init__(self, graphviz_path, repo_path, output_path):
        self.graphviz_path = graphviz_path
        self.repo_path = repo_path
        self.output_path = output_path
        self.commits = []

    def build_graph(self):
        self.commits = get_commits(self.repo_path)
        dot_content = create_dot(self.commits)
        with open("graph.dot", "w") as f:
            f.write(dot_content)
        cmd = [self.graphviz_path, "-Tpng", "graph.dot", "-o", self.output_path]
        subprocess.run(cmd)

    def run(self):
        self.build_graph()
        print(f"Граф построен и сохранен в {self.output_path}.")