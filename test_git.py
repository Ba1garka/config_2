import unittest
from unittest.mock import patch
from git import get_commits


class TestGetCommits(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_commits_success(self, mock_subprocess):

        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = (
            'abcd1234|Initial commit|\n'
            'efgh5678|Added feature|abcd1234'
        )

        repo_path = 'C:/Users/ovdem/PycharmProjects/config_2/repo_conf_2'
        expected_commits = [
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

        commits = get_commits(repo_path)
        self.assertEqual(commits, expected_commits)

    @patch('subprocess.run')
    def test_get_commits_failure(self, mock_subprocess):

        mock_subprocess.return_value.returncode = 1

        repo_path = 'C:/Users/ovdem/PycharmProjects/config_2/repo_conf_2'

        with self.assertRaises(Exception) as context:
            get_commits(repo_path)

        self.assertEqual(str(context.exception), "Ошибка получения коммитов!")


if __name__ == '__main__':
    unittest.main()
