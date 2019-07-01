# Permission Conventions

Django permissions are added to migrations, so always remove the default permissions for every model before creating the first migration. AFAIK, permissions can never be removed once added.

## Removing and Replacing Default Permissions
Always remove default permissions from all models. If the model must be accessable in the Django admin panel, add new ones with the same codename instead (Django limitation).

Required codename format: `(view|add|change|delete)_<lowercase_model_name>` (e.g. `view_arealayout`)

Example default permissions for the `AreaLayout` model:
```python
from common.permissions import generate_default_permissions

default_permissions = []
permissions = [
    # ...
]
permissions += generate_default_permissions("AreaLayout", "seating area layout")
```

## Adding Custom Permissions
Add all permissions used in views etc. as custom permissions. Don't use the shady default permissions for anything except the Django admin panel (which requires them). Custom permissions can be logically shared between multiple models (e.g. `layout.<...>` instead of `area_layout.<...>` and `row_layout.<...>`), but must be defined within a model (e.g. `SeatingLayout`) (Django limitation).

Suggested codename format: `<lowercase_underscore_model_name>.(list|view|add|change|delete|...)` (e.g. `area_layout.view`)

Example custom permissions for the AreaLayout model:
```python
permissions = [
    ("layout.list", "List seating layouts"),
    ("layout.create", "Create seating layouts"),
    ("layout.change", "Change seating layouts"),
    ("layout.delete", "Delete seating layouts"),
    ("layout.view_inactive", "View inactive seating layouts"),
    # No "view" permission is added because active seatings are public
]
```

# Using Permissions
The full format of a permission is `<app_name>.<codename>`, e.g. `seating.area_layout.view`.

Permissions for a user can be checked directly (Django-style) like this:
```python
user.has_perm("<app_name>.<codename>")
```

Permissions for a user can be wrapped in a DRF permission object like this:
```python
from common.permissions import ModelPermission
ModelPermission("<app_name>.<codename>")
```
