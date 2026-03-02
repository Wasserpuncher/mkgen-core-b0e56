# mkgen-core

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://github.com/YOUR_USERNAME/mkgen-core/workflows/Python%20application/badge.svg)

## Ein leichter, erweiterbarer Kern für Markdown-basierte statische Website-Generatoren

`mkgen-core` ist die grundlegende Engine zum Erstellen statischer Websites aus Markdown-Dateien. Es bietet Kernfunktionen für die Konvertierung von Markdown in HTML, die Extraktion von Metadaten und das Rendern von Inhalten mithilfe von Jinja2-Vorlagen. Es wurde entwickelt, um einfach in größere Frameworks zur Generierung statischer Websites integriert oder als eigenständiges Tool für einfache Projekte verwendet zu werden.

### Funktionen

*   **Markdown-zu-HTML-Konvertierung**: Nutzt die `markdown`-Bibliothek mit Metadatenunterstützung für eine robuste Konvertierung.
*   **Jinja2-Templating**: Flexible Vorlagen-Engine für benutzerdefinierte Layouts und dynamische Inhaltseinfügung.
*   **Metadaten-Extraktion**: Extrahiert automatisch Frontmatter (z.B. Titel, Autor) aus Markdown-Dateien.
*   **Verzeichnisdurchlauf**: Verarbeitet Markdown-Dateien über verschachtelte Verzeichnisse hinweg.
*   **Saubere Ausgabe**: Sorgt für einen frischen Build, indem das Ausgabeverzeichnis vor der Generierung geleert wird.
*   **Erweiterbares Design**: Mit einem OOP-Ansatz aufgebaut, was die Erweiterung oder den Austausch von Komponenten erleichtert.

### Projektstruktur

```
mkgen-core/
├── content/                # Eingabeverzeichnis für Markdown-Dateien
│   ├── index.md
│   └── about/
│       └── us.md
├── templates/              # Jinja2-Vorlagen für Seitenlayouts
│   └── page.html
├── public/                 # Ausgabeverzeichnis für generiertes HTML (wird erstellt)
├── main.py                 # Hauptanwendungslogik
├── test_main.py            # Unit-Tests
├── requirements.txt        # Python-Abhängigkeiten
├── README.md               # Projekt README (Englisch)
├── README_de.md            # Projekt README (Deutsch)
├── CONTRIBUTING.md         # Richtlinien für Beiträge
├── LICENSE                 # MIT-Lizenz
└── .github/                # GitHub Actions CI/CD-Workflows
    └── workflows/
        └── python-app.yml
```

### Installation

1.  **Repository klonen:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/mkgen-core.git
    cd mkgen-core
    ```

2.  **Virtuelle Umgebung erstellen (empfohlen):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Unter Windows: .\venv\Scripts\activate
    ```

3.  **Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```

### Verwendung

`mkgen-core` verarbeitet Markdown-Dateien aus einem Eingabeverzeichnis, wendet Vorlagen an und gibt statische HTML-Dateien in ein angegebenes Ausgabeverzeichnis aus.

1.  **Inhalte vorbereiten:** Erstellen Sie Markdown-Dateien in einem `input_dir` (z.B. `content/`). Sie können Frontmatter am Anfang Ihrer Markdown-Dateien für Metadaten hinzufügen:
    ```markdown
    ---
    title: Meine fantastische Seite
    author: Johanna Mustermann
    ---

    # Willkommen auf meiner Seite

    Dies ist der **Inhalt** meiner Seite.
    ```

2.  **Vorlagen vorbereiten:** Erstellen Sie Jinja2-HTML-Vorlagen in einem `template_dir` (z.B. `templates/`). Eine einfache `page.html` könnte so aussehen:
    ```html
    <!DOCTYPE html>
    <html lang="de">
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
            {% if metadata.author %}<p>Von: {{ metadata.author }}</p>{% endif %}
            <p>Generiert mit mkgen-core</p>
        </footer>
    </body>
    </html>
    ```
    *   `{{ title }}`: Rendert den Seitentitel (aus dem Markdown-Frontmatter).
    *   `{{ content | safe }}`: Rendert den konvertierten HTML-Inhalt aus Markdown. `| safe` ist entscheidend, um zu verhindern, dass Jinja2 das HTML escaped.
    *   `{{ metadata.author }}`: Greift auf andere Frontmatter-Felder zu.

3.  **Generator ausführen:**
    Sie können `main.py` direkt ausführen, wie im `if __name__ == "__main__":`-Block zur Demonstration gezeigt. Für Ihr eigenes Projekt würden Sie `SiteGenerator` typischerweise in Ihr Build-Skript integrieren:

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
    print(f"Website erfolgreich generiert in {output_directory}/")
    ```

### Tests ausführen

Um die Unit-Tests auszuführen, verwenden Sie den folgenden Befehl aus dem Projekt-Root-Verzeichnis:

```bash
python -m unittest discover
```

### Mitwirken

Wir freuen uns über Beiträge! Bitte lesen Sie `CONTRIBUTING.md` für Richtlinien zum Einreichen von Problemen, Funktionen und Pull-Requests.

### Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert – Details finden Sie in der Datei `LICENSE`.
