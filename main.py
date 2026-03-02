import os
import re
import shutil
from typing import Dict, Any, Optional

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

class MarkdownProcessor:
    """
    Verarbeitet Markdown-Inhalte, konvertiert sie in HTML und extrahiert Metadaten.
    Processes Markdown content, converts it to HTML, and extracts metadata.
    """
    def __init__(self) -> None:
        """
        Initialisiert den Markdown-Konverter mit der 'Meta-Data'-Erweiterung.
        Initializes the Markdown converter with the 'Meta-Data' extension.
        """
        # Initialisiert den Markdown-Konverter mit der 'Meta-Data'-Erweiterung, um Frontmatter zu verarbeiten.
        # Initializes the Markdown converter with the 'Meta-Data' extension to process front matter.
        self.md = markdown.Markdown(extensions=['meta'])

    def convert(self, markdown_content: str) -> str:
        """
        Konvertiert Markdown-Inhalte in HTML.
        Converts Markdown content to HTML.

        Args:
            markdown_content (str): Der zu konvertierende Markdown-String.

        Returns:
            str: Der resultierende HTML-String.
        """
        # Konvertiert den Markdown-Inhalt in HTML. Die Metadaten werden dabei intern gespeichert.
        # Converts the Markdown content to HTML. Metadata is stored internally during this process.
        return self.md.convert(markdown_content)

    def extract_metadata(self) -> Dict[str, Any]:
        """
        Extrahiert die Metadaten, die während der letzten Konvertierung gefunden wurden.
        Extracts metadata found during the last conversion.

        Returns:
            Dict[str, Any]: Ein Dictionary mit den extrahierten Metadaten.
                            Jeder Wert ist eine Liste von Strings (wie von der 'meta'-Erweiterung geliefert).
        """
        # Gibt die während der letzten Konvertierung gesammelten Metadaten zurück.
        # Returns the metadata collected during the last conversion.
        # Die 'meta'-Erweiterung speichert die Metadaten im 'meta'-Attribut des Markdown-Objekts.
        # The 'meta' extension stores metadata in the 'meta' attribute of the Markdown object.
        return self.md.Meta


class TemplateEngine:
    """
    Verwaltet das Laden und Rendern von Jinja2-Vorlagen.
    Manages loading and rendering Jinja2 templates.
    """
    def __init__(self, template_dir: str) -> None:
        """
        Initialisiert die Jinja2-Umgebung.
        Initializes the Jinja2 environment.

        Args:
            template_dir (str): Das Verzeichnis, in dem sich die Vorlagen befinden.
        """
        # Überprüft, ob das Vorlagenverzeichnis existiert, bevor die Jinja2-Umgebung initialisiert wird.
        # Checks if the template directory exists before initializing the Jinja2 environment.
        if not os.path.isdir(template_dir):
            raise ValueError(f"Vorlagenverzeichnis '{template_dir}' existiert nicht.")

        # Konfiguriert die Jinja2-Umgebung, um Vorlagen aus dem angegebenen Verzeichnis zu laden.
        # Setzt 'autoescape' auf True für Sicherheitsgründe, um XSS-Angriffe zu verhindern.
        # Configures the Jinja2 environment to load templates from the specified directory.
        # Sets 'autoescape' to True for security reasons to prevent XSS attacks.
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Rendert eine Vorlage mit den bereitgestellten Kontextdaten.
        Renders a template with the provided context data.

        Args:
            template_name (str): Der Name der zu rendernden Vorlage (z.B. 'page.html').
            context (Dict[str, Any]): Ein Dictionary von Daten, die an die Vorlage übergeben werden sollen.

        Returns:
            str: Der gerenderte HTML-String.
        """
        # Lädt die angegebene Vorlage und rendert sie mit dem bereitgestellten Kontext.
        # Loads the specified template and renders it with the provided context.
        template = self.env.get_template(template_name)
        return template.render(context)


class SiteGenerator:
    """
    Die Kernklasse, die den gesamten Prozess der Seitengenerierung orchestriert.
    The core class that orchestrates the entire site generation process.
    """
    def __init__(
        self, 
        input_dir: str, 
        output_dir: str, 
        template_dir: str, 
        default_template: str = 'page.html'
    ) -> None:
        """
        Initialisiert den SiteGenerator.
        Initializes the SiteGenerator.

        Args:
            input_dir (str): Das Verzeichnis, das die Markdown-Quelldateien enthält.
            output_dir (str): Das Verzeichnis, in das die generierten HTML-Dateien geschrieben werden sollen.
            template_dir (str): Das Verzeichnis, das die Jinja2-Vorlagen enthält.
            default_template (str): Der Name der Standardvorlage, die für alle Seiten verwendet wird.
        """
        # Speichert die Eingabe-, Ausgabe- und Vorlagenverzeichnisse.
        # Stores the input, output, and template directories.
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.template_dir = template_dir
        self.default_template = default_template

        # Initialisiert den Markdown-Prozessor und die Template-Engine.
        # Initializes the Markdown processor and template engine.
        self.markdown_processor = MarkdownProcessor()
        self.template_engine = TemplateEngine(template_dir)

    def _ensure_output_dir(self) -> None:
        """
        Stellt sicher, dass das Ausgabeverzeichnis existiert, und erstellt es, falls nicht.
        Löscht den Inhalt des Verzeichnisses, wenn es bereits existiert.
        Ensures the output directory exists, creating it if it doesn't.
        Clears the directory's content if it already exists.
        """
        # Überprüft, ob das Ausgabeverzeichnis existiert.
        # Checks if the output directory exists.
        if os.path.exists(self.output_dir):
            # Wenn es existiert, löscht es den Inhalt, um eine saubere Generierung zu gewährleisten.
            # If it exists, it deletes the content to ensure a clean generation.
            shutil.rmtree(self.output_dir)
        # Erstellt das Ausgabeverzeichnis neu, einschließlich aller übergeordneten Verzeichnisse.
        # Recreates the output directory, including any parent directories.
        os.makedirs(self.output_dir, exist_ok=True)

    def _process_file(self, input_filepath: str) -> None:
        """
        Verarbeitet eine einzelne Markdown-Datei: liest, konvertiert, rendert und schreibt HTML.
        Processes a single Markdown file: reads, converts, renders, and writes HTML.

        Args:
            input_filepath (str): Der vollständige Pfad zur Eingabe-Markdown-Datei.
        """
        # Überprüft, ob die Datei eine Markdown-Datei ist.
        # Checks if the file is a Markdown file.
        if not input_filepath.endswith('.md'):
            print(f"Überspringe nicht-Markdown-Datei: {input_filepath}")
            return

        print(f"Verarbeite Datei: {input_filepath}")

        # Liest den Inhalt der Markdown-Datei.
        # Reads the content of the Markdown file.
        with open(input_filepath, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Konvertiert Markdown zu HTML und extrahiert Metadaten.
        # Converts Markdown to HTML and extracts metadata.
        html_content = self.markdown_processor.convert(markdown_content)
        metadata = self.markdown_processor.extract_metadata()

        # Erstellt einen Kontext für die Vorlage.
        # Creates a context for the template.
        # Die Metadaten werden als Listen von Strings geliefert; wir nehmen den ersten Wert für einfache Felder.
        # Metadata is provided as lists of strings; we take the first value for simple fields.
        context = {
            'content': html_content,
            'title': metadata.get('title', [''])[0] if metadata.get('title') else 'Untitled Page',
            'metadata': {k: v[0] if v else '' for k, v in metadata.items()}
        }

        # Rendert die HTML-Seite mit der Standardvorlage und dem Kontext.
        # Renders the HTML page using the default template and context.
        rendered_html = self.template_engine.render(self.default_template, context)

        # Bestimmt den Ausgabedateipfad. Ersetzt '.md' durch '.html'.
        # Determines the output file path. Replaces '.md' with '.html'.
        relative_path = os.path.relpath(input_filepath, self.input_dir)
        output_filename = os.path.splitext(relative_path)[0] + '.html'
        output_filepath = os.path.join(self.output_dir, output_filename)

        # Stellt sicher, dass das Unterverzeichnis für die Ausgabedatei existiert.
        # Ensures that the subdirectory for the output file exists.
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

        # Schreibt die gerenderte HTML-Datei in das Ausgabeverzeichnis.
        # Writes the rendered HTML file to the output directory.
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        print(f"Generiert: {output_filepath}")

    def generate(self) -> None:
        """
        Startet den Generierungsprozess der statischen Website.
        Orchestrates the static site generation process.
        """
        print(f"Starte Generierung von '{self.input_dir}' nach '{self.output_dir}'...")

        # Stellt sicher, dass das Ausgabeverzeichnis vorbereitet ist.
        # Ensures the output directory is prepared.
        self._ensure_output_dir()

        # Durchläuft alle Dateien im Eingabeverzeichnis und seinen Unterverzeichnissen.
        # Iterates through all files in the input directory and its subdirectories.
        for root, _, files in os.walk(self.input_dir):
            for filename in files:
                # Erstellt den vollständigen Pfad zur Eingabedatei.
                # Creates the full path to the input file.
                input_filepath = os.path.join(root, filename)
                # Verarbeitet nur Markdown-Dateien.
                # Processes only Markdown files.
                if filename.endswith('.md'):
                    self._process_file(input_filepath)

        print("Generierung abgeschlossen.")


if __name__ == "__main__":
    # Beispiel für die Verwendung des SiteGenerators.
    # Example usage of the SiteGenerator.

    # Erstellt temporäre Verzeichnisse für das Beispiel.
    # Creates temporary directories for the example.
    temp_input_dir = 'content'
    temp_output_dir = 'public'
    temp_template_dir = 'templates'

    # Bereinigt alte temporäre Verzeichnisse, falls vorhanden.
    # Cleans up old temporary directories if they exist.
    if os.path.exists(temp_input_dir): shutil.rmtree(temp_input_dir)
    if os.path.exists(temp_output_dir): shutil.rmtree(temp_output_dir)
    if os.path.exists(temp_template_dir): shutil.rmtree(temp_template_dir)

    os.makedirs(temp_input_dir, exist_ok=True)
    os.makedirs(temp_template_dir, exist_ok=True)

    # Erstellt eine Beispiel-Markdown-Datei mit Metadaten.
    # Creates an example Markdown file with metadata.
    with open(os.path.join(temp_input_dir, 'index.md'), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("title: Willkommen bei MkGen\n")
        f.write("author: Max Mustermann\n")
        f.write("---\n")
        f.write("\n# Herzlich Willkommen!")
        f.write("\n\nDies ist die Startseite, generiert mit **MkGen-Core**.")
        f.write("\n\n*   Schnell
*   Einfach
*   Erweiterbar")

    # Erstellt eine weitere Beispiel-Markdown-Datei in einem Unterverzeichnis.
    # Creates another example Markdown file in a subdirectory.
    os.makedirs(os.path.join(temp_input_dir, 'about'), exist_ok=True)
    with open(os.path.join(temp_input_dir, 'about', 'us.md'), 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write("title: Über Uns\n")
        f.write("date: 2024-07-20\n")
        f.write("---\n")
        f.write("\n# Unsere Geschichte")
        f.write("\n\nWir sind ein Team von Enthusiasten, die glauben, dass statische Websites großartig sind.")

    # Erstellt eine Beispiel-Jinja2-Vorlage.
    # Creates an example Jinja2 template.
    with open(os.path.join(temp_template_dir, 'page.html'), 'w', encoding='utf-8') as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang=\"de\">\n")
        f.write("<head>\n")
        f.write("    <meta charset=\"UTF-8\">\n")
        f.write("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
        f.write("    <title>{{ title }} - Meine Statische Seite</title>\n")
        f.write("    <style>\n")
        f.write("        body { font-family: sans-serif; margin: 2em; line-height: 1.6; }\n")
        f.write("        h1, h2, h3 { color: #333; }\n")
        f.write("        .content { max-width: 800px; margin: 0 auto; padding: 1em; background: #f9f9f9; border-radius: 5px; }\n")
        f.write("        .metadata { font-size: 0.9em; color: #666; margin-top: 1em; border-top: 1px solid #eee; padding-top: 0.5em; }\n")
        f.write("    </style>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write("    <div class=\"content\">\n")
        f.write("        <header>\n")
        f.write("            <h1>{{ title }}</h1>\n")
        f.write("        </header>\n")
        f.write("        <main>\n")
        f.write("            {{ content | safe }}\n")
        f.write("        </main>\n")
        f.write("        <footer class=\"metadata\">\n")
        f.write("            {% if metadata.author %}<p>Autor: {{ metadata.author }}</p>{% endif %}\n")
        f.write("            {% if metadata.date %}<p>Datum: {{ metadata.date }}</p>{% endif %}\n")
        f.write("            <p>Generiert mit MkGen-Core</p>\n")
        f.write("        </footer>\n")
        f.write("    </div>\n")
        f.write("</body>\n")
        f.write("</html>\n")

    try:
        # Erstellt eine Instanz des SiteGenerators und startet die Generierung.
        # Creates an instance of SiteGenerator and starts the generation.
        generator = SiteGenerator(
            input_dir=temp_input_dir,
            output_dir=temp_output_dir,
            template_dir=temp_template_dir
        )
        generator.generate()

        print(f"\nStatische Website erfolgreich in '{temp_output_dir}' generiert.")
        print("Öffnen Sie 'public/index.html' in Ihrem Browser, um das Ergebnis zu sehen.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        # Optional: Bereinigt die temporären Verzeichnisse nach der Ausführung.
        # Optional: Cleans up temporary directories after execution.
        # shutil.rmtree(temp_input_dir)
        # shutil.rmtree(temp_output_dir)
        # shutil.rmtree(temp_template_dir)
        pass
