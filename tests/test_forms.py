from api.form_views import organization_view


def test_organization_view():
    class Request:
        @property
        def method(self):
            return "GET"

    r = Request()
    assert organization_view(r, None)
