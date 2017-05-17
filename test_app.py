import app
import mock

sample = {"owner_name": "Someone", "name": "Ruby", "event_name": "project_create",
          "owner_email": "example@gitlabhq.com", "path": "ruby", "project_id": 1}


def test_basic():
    app.gitlab = mock.Mock()
    app.hook_url = "hook_url"
    app.do_event(sample)
    app.gitlab.setupHook.assert_called_with(1, app.hook_url)
