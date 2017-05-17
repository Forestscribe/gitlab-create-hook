import gitlab
import requests_mock

GL_URL = "https://gitlab"
GL_TOKEN = "XXX"


def test_gitlab():
    with requests_mock.mock() as m:
        m.get("https://gitlab/api/v4/projects/forestscribe-yocto%2Fa_bsp_kernel_bxt/hooks", json=[])
        m.post("https://gitlab/api/v4/projects/forestscribe-yocto%2Fa_bsp_kernel_bxt/hooks", json={'id': 4})
        gl = gitlab.GLSession(GL_URL, GL_TOKEN)
        gl.setupHook('forestscribe-yocto/a_bsp_kernel_bxt', "https://gitlab_hook")
        assert m.call_count == 2


def test_gitlab_already_setup():
    with requests_mock.mock() as m:
        m.get("https://gitlab/api/v4/projects/forestscribe-yocto%2Fa_bsp_kernel_bxt/hooks", json=[
            {'url': "https://gitlab_hook"}])
        gl = gitlab.GLSession(GL_URL, GL_TOKEN)
        gl.setupHook('forestscribe-yocto/a_bsp_kernel_bxt', "https://gitlab_hook")
        assert m.call_count == 1
