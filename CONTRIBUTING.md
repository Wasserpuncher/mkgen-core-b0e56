# Contributing to mkgen-core

We welcome contributions to `mkgen-core`! Whether it's reporting a bug, suggesting an enhancement, or submitting a pull request, your help is valuable.

Please take a moment to review this document before making your contribution.

## How to Contribute

### 1. Reporting Bugs

If you find a bug, please open an issue on our GitHub repository. When reporting a bug, please include:

*   A clear and concise description of the bug.
*   Steps to reproduce the behavior.
*   Expected behavior.
*   Actual behavior.
*   Screenshots or error messages, if applicable.
*   Your operating system and Python version.

### 2. Suggesting Enhancements

We're always looking for ways to improve `mkgen-core`. If you have an idea for a new feature or an improvement to an existing one, please open an issue. Describe the enhancement, its potential benefits, and any relevant use cases.

### 3. Submitting Pull Requests (PRs)

Follow these steps to contribute code:

1.  **Fork the repository:** Click the 'Fork' button on the top right of the GitHub page.
2.  **Clone your fork:** `git clone https://github.com/YOUR_USERNAME/mkgen-core.git`
3.  **Create a new branch:** `git checkout -b feature/your-feature-name` or `bugfix/your-bug-name`.
4.  **Make your changes:** Write your code, add tests, and update documentation as necessary.
    *   Ensure your code adheres to PEP 8 style guidelines.
    *   Add type hints and docstrings to new functions/methods.
    *   Write inline comments in German for code explanations.
5.  **Run tests:** Ensure all existing tests pass and your new tests cover your changes.
    `python -m unittest discover`
6.  **Commit your changes:** Use clear and concise commit messages. A good commit message explains *what* was changed and *why*.
    `git commit -m "feat: Add new feature for X"`
7.  **Push to your fork:** `git push origin feature/your-feature-name`
8.  **Open a Pull Request:** Go to the original `mkgen-core` repository on GitHub and click 'New Pull Request'.
    *   Provide a clear title and description for your PR.
    *   Reference any related issues (e.g., `Closes #123`).

### Code Style and Quality

*   **Python:** Follow PEP 8.
*   **Type Hinting:** Use type hints for function arguments and return values.
*   **Docstrings:** Provide clear docstrings for classes, methods, and functions.
*   **Comments:** Use inline comments in German to explain complex logic or non-obvious parts of the code.
*   **Tests:** All new features and bug fixes should be accompanied by appropriate unit tests.

Thank you for contributing to `mkgen-core`!
