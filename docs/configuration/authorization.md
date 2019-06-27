# Authorization

## Overview
- The user is authenticated through Keycloak using OpenID Connect (OIDC).
- The app gets the user's subject ID and list of groups from OIDC, among other things.
- Logging into into an app account:
  - If no accounts have a matching subject ID, a new account is created and logged into.
  - If the app has an account with a matching subject ID, the user is logged into that account. If the username and/or email address are/is different, the account's username and/or email are updated.
  - When creating a new user or updating an existing user, if the username and/or email address matches any other account, the creation/update and subsequent login is rejected. Manual action by staff is required in order to resolve this problem, by e.g. updating the subject ID or deleting the other account.
- The user is given membership to all groups from OIDC which have an app group with a matching name. There should be a default user group that all users are member of.
- Users are not granted any permissions or other authorization-related statuses (like is-active, is-staff and is-superuser) directly, but inherit them from the groups it's member of.

## Statuses and Permissions
- Each group and user have a set of statuses and permissions.
- "Active" status: If the user can log into the app.
- "Staff" status: If the user can access the admin panel of the app (for the back-end).
- "Superuser" status: If the user has every possible permission.
- Permissions are manually assigned to groups and indicate which resources users can see and what actions users can perform.

## Groups
- Groups must be manually created in the app.
- By default, the app has a "user" group with the most basic user permission, and an "admin" group which grants its members staff and superuser status.

## Users
- Users are primarily identified by their subject ID, as given by OIDC. They also have unique usernames and email addresses. The username is the preferred way to identify users against the app API.
- Users are inactive, not staff, not superadmin and have no permissions by default, but inherit the "highest" of all it's groups' statuses and permissions.
