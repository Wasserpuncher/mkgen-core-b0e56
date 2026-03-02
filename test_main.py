import unittest
import os
import shutil
import tempfile

from main import MarkdownProcessor, TemplateEngine, SiteGenerator

class TestMarkdownProcessor(unittest.TestCase):
    """
    Testfälle für die MarkdownProcessor-Klasse.
    Test cases for the MarkdownProcessor class.
    """
    def setUp(self) -> None:
        """
        Richtet einen neuen MarkdownProcessor für jeden Test ein.
        Sets up a new MarkdownProcessor for each test.
        """
        # Erstellt eine neue Instanz des MarkdownProcessors vor jedem Test.
        # Creates a new instance of MarkdownProcessor before each test.
        self.processor = MarkdownProcessor()

    def test_convert_basic_markdown(self) -> None:
        """
        Testet die Konvertierung von einfachem Markdown in HTML.
        Tests the conversion of basic Markdown to HTML.
        """
        markdown_content = "# Hallo Welt\n\nDies ist ein **Test**."
        expected_html = "<h1>Hallo Welt</h1>\n<p>Dies ist ein <strong>Test</strong>.</p>"
        # Konvertiert den Markdown-Inhalt und überprüft, ob das Ergebnis dem erwarteten HTML entspricht.
        # Converts the Markdown content and checks if the result matches the expected HTML.
        self.assertEqual(self.processor.convert(markdown_content).strip(), expected_html.strip())

    def test_extract_metadata(self) -> None:
        """
        Testet die Extraktion von Metadaten aus Markdown-Frontmatter.
        Tests the extraction of metadata from Markdown front matter.
        """
        markdown_content = """
---
title: Meine Seite
author: John Doe
---
# Inhalt
"""
        # Konvertiert den Markdown-Inhalt, um die Metadaten zu laden.
        # Converts the Markdown content to load the metadata.
        self.processor.convert(markdown_content)
        metadata = self.processor.extract_metadata()
        # Überprüft, ob die extrahierten Metadaten korrekt sind.
        # Checks if the extracted metadata is correct.
        self.assertIn('title', metadata)
        self.assertEqual(metadata['title'][0], 'Meine Seite')
        self.assertIn('author', metadata)
        self.assertEqual(metadata['author'][0], 'John Doe')

    def test_metadata_empty_if_none(self) -> None:
        """
        Testet, dass Metadaten leer sind, wenn kein Frontmatter vorhanden ist.
        Tests that metadata is empty if no front matter is present.
        """
        markdown_content = "# Kein Frontmatter"
        # Konvertiert den Markdown-Inhalt ohne Metadaten.
        # Converts the Markdown content without metadata.
        self.processor.convert(markdown_content)
        metadata = self.processor.extract_metadata()
        # Überprüft, ob das Metadaten-Dictionary leer ist.
        # Checks if the metadata dictionary is empty.
        self.assertEqual(metadata, {})


class TestTemplateEngine(unittest.TestCase):
    """
    Testfälle für die TemplateEngine-Klasse.
    Test cases for the TemplateEngine class.
    """
    def setUp(self) -> None:
        """
        Richtet ein temporäres Vorlagenverzeichnis und eine TemplateEngine ein.
        Sets up a temporary template directory and a TemplateEngine.
        """
        # Erstellt ein temporäres Verzeichnis für Vorlagen.
        # Creates a temporary directory for templates.
        self.temp_template_dir = tempfile.mkdtemp()
        # Erstellt eine Beispielvorlage im temporären Verzeichnis.
        # Creates an example template in the temporary directory.
        with open(os.path.join(self.temp_template_dir, 'test_template.html'), 'w', encoding='utf-8') as f:
            f.write("<h1>{{ title }}</h1><p>{{ content }}</p>")
        # Initialisiert die TemplateEngine mit dem temporären Verzeichnis.
        # Initializes the TemplateEngine with the temporary directory.
        self.engine = TemplateEngine(self.temp_template_dir)

    def tearDown(self) -> None:
        """
        Entfernt das temporäre Vorlagenverzeichnis nach den Tests.
        Removes the temporary template directory after tests.
        """
        # Löscht das temporäre Verzeichnis und seinen Inhalt.
        # Deletes the temporary directory and its content.
        shutil.rmtree(self.temp_template_dir)

    def test_render_template(self) -> None:
        """
        Testet das Rendern einer einfachen Vorlage mit Kontext.
        Tests rendering a simple template with context.
        """
        context = {'title': 'Test Seite', 'content': 'Dies ist der Inhalt.'}
        expected_html = "<h1>Test Seite</h1><p>Dies ist der Inhalt.</p>"
        # Rendert die Vorlage und überprüft das Ergebnis.
        # Renders the template and checks the result.
        self.assertEqual(self.engine.render('test_template.html', context), expected_html)

    def test_render_template_with_no_context(self) -> None:
        """
        Testet das Rendern einer Vorlage ohne Kontext.
        Tests rendering a template without context.
        """
        # Erstellt eine Vorlage, die keine Kontextvariablen verwendet.
        # Creates a template that does not use context variables.
        with open(os.path.join(self.temp_template_dir, 'no_context.html'), 'w', encoding='utf-8') as f:
            f.write("<html><body>Hello</body></html>")
        expected_html = "<html><body>Hello</body></html>"
        # Rendert die Vorlage mit einem leeren Kontext.
        # Renders the template with an empty context.
        self.assertEqual(self.engine.render('no_context.html', {}), expected_html)

    def test_template_not_found(self) -> None:
        """
        Testet das Verhalten, wenn eine Vorlage nicht gefunden wird.
        Tests the behavior when a template is not found.
        """
        # Erwartet, dass ein TemplateNotFound-Fehler ausgelöst wird.
        # Expects a TemplateNotFound error to be raised.
        from jinja2 import TemplateNotFound
        with self.assertRaises(TemplateNotFound):
            self.engine.render('non_existent_template.html', {})

    def test_template_dir_not_found(self) -> None:
        """
        Testet die Initialisierung, wenn das Vorlagenverzeichnis nicht existiert.
        Tests initialization when the template directory does not exist.
        """
        # Erwartet, dass ein ValueError ausgelöst wird, wenn das Verzeichnis ungültig ist.
        # Expects a ValueError to be raised if the directory is invalid.
        with self.assertRaises(ValueError):
            TemplateEngine('/path/to/nonexistent/templates')


class TestSiteGenerator(unittest.TestCase):
    """
    Testfälle für die SiteGenerator-Klasse.
    Test cases for the SiteGenerator class.
    """
    def setUp(self) -> None:
        """
        Richtet temporäre Eingabe-, Ausgabe- und Vorlagenverzeichnisse ein.
        Sets up temporary input, output, and template directories.
        """
        # Erstellt temporäre Verzeichnisse für Eingabe, Ausgabe und Vorlagen.
        # Creates temporary directories for input, output, and templates.
        self.temp_input_dir = tempfile.mkdtemp()
        self.temp_output_dir = tempfile.mkdtemp()
        self.temp_template_dir = tempfile.mkdtemp()

        # Erstellt eine Standardvorlage im temporären Vorlagenverzeichnis.
        # Creates a default template in the temporary template directory.
        with open(os.path.join(self.temp_template_dir, 'page.html'), 'w', encoding='utf-8') as f:
            f.write("<!DOCTYPE html><html lang=\"en\"><head><title>{{ title }}</title></head><body><h1>{{ title }}</h1><main>{{ content | safe }}</main><footer>{{ metadata.author }}</footer></body></html>")

        # Erstellt eine Beispiel-Markdown-Datei im temporären Eingabeverzeichnis.
        # Creates an example Markdown file in the temporary input directory.
        with open(os.path.join(self.temp_input_dir, 'test_page.md'), 'w', encoding='utf-8') as f:
            f.write("---\ntitle: Test Page\nauthor: Jane Doe\n---\n# This is a test\n\nContent goes here.")

        # Erstellt eine weitere Markdown-Datei in einem Unterverzeichnis.
        # Creates another Markdown file in a subdirectory.
        os.makedirs(os.path.join(self.temp_input_dir, 'subfolder'), exist_ok=True)
        with open(os.path.join(self.temp_input_dir, 'subfolder', 'nested_page.md'), 'w', encoding='utf-8') as f:
            f.write("---\ntitle: Nested Page\n---\n## Nested Content")

        # Erstellt eine Nicht-Markdown-Datei, die ignoriert werden sollte.
        # Creates a non-Markdown file that should be ignored.
        with open(os.path.join(self.temp_input_dir, 'ignored.txt'), 'w', encoding='utf-8') as f:
            f.write("This should be ignored.")

        # Initialisiert den SiteGenerator.
        # Initializes the SiteGenerator.
        self.generator = SiteGenerator(
            input_dir=self.temp_input_dir,
            output_dir=self.temp_output_dir,
            template_dir=self.temp_template_dir
        )

    def tearDown(self) -> None:
        """
        Entfernt alle temporären Verzeichnisse nach den Tests.
        Removes all temporary directories after tests.
        """
        # Löscht alle temporären Verzeichnisse.
        # Deletes all temporary directories.
        shutil.rmtree(self.temp_input_dir)
        shutil.rmtree(self.temp_output_dir)
        shutil.rmtree(self.temp_template_dir)

    def test_generate_single_page(self) -> None:
        """
        Testet die Generierung einer einzelnen Markdown-Datei zu HTML.
        Tests the generation of a single Markdown file to HTML.
        """
        # Führt den Generierungsprozess aus.
        # Executes the generation process.
        self.generator.generate()

        # Überprüft, ob die Ausgabedatei existiert.
        # Checks if the output file exists.
        output_filepath = os.path.join(self.temp_output_dir, 'test_page.html')
        self.assertTrue(os.path.exists(output_filepath))

        # Liest den Inhalt der generierten HTML-Datei.
        # Reads the content of the generated HTML file.
        with open(output_filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Überprüft den Inhalt der HTML-Datei.
        # Checks the content of the HTML file.
        self.assertIn('<title>Test Page</title>', content)
        self.assertIn('<h1>Test Page</h1>', content)
        self.assertIn('<h1>This is a test</h1>', content)
        self.assertIn('<p>Content goes here.</p>', content)
        self.assertIn('<footer>Jane Doe</footer>', content)

    def test_generate_nested_page(self) -> None:
        """
        Testet die Generierung einer Markdown-Datei in einem Unterverzeichnis.
        Tests the generation of a Markdown file in a subdirectory.
        """
        # Führt den Generierungsprozess aus.
        # Executes the generation process.
        self.generator.generate()

        # Überprüft, ob die Ausgabedatei im korrekten Unterverzeichnis existiert.
        # Checks if the output file exists in the correct subdirectory.
        output_filepath = os.path.join(self.temp_output_dir, 'subfolder', 'nested_page.html')
        self.assertTrue(os.path.exists(output_filepath))

        # Liest den Inhalt der generierten HTML-Datei.
        # Reads the content of the generated HTML file.
        with open(output_filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Überprüft den Inhalt der HTML-Datei.
        # Checks the content of the HTML file.
        self.assertIn('<title>Nested Page</title>', content)
        self.assertIn('<h1>Nested Page</h1>', content)
        self.assertIn('<h2>Nested Content</h2>', content)

    def test_output_dir_cleared(self) -> None:
        """
        Testet, dass das Ausgabeverzeichnis vor der Generierung geleert wird.
        Tests that the output directory is cleared before generation.
        """
        # Erstellt eine Dummy-Datei im Ausgabeverzeichnis.
        # Creates a dummy file in the output directory.
        dummy_file = os.path.join(self.temp_output_dir, 'old_file.html')
        with open(dummy_file, 'w') as f:
            f.write('Old content')

        # Führt den Generierungsprozess aus.
        # Executes the generation process.
        self.generator.generate()

        # Überprüft, dass die Dummy-Datei gelöscht wurde.
        # Checks that the dummy file has been deleted.
        self.assertFalse(os.path.exists(dummy_file))

    def test_non_markdown_files_ignored(self) -> None:
        """
        Testet, dass Nicht-Markdown-Dateien ignoriert werden.
        Tests that non-Markdown files are ignored.
        """
        # Führt den Generierungsprozess aus.
        # Executes the generation process.
        self.generator.generate()

        # Überprüft, dass die 'ignored.txt'-Datei nicht in den Ausgabedateien ist.
        # Checks that the 'ignored.txt' file is not among the output files.
        output_ignored_file = os.path.join(self.temp_output_dir, 'ignored.txt')
        self.assertFalse(os.path.exists(output_ignored_file))


if __name__ == '__main__':
    unittest.main()
