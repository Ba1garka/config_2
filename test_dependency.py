import unittest
from unittest.mock import patch, mock_open
from dependency import create_dot, Graph


class TestCreateDot(unittest.TestCase):
    def test_create_dot_with_commits(self):

        commits = [
            {
                "hash": "abcd1234",
                "massage": "Initial commit",
                "dependencies": []
            },
            {
                "hash": "efgh5678",
                "massage": "Added feature",
                "dependencies": ["abcd1234"]
            }
        ]
        expected_dot_content = (
            'digraph G {\n'
            '    "abcd1234" [label="Initial commit"];\n'
            '    "efgh5678" [label="Added feature"];\n'
            '    "abcd1234" -> "efgh5678";\n'
            '}'
        )
        dot_content = create_dot(commits)
        self.assertEqual(dot_content, expected_dot_content)


class TestGraph(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.run')
    @patch('dependency.get_commits')
    def test_build_graph(self, mock_get_commits, mock_subprocess, mock_file):

        mock_get_commits.return_value = [
            {
                "hash": "abcd1234",
                "massage": "Initial commit",
                "dependencies": []
            }
        ]

        graphviz_path = 'C:/Program Files/Graphviz/bin/dot.exe'
        repo_path = 'C:/Users/ovdem/PycharmProjects/config_2/repo_conf_2'
        output_path = 'C:/Users/ovdem/PycharmProjects/config_2/output.png'

        graph = Graph(graphviz_path, repo_path, output_path)
        graph.build_graph()

        # Проверка, что get_commits вызван с правильным путем репозитория
        mock_get_commits.assert_called_once_with(repo_path)

        # Проверка, что открытие и запись dot-файла выполнены
        mock_file.assert_called_once_with("graph.dot", "w")
        mock_file().write.assert_called_once()  # Проверяем, что в файл записывается что-то

        # Проверка, что subprocess.run с правильными аргументами
        cmd = [graphviz_path, "-Tpng", "graph.dot", "-o", output_path]
        mock_subprocess.assert_called_once_with(cmd)


if __name__ == '__main__':
    unittest.main()

