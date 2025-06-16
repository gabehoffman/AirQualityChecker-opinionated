---
description: Python and Django-specific conventions and requirements for this project.
applyTo: "**/*.py"
---

# Python and Django Specifics

## Development Environment
- Use a virtual environment for all development and deployment
- Use a dependency management tool (Poetry or pip-tools) with pinned versions
- Configure pre-commit hooks for automatic linting and formatting

## Code Quality
- Follow PEP 8 for code style and formatting
- Use type hints (PEP 484) for improved code clarity and editor support
- Use linters (flake8, pylint) and formatters (black, isort) consistently
- Keep cyclomatic complexity low (max 10) and functions focused on single responsibility
- Limit line length to 88 characters (black default)

## Django Project Structure
- Organize Django apps by domain functionality, not technical layers
- Keep settings modular with base, dev, test, and production configurations
- Use environment variables for all secrets and environment-specific settings
- Structure URLs hierarchically and name them consistently

## Security
- Use Django's built-in security features (CSRF, XSS, SQL injection protection)
- Enable and configure Django security middleware
- Never disable security features without documented justification
- Conduct regular security dependency checks (e.g., with safety)
- Use Django's password hashing and authentication system

## Data & Models
- Define explicit field types and constraints in models
- Use Django's migration system for all database changes
- Create custom model managers for complex querysets
- Implement proper related_name for all relationships
- Use select_related() and prefetch_related() for optimized queries
- Use F() and Q() objects for complex database operations

## Views & Templates
- Prefer class-based views for reusability and clarity
- Use function-based views for simple, one-off views when appropriate
- Implement proper permission checking at the view level
- Keep business logic in models or services, not in views
- Use Django forms for data validation, even in API contexts
- Structure templates with inheritance and reusable components

## APIs (if applicable)
- Use Django REST Framework with consistent serializer patterns
- Implement proper API versioning and documentation
- Apply rate limiting and throttling for API endpoints
- Use proper HTTP status codes and error handling

## Testing
- Write tests for models, views, forms, and custom logic
- Maintain minimum 80% test coverage for business logic
- Use pytest fixtures for reusable test components
- Mock external services in tests
- Include performance tests for critical paths

## Error Handling & Logging
- Configure proper logging for development and production
- Log all exceptions with appropriate context
- Create custom exception classes for domain-specific errors
- Handle errors gracefully and show user-friendly messages

## Performance
- Implement caching strategy for expensive operations
- Use Django's cached_property where appropriate
- Profile and optimize slow database queries
- Consider async views for IO-bound operations (Django 3.1+)

## Documentation
- Document all non-obvious code with docstrings
- Document custom management commands, signals, and middleware
- Maintain up-to-date API documentation
- Include setup instructions in README.md
