# Keycloak (OpenID Connect)

## Realm Settings and Authentication
- **TODO** Flows and executions and stuff.
- Create a single realm for all instances of CaG Events.
- Generel settings:
  - Set display name to the desired login prompt title.
- Login settings:
  - Enable: User registration, forgot password, remember me, verify email, login with email.
  - Disable: Edit username.
  - Require SSL for all requests.
- Configure email settings (use Mailgun or something).
- Token settings:
  - Increase SSO session idle and max to appropriate durations (too short is annoying).
- Configure ReCAPTCHA.
- Configure password policies.
- Configure terms and conditions.

## Realm Identity Providers and User Federation
- **TODO** Use social login through identity providers?

## Groups, Statuses and Permissions
- CaG Events maps OIDC groups to existing local groups.
- Users are disabled, are not staff, are not superadmin and have no permissions by default.
- Users are active, staff and superadmin if any of its groups are. They inherit all permissions from groups they are members of.
- Local groups with its statuses and permissions are configured completely locally, as opposed to being configured by Keycloak groups.
- CaG Events adds two default groups: "user" and "admin". Users in "user" can log into the site, users in "admin" have all permissions and have access to the admin panel.
- Keycloak users should have a default group such as "users", so that they can log into CaG Events.

## Clients
- **TODO** Export client for use as template?
- Create a client in Keycloak for every instance of CaG Events.
- Use access type confidential
- Use standard flow only (AKA authorization code flow), not implicit flow.
- Set valid redirect URIs (e.g. to `http://localhost:8000/oidc/*`)
- Use signed JWT with client secret as client authenticator. (**TODO** Is JWT needed? Client ID and secret works fine.)
- Add the needed mappers for the correct claims.

## User IDs
Users are identified by a shared UUID in Keycloak and CaG Events. Unique usernames from Keycloak are used to reference users in the CaG Events API. Since users are identified internally using an immutable UUID, changing a user's username or email address shouldn't affect internal consistency in Keycloak or CaG Events. UUIDs, usernames and email addresses must be unique.

## Required Claims
These claims are required for CaG Events to accept user logins. They can be implemented in Keycloak as user attributes and added as claims using client mappers (preferably builtin ones).

- `given_name` (profile mapper)
- `family_name` (profile mapper)
- `email` (profile mapper)
- `username` (username mapper) (unique, a-z, 0-9, _)
- `pretty_username` (??? mapper) (empty or username but with some letters as upper-case allowed)
- `birth_date` (birthdate mapper)
- `gender` (gender mapper)
- `phone_number` (phone number mapper)
- `country` (address mapper)
- `postal_code` (address mapper)
- `street_address` (address mapper)
- `groups` (custom group membership mapper, not full group path)
- `membership_years` (custom user attribute mapper)
