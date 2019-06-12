# Keycloak (OIDC)

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
- `groups` (custom mapper, not full group path)

## User IDs
Users are identified by a shared UUID in Keycloak and CaG Events. Unique usernames from Keycloak are used to reference users in the CaG Events API. Since users are identified internally using an immutable UUID, changing a user's username shouldn't affect internal integrity.
