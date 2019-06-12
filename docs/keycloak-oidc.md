# Keycloak (OIDC)

## Realm Settings

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

## Realm Authentication
- **TODO** Flows and executions.
- Configure ReCAPTCHA.
- Configure password policies.
- Configure terms and conditions.

## Realm Identity Providers and User Federation
- **TODO** Use social login through identity providers?

## Clients
- **TODO** Export client for use as template?
- Create a client in Keycloak for every instance of CaG Events.
- Use access type confidential
- Use standard flow only (AKA authorization code flow), not implicit flow.
- Set valid redirect URIs (e.g. to `http://localhost:8000/oidc/*`)
- Use signed JWT with client secret as client authenticator. (**TODO** Is JWT needed? Client ID and secret works fine.)
- Add the needed mappers for the correct claims.

## User IDs
Users are identified by a shared UUID in Keycloak and CaG Events. Unique usernames from Keycloak are used to reference users in the CaG Events API. Since users are identified internally using an immutable UUID, changing a user's username shouldn't affect internal integrity.

## Required Claims
These claims are required for CaG Events to accept user logins. They can be implemented in Keycloak as user attributes and added as claims using client mappers (preferably builtin ones).

- `given_name` (profile mapper)
- `family_name` (profile mapper)
- `email` (profile mapper)
- `username` (username mapper)
- `birth_date` (birthdate mapper)
- `gender` (gender mapper)
- `phone_number` (phone number mapper)
- `country` (address mapper)
- `postal_code` (address mapper)
- `street_address` (address mapper)
- `groups` (custom group membership mapper, not full group path)
- `membership_years` (custom user attribute mapper)
