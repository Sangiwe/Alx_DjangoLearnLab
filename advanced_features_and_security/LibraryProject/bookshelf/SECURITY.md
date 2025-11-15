# Security configuration notes

- DEBUG = False for production.
- Cookie security enabled via CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE in production.
- CSP implemented via django-csp middleware (see settings).
- All forms include {% csrf_token %}.
- Views use Django forms and ORM to prevent SQL injection.
- Permissions enforced with @permission_required for sensitive endpoints.
- SECRET_KEY and other secrets stored in env vars.
