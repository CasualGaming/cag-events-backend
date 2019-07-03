from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import AllowAll


class LoginFailureView(APIView):

    permission_classes = [AllowAll]

    def get(self, request):
        content = {
            "message": "Login failed. Check the server log for details. If you were not trying to log in, disregard this message.",
        }
        return Response(content)
