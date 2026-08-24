from scripts.git_helper import GitHelper


def test_build_authenticated_url_includes_actor_and_token():
    helper = GitHelper(token='test-token', actor='octocat')

    authenticated_url = helper._build_authenticated_url(
        'https://github.com/octocat/hello-world.git'
    )

    scheme, rest = authenticated_url.split('://', 1)
    credentials, host_and_path = rest.split('@', 1)

    assert scheme == 'https'
    assert credentials == 'octocat:test-token'
    assert host_and_path == 'github.com/octocat/hello-world.git'


def test_build_authenticated_url_leaves_non_https_urls_unchanged():
    helper = GitHelper(token='test-token', actor='octocat')

    clone_url = 'git@github.com:octocat/hello-world.git'

    assert helper._build_authenticated_url(clone_url) == clone_url
