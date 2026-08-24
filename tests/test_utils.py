from scripts.utils import load_env_inputs


def test_load_env_inputs_reads_gh_token(monkeypatch):
    monkeypatch.setenv('GH_TOKEN', 'test-token')
    monkeypatch.setenv('GITHUB_TOKEN', 'reserved_token_name_should_be_ignored')

    inputs = load_env_inputs()

    assert inputs['github_token'] == 'test-token'
