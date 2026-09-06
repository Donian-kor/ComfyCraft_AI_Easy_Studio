# Project AI Instructions

## User

* The user is a Python beginner with very limited ability to read and understand code.
* Always communicate with the user in Korean.
* Explain technical concepts in simple Korean.
* Avoid unnecessary programming terminology.
* When technical terms are necessary, explain them briefly in simple Korean.
* When reporting changes, clearly explain:

  1. What was changed.
  2. Why it was changed.
  3. Which files were changed.
  4. How the change was verified.
* Do not assume the user understands programming terminology.

---

## Core Principles

* Inspect the project before making changes.
* Understand the existing implementation before modifying it.
* Do not guess when the required information can be obtained by inspecting the project.
* Preserve existing functionality unless the user explicitly requests otherwise.
* Make the smallest necessary change.
* Preserve the existing architecture and coding style whenever possible.
* Do not rewrite large portions of existing code unnecessarily.
* Do not modify unrelated files.
* Do not introduce duplicate functionality.
* Do not rename, move, or delete files unless necessary.
* Do not replace working code merely because another implementation appears cleaner.
* Do not claim something is fixed unless it has actually been verified.

---

## Large Project Analysis

This is a potentially large and interconnected project.

Do not assume that a single file contains all relevant logic.

Before modifying code:

1. Identify the relevant feature or problem.
2. Search the project for related files, functions, classes, variables, signals, slots, imports, configuration values, and resources.
3. Determine how the relevant components interact.
4. Inspect callers and dependencies when appropriate.
5. Inspect configuration and resource files that may affect the behavior.
6. Check whether the same functionality already exists elsewhere.
7. Identify the smallest safe set of files that actually need modification.

When a change affects multiple components, inspect all relevant components before editing.

Do not stop after finding the first apparently relevant file.

For large or unfamiliar changes, briefly summarize the discovered structure before making modifications.

---

## Change Planning

Before making a non-trivial change:

1. Explain the intended approach in simple Korean.
2. Identify the files expected to change.
3. Identify possible side effects.
4. Then make the changes.

For very small and obvious fixes, a separate detailed plan is not required.

Do not make unrelated improvements during the requested task.

Do not refactor existing code unless it is necessary to solve the requested problem.

---

## Python

* Follow the Python version already used by the project.
* Follow existing project dependencies.
* Do not introduce new dependencies unless necessary.
* Follow existing coding patterns and architecture.
* Prefer simple, readable Python suitable for a beginner.
* Avoid unnecessarily advanced syntax or architecture.
* Use clear names for functions, classes, and variables.
* Preserve existing APIs and interfaces unless a change is required.
* Consider backward compatibility when modifying shared functions or classes.
* Handle errors in a way consistent with the existing project.
* Do not silently swallow exceptions unless the existing design explicitly does so.

---

## GUI

First identify which GUI framework the project uses:

* PySide6
* PyQt5
* PyQt6
* Another framework

Do not mix GUI framework syntax.

Preserve the existing UI architecture unless the user explicitly requests a redesign.

Preserve Qt Designer compatibility when applicable.

Do not manually rewrite generated Qt Designer code unless necessary.

Do not change QSS, colors, fonts, layouts, icons, or visual styling unless requested.

Preserve existing signal/slot relationships.

When modifying UI behavior, inspect both the UI definition and the Python logic controlling it.

Long-running operations must not block the main GUI thread.

Use the project's existing threading, worker, signal, or asynchronous architecture when available.

---

## File Changes

* Inspect a file before modifying it.
* Modify only the necessary parts.
* Preserve existing code style and architecture.
* Avoid unnecessary formatting changes.
* Avoid changing line endings or file encoding unnecessarily.
* Be especially careful with:

  * UI files
  * QSS files
  * configuration files
  * JSON/XML files
  * resource files
  * generated files
  * project structure

Do not modify generated files if the project provides a source file or generator that should be changed instead.

---

## Configuration

Before changing configuration:

1. Inspect the existing configuration.
2. Determine which application or component uses it.
3. Preserve existing options unless they are directly related to the requested change.
4. Do not invent configuration keys.
5. Verify that configuration syntax is valid.
6. Check whether the application actually reads the modified configuration.

---

## Dependencies

Before adding a dependency:

* Check whether an existing dependency already provides the required functionality.
* Check the project's dependency files.
* Avoid adding a package for a problem that can be solved with the existing standard library or project dependencies.
* Do not upgrade or downgrade unrelated packages.
* Do not modify dependency versions unless required.

---

## Debugging

When investigating an error:

1. Read the complete error message.
2. Identify the file and line involved.
3. Inspect the surrounding code.
4. Trace the relevant call path when necessary.
5. Check related configuration and dependencies.
6. Determine the actual root cause.
7. Make the smallest appropriate fix.
8. Verify that the fix works.

Do not blindly patch the line mentioned in an error message without understanding why the error occurred.

If the root cause cannot be confirmed, clearly state that it has not been confirmed.

---

## Verification

After making changes:

1. Check for syntax errors.
2. Run the project's existing tests when available.
3. Run the relevant application or validation command when practical.
4. Check for obvious import, configuration, or runtime errors.
5. Verify that the requested behavior actually works.
6. Confirm that unrelated functionality was not unnecessarily changed.

If full verification cannot be performed, explicitly state what was and was not verified.

Never say "fixed" when the change has not been verified.

---

## Git and Existing Changes

* Preserve the user's existing uncommitted changes.
* Do not overwrite unrelated user modifications.
* Do not reset, revert, or discard user changes unless explicitly requested.
* Before making a potentially destructive change, inspect the current state.
* Do not create commits unless the user explicitly asks for a commit.

---

## Communication

Always answer the user in Korean.

Keep explanations beginner-friendly.

When a task is complete, use this structure when appropriate:

### 변경 내용

* What changed.

### 변경 파일

* Files that were modified.

### 확인 결과

* What was tested or verified.

### 참고

* Any remaining limitations, warnings, or things the user should know.

Do not overwhelm the user with unnecessary technical details.

When the user asks for a code change, prioritize actually making the change over giving a long theoretical explanation.
