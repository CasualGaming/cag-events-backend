# Permission Conventions

## Default Permissions
Django automatically adds four default permissions for all models, which are used by the Django admin panel and should **not** be used for anything else, because they are trash. If you want to disallow creating, changing or deleting a model from the admin panel, customize `default_permissions` in the model's meta class.

Default permission codename format: `(view|add|change|delete)_<lowercase_model_name>` (e.g. `view_arealayout`)

Default default permissions (all): `default_permissions = ["view", "create", "change", "delete"]`

## Custom Permissions
Add all permissions used in views etc. as custom permissions. Don't use the shady default permissions for anything except the Django admin panel (which requires them).

Suggested codename format: `<lowercase_underscore_model_name>.(list|view|add|change|delete|...)` (e.g. `area_layout.view`)

All custom permissions for an app can (should) be added to a special model like this one:
```python
# Within the Authentication app
class Permissions(Model):
    class Meta:
        managed = False
        default_permissions = []
        permissions = [
            ("*", "Authentication app admin"),
            ("user.*", "User admin"),
            ("user.list", "List users"),
            ("user.view_basic", "View users' non-address info"),
            ("user.view_address", "View users' address"),
            ("user.delete", "Delete users"),
        ]
]
```

## Using Permissions
The full format of a permission is `<app_name>.<codename>`, e.g. `seating.area_layout.view`.

Permissions for a user can be checked directly (Django-style) like this:
```python
user.has_perm("<app_name>.<codename>")
```

Permissions for a user can be wrapped in a DRF permission object like this:
```python
from common.permissions import StringPermission
StringPermission("<app_name>.<codename>")
```

Both permissions classes and instantiated permissions can be AND'ed together by separating them with a comma (all supplied permissions must pass). While permissions classes can me OR'ed together using `|`, instantiated permissions can be OR'ed like this:
```python
from common.permissions import DisjunctionPermission
DisjunctionPermission(PermA, PermB, ...)
```

For more advanced expressions of OR and AND, ConjunctionPermission can be used together with DisjunctionPermission.
