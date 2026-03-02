# mkgen-core

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://github.com/YOUR_USERNAME/mkgen-core/workflows/Python%20application/badge.svg)

## A Lightweight, Extensible Markdown-based Static Site Generator Core

`mkgen-core` is the foundational engine for building static websites from Markdown files. It provides core functionalities for converting Markdown to HTML, extracting metadata, and rendering content using Jinja2 templates, designed to be easily integrated into larger static site generation frameworks or used as a standalone tool for simple projects.

### Features

*   **Markdown to HTML Conversion**: Leverages the `markdown` library with metadata support for robust conversion.
*   **Jinja2 Templating**: Flexible templating engine for custom layouts and dynamic content injection.
*   **Metadata Extraction**: Automatically extracts front matter (e.g., title, author) from Markdown files.
*   **Directory Traversal**: Processes Markdown files across nested directories.
*   **Clean Output**: Ensures a fresh build by clearing the output directory before generation.
*   **Extensible Design**: Built with an OOP approach, making it easy to extend or swap components.

### Project Structure

```
mkgen-core/
├── content/                # Input directory for Markdown files
│   ├── index.md
│   └── about/
│       └── us.md
├── templates/              # Jinja2 templates for page layouts
│   └── page.html
├── public/                 # Output directory for generated HTML (will be created)
├── main.py                 # Core application logic
├── test_main.py            # Unit tests
├── requirements.txt        # Python dependencies
├── README.md               # Project README (English)
├── README_de.md            # Project README (German)
├── CONTRIBUTING.md         # Contribution guidelines
├── LICENSE                 # MIT License
└── .github/                # GitHub Actions CI/CD workflows
    └── workflows/
        └── python-app.yml
```

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/mkgen-core.git
    cd mkgen-core
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

`mkgen-core` processes Markdown files from an input directory, applies templates, and outputs static HTML files to a specified output directory.

1.  **Prepare your content:** Create Markdown files in an `input_dir` (e.g., `content/`). You can include front matter at the top of your Markdown files for metadata:
    ```markdown
    ---
    title: My Awesome Page
    author: Jane Doe
    ---

    # Welcome to My Site

    This is the **content** of my page.
    ```

2.  **Prepare your templates:** Create Jinja2 HTML templates in a `template_dir` (e.g., `templates/`). A basic `page.html` might look like this:
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ title }}</title>
    </head>
    <body>
        <header>
            <h1>{{ title }}</h1>
        </header>
        <main>
            {{ content | safe }}
        </main>
        <footer>
            {% if metadata.author %}<p>By: {{ metadata.author }}</p>{% endif %}
            <p>Generated with mkgen-core</p>
        </footer>
    </body>
    </html>
    ```
    *   `{{ title }}`: Renders the page title (from Markdown front matter).
    *   `{{ content | safe }}`: Renders the converted HTML content from Markdown. `| safe` is crucial to prevent Jinja2 from escaping the HTML.
    *   `{{ metadata.author }}`: Accesses other front matter fields.

3.  **Run the generator:**
    You can run `main.py` directly as shown in the `if __name__ == "__main__":` block for a demonstration. For your own project, you would typically integrate `SiteGenerator` into your build script:

    ```python
    from main import SiteGenerator

    input_directory = 'content'
    output_directory = 'public'
    template_directory = 'templates'

    generator = SiteGenerator(
        input_dir=input_directory,
        output_dir=output_directory,
        template_dir=template_directory,
        default_template='page.html'
    )
    generator.generate()
    print(f"Site generated successfully in {output_directory}/")
    ```

### Running Tests

To run the unit tests, use the following command from the project root:

```bash
python -m unittest discover
```

### Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for guidelines on how to submit issues, features, and pull requests.

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.
