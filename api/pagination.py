import uuid

from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def build_resource(self, resource):
        _id = resource["id"]
        url = self.request.build_absolute_uri()
        if "?" in url:
            url = url.split("?")[0]
        return {"resource": resource, "fullUrl": f"{url}{_id}"}

    def get_paginated_response(self, data):
        return Response(
            {
                "resourceType": "Bundle",
                "id": uuid.uuid4(),
                "type": "searchset",
                "total": self.page.paginator.count,
                "link": [
                    {"relation": "prev", "url": self.get_previous_link()},
                    {"relation": "next", "url": self.get_next_link()},
                ],
                "entry": list(map(self.build_resource, data)),
            }
        )
