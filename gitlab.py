import urllib

from requests import Session

from certs import install_intel_certs


class GLSession(Session):
    """a Session wrapper for github api"""
    def __init__(self, url, token):
        install_intel_certs()
        url = url.rstrip("/")
        self.hosted_url = url
        self.prefix_url = self.hosted_url + "/api/v4"
        super(GLSession, self).__init__()
        self.headers = {'PRIVATE-TOKEN': token,
                        'User-Agent': 'Gitlab_hooks'}

    def request(self, method, url, *args, **kwargs):
        url = self.prefix_url + url
        res = super(GLSession, self).request(method, url, *args, **kwargs)
        return res

    def setupHook(self, project_id, hook_url):
        if not isinstance(project_id, int):
            project_id = urllib.quote_plus(project_id)
        hooks = self.get("/projects/{}/hooks".format(project_id)).json()
        for hook in hooks:
            if hook['url'] == hook_url:
                return

        r = self.post("/projects/{}/hooks".format(project_id), json={
            "id": project_id,
            "url": hook_url,
            "push_events": True,
            "issues_events": True,
            "merge_requests_events": True,
            "tag_push_events": True,
            "note_events": True,
            "job_events": True,
            "pipeline_events": True,
            "wiki_page_events": True,
            "enable_ssl_verification": False
        })
        r.raise_for_status()
        print "created hook!", r.content
