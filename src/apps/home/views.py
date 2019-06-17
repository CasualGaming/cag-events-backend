from rest_framework.response import Response
from rest_framework.views import APIView


root_path = "/v0/"

app_paths = [
    "user",
]


class Home(APIView):
    permission_classes = []

    def get(self, request):
        paths = [request.build_absolute_uri(root_path + app_path) for app_path in app_paths]
        return Response(paths)
