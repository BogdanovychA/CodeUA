# Project Instructions: CodeUA

## UI & Architecture
- **State Management**:
    - Use the `PandorasBox` dataclass (from `utils.models`) as a unified container for application state (`lang`, `audio`, `storage` and all session variables).
    - **FORBIDDEN**: Do not use `page.session.store`. All state must be packed into `box: PandorasBox`.
- **Localization**: Use `box.lang` (`FluentManager`) for all localized strings.
- **Audio Handling**:
    - **DO NOT** add `fta.Audio` objects to `page.overlay`. This is considered a legacy/unnecessary practice in this project's current architecture.
    - Reference the audio player via `box.audio`.

## Development Workflow
- **Refactoring**: When modifying UI components, ensure they accept the `box: PandorasBox` parameter where state access is required.
- **Imports**: Maintain clean imports and use `TYPE_CHECKING` blocks for complex types to avoid circular dependencies and unnecessary runtime overhead.
