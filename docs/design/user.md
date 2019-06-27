# User Notes

## Login
Users can only log in through the configured OpenID Connect server. For every login, the user is required to have a set of attributes assigned to its OIDC user. The users' subject IDs are used to identify users.

## Creation
OIDC user account creation is handled by the OIDC server, e.g. through a public user registration form. App user accounts are automatically created when a user attempts to log into the app through OIDC if no accounts with a matching subject ID was found.

## Deletion
**TODO**

## Banning
**TODO**

## Membership
**TODO**
