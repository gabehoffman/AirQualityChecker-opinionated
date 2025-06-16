---
description: Engineering best practices, workflows, and standards for this project.
applyTo: "**"
---

# Engineering Best Practices

## Code Implementation

- **Code Organization**:
  - Every file starts with a brief 2-line "ABOUTME:" comment explaining its purpose
  - Organize code by domain functionality, not technical layers
  - Maintain clear separation of concerns between components
  - Limit function and method size to enhance readability

- **Style & Formatting**:
  - Match the style of surrounding code for consistency
  - Use automated formatting tools when available
  - Preserve existing whitespace that doesn't affect execution
  - Follow established naming conventions for the project

- **Code Quality**:
  - Eliminate code duplication through careful refactoring
  - Use appropriate design patterns to solve common problems
  - Implement proper error handling and validation
  - Write self-documenting code with meaningful names
  - Include type hints and parameter documentation

- **Dependency Management**:
  - Minimize external dependencies to reduce vulnerability surface
  - Pin dependency versions for reproducible builds
  - Regularly audit and update dependencies
  - Document the purpose of each dependency

## Version Control Workflow

- **Repository Management**:
  - Initialize git repositories for all projects
  - Create dedicated branches for each feature or bugfix
  - Commit uncommitted changes before starting new work
  - Use WIP branches when task boundaries are unclear

- **Commit Practices**:
  - Commit frequently with descriptive messages
  - Track all non-trivial changes in git
  - Structure commits logically around complete changes
  - Reference issue numbers in commit messages when applicable

## Comprehensive Testing Strategy

- **Test-Driven Development**:
  1. Write failing tests that validate desired functionality
  2. Run tests to confirm expected failure
  3. Implement minimal code to make tests pass
  4. Verify tests pass with implementation
  5. Refactor while maintaining passing tests

- **Test Coverage**:
  - Implement unit tests for all functions and methods
  - Create integration tests for component interactions
  - Develop end-to-end tests for critical user workflows
  - Avoid mocks in end-to-end tests; use real data and APIs

- **Test Quality**:
  - Ensure tests are deterministic and reliable
  - Maintain pristine test output without unexpected errors
  - Test edge cases and error conditions explicitly
  - Capture and verify expected error conditions

## Systematic Debugging Process

- **Investigation Phase**:
  - Read error messages thoroughly for diagnostic information
  - Establish consistent reproduction steps
  - Review recent changes that could have introduced the issue
  - Examine logs and system output for clues

- **Analysis Phase**:
  - Find and study similar working code
  - Compare against reference implementations
  - Identify specific differences between working and broken code
  - Understand all dependencies and requirements

- **Resolution Phase**:
  - Form a single, clear hypothesis about the root cause
  - Test with minimal changes to verify the hypothesis
  - Avoid implementing multiple fixes simultaneously
  - Reanalyze if initial fix doesn't resolve the issue

## Documentation Requirements

- **Code Documentation**:
  - Maintain all existing comments unless provably false
  - Write evergreen comments that describe code as it is
  - Document architectural decisions and their rationales
  - Include context for complex or non-obvious implementations

- **Knowledge Management**:
  - Maintain a journal of technical insights and learnings
  - Document unrelated issues discovered during development
  - Record failed approaches to prevent repetition
  - Track patterns in technical feedback