# mkgen-core Architecture Deep Dive

`mkgen-core` is designed as a modular and extensible static site generator core. Its architecture is based on a clear separation of concerns, with distinct components responsible for specific tasks: Markdown processing, templating, and overall orchestration. This design promotes maintainability, testability, and flexibility for future enhancements.

## High-Level Overview

The core workflow of `mkgen-core` can be summarized in these steps:

1.  **Input Reading**: Read Markdown files from a specified source directory.
2.  **Markdown Processing**: Convert Markdown content into HTML and extract any associated metadata (front matter).
3.  **Templating**: Combine the generated HTML content and metadata with a Jinja2 template to produce a final HTML page.
4.  **Output Writing**: Write the rendered HTML page to a target output directory.
5.  **Orchestration**: A central `SiteGenerator` class manages this entire flow, iterating through input files and coordinating the other components.

## Component Breakdown

The project is structured around three primary classes, each encapsulating a core responsibility:

### 1. `MarkdownProcessor`

*   **Responsibility**: Handles the conversion of Markdown text into HTML and the extraction of structured metadata (front matter).
*   **Key Methods**:
    *   `__init__()`: Initializes the `markdown.Markdown` converter, specifically enabling the `meta` extension for front matter parsing.
    *   `convert(markdown_content: str) -> str`: Takes a raw Markdown string and returns its HTML representation. During this process, the `meta` extension populates the `self.md.Meta` attribute with any detected front matter.
    *   `extract_metadata() -> Dict[str, Any]`: Returns the metadata dictionary (`self.md.Meta`) from the last conversion. This dictionary typically contains lists of strings for each metadata field (e.g., `{'title': ['My Title'], 'author': ['John Doe']}`).
*   **Dependencies**: Relies on the external `markdown` library.
*   **Extensibility**: If different Markdown flavors or more advanced parsing features were needed (e.g., custom syntax highlighting), this class would be the primary point of modification or extension. One could swap out the `markdown` library for another parser or add custom extensions.

### 2. `TemplateEngine`

*   **Responsibility**: Manages the loading and rendering of HTML templates using the Jinja2 templating engine.
*   **Key Methods**:
    *   `__init__(template_dir: str)`: Initializes the Jinja2 `Environment`. It configures a `FileSystemLoader` to find templates within the specified `template_dir` and enables `select_autoescape` for security against XSS attacks.
    *   `render(template_name: str, context: Dict[str, Any]) -> str`: Loads a template by its `template_name` and populates it with data provided in the `context` dictionary. The `context` typically includes the converted HTML content and extracted metadata.
*   **Dependencies**: Relies on the external `Jinja2` library.
*   **Extensibility**: This component is highly flexible. Different template engines could be integrated by creating a new class adhering to a similar `render` interface. Custom filters, tests, or globals for Jinja2 could be added in its `__init__` method.

### 3. `SiteGenerator`

*   **Responsibility**: The orchestrator. It ties together the `MarkdownProcessor` and `TemplateEngine` to manage the end-to-end static site generation workflow. It handles file system operations (reading input, creating output directories, writing files).
*   **Key Methods**:
    *   `__init__(input_dir: str, output_dir: str, template_dir: str, default_template: str = 'page.html')`: Initializes the generator with input/output paths, the template directory, and the default template to use. It also instantiates `MarkdownProcessor` and `TemplateEngine`.
    *   `_ensure_output_dir() -> None`: Prepares the output directory. If it exists, it's cleared to ensure a clean build; otherwise, it's created.
    *   `_process_file(input_filepath: str) -> None`: The core logic for processing a single Markdown file. It reads the file, uses `MarkdownProcessor` to get HTML and metadata, prepares a context dictionary, uses `TemplateEngine` to render the final HTML, and writes the result to the appropriate path in the `output_dir`.
    *   `generate() -> None`: The main entry point for the generation process. It recursively walks through the `input_dir`, identifies Markdown files, and calls `_process_file` for each.
*   **Dependencies**: Depends on `MarkdownProcessor` and `TemplateEngine` instances, as well as Python's built-in `os` and `shutil` modules for file system interactions.
*   **Extensibility**: This class is designed to be the control center. Future features like copying static assets, handling different content types (e.g., JSON, YAML), implementing permalink structures, or adding a configuration layer would primarily involve modifications or extensions within this class or by introducing new helper classes that `SiteGenerator` orchestrates.

## Data Flow

1.  `SiteGenerator.generate()` initiates the process, scanning `input_dir`.
2.  For each `.md` file, `SiteGenerator._process_file()` is called.
3.  `_process_file` reads the Markdown content.
4.  `MarkdownProcessor.convert()` transforms Markdown to raw HTML and stores metadata.
5.  `MarkdownProcessor.extract_metadata()` retrieves the stored metadata.
6.  `_process_file` constructs a `context` dictionary containing the HTML content and metadata.
7.  `TemplateEngine.render()` uses the `context` to fill the `default_template`.
8.  `_process_file` writes the final rendered HTML to the corresponding path in `output_dir`.

## Future Considerations and Extensibility Points

*   **Configuration Layer**: Introduce a `Config` class (e.g., loading from `config.json` or `pyproject.toml`) to centralize settings like input/output directories, template paths, default templates, and potentially custom Markdown extensions.
*   **Static Asset Copying**: Extend `SiteGenerator` to identify and copy non-Markdown files (images, CSS, JS) from the `input_dir` to the `output_dir`.
*   **Permalink Structures**: Allow users to define custom URL structures for generated pages.
*   **Plugin System**: Implement a simple plugin architecture to allow users to hook into different stages of the generation process (e.g., pre-processing Markdown, post-processing HTML, custom data sources).
*   **Error Handling and Logging**: Enhance error reporting and add a robust logging mechanism.
*   **Command-Line Interface (CLI)**: Wrap the `SiteGenerator` in a CLI using libraries like `argparse` or `Click` for easier user interaction.
*   **Content Types**: Support other content types beyond Markdown, such as reStructuredText or AsciiDoc, by integrating different processors.

This modular design ensures that `mkgen-core` remains focused on its core responsibilities while providing clear pathways for growth and customization, making it a robust foundation for various static site generation needs.
