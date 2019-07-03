user = self.request.user
permissions = set()
from django.contrib import auth
for backend in auth.get_backends():
    if hasattr(backend, "get_all_permissions"):
        permissions.update(backend.get_all_permissions(user))
sorted_list_of_permissions = sorted(list(permissions))
for perm in sorted_list_of_permissions:
    print(perm)
