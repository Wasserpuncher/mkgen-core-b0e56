# mkgen-core Architektur im Detail

`mkgen-core` ist als modularer und erweiterbarer Kern für statische Website-Generatoren konzipiert. Seine Architektur basiert auf einer klaren Trennung der Verantwortlichkeiten, wobei einzelne Komponenten für spezifische Aufgaben zuständig sind: Markdown-Verarbeitung, Templating und die gesamte Orchestrierung. Dieses Design fördert die Wartbarkeit, Testbarkeit und Flexibilität für zukünftige Erweiterungen.

## Überblick auf hoher Ebene

Der Kern-Workflow von `mkgen-core` lässt sich in diesen Schritten zusammenfassen:

1.  **Eingabe lesen**: Lesen von Markdown-Dateien aus einem angegebenen Quellverzeichnis.
2.  **Markdown-Verarbeitung**: Konvertieren von Markdown-Inhalten in HTML und Extrahieren aller zugehörigen Metadaten (Frontmatter).
3.  **Templating**: Kombinieren der generierten HTML-Inhalte und Metadaten mit einer Jinja2-Vorlage, um eine endgültige HTML-Seite zu erstellen.
4.  **Ausgabe schreiben**: Schreiben der gerenderten HTML-Seite in ein Ziel-Ausgabeverzeichnis.
5.  **Orchestrierung**: Eine zentrale `SiteGenerator`-Klasse verwaltet diesen gesamten Fluss, indem sie die Eingabedateien durchläuft und die anderen Komponenten koordiniert.

## Komponentenaufschlüsselung

Das Projekt ist um drei primäre Klassen herum strukturiert, die jeweils eine Kernverantwortlichkeit kapseln:

### 1. `MarkdownProcessor`

*   **Verantwortlichkeit**: Handhabt die Konvertierung von Markdown-Text in HTML und die Extraktion von strukturierten Metadaten (Frontmatter).
*   **Schlüsselmethoden**:
    *   `__init__()`: Initialisiert den `markdown.Markdown`-Konverter, insbesondere durch Aktivierung der `meta`-Erweiterung für das Parsen von Frontmatter.
    *   `convert(markdown_content: str) -> str`: Nimmt einen rohen Markdown-String entgegen und gibt dessen HTML-Darstellung zurück. Während dieses Prozesses füllt die `meta`-Erweiterung das Attribut `self.md.Meta` mit allen erkannten Frontmatter-Informationen.
    *   `extract_metadata() -> Dict[str, Any]`: Gibt das Metadaten-Dictionary (`self.md.Meta`) der letzten Konvertierung zurück. Dieses Dictionary enthält typischerweise Listen von Strings für jedes Metadatenfeld (z.B. `{'title': ['Mein Titel'], 'author': ['Hans Mustermann']}`).
*   **Abhängigkeiten**: Basiert auf der externen `markdown`-Bibliothek.
*   **Erweiterbarkeit**: Wenn verschiedene Markdown-Dialekte oder fortgeschrittenere Parsing-Funktionen benötigt würden (z.B. benutzerdefinierte Syntaxhervorhebung), wäre diese Klasse der primäre Punkt für Änderungen oder Erweiterungen. Man könnte die `markdown`-Bibliothek durch einen anderen Parser ersetzen oder benutzerdefinierte Erweiterungen hinzufügen.

### 2. `TemplateEngine`

*   **Verantwortlichkeit**: Verwaltet das Laden und Rendern von HTML-Vorlagen mithilfe der Jinja2-Templating-Engine.
*   **Schlüsselmethoden**:
    *   `__init__(template_dir: str)`: Initialisiert die Jinja2 `Environment`. Es konfiguriert einen `FileSystemLoader`, um Vorlagen innerhalb des angegebenen `template_dir` zu finden, und aktiviert `select_autoescape` zur Sicherheit gegen XSS-Angriffe.
    *   `render(template_name: str, context: Dict[str, Any]) -> str`: Lädt eine Vorlage anhand ihres `template_name` und füllt sie mit den im `context`-Dictionary bereitgestellten Daten. Der `context` enthält typischerweise den konvertierten HTML-Inhalt und die extrahierten Metadaten.
*   **Abhängigkeiten**: Basiert auf der externen `Jinja2`-Bibliothek.
*   **Erweiterbarkeit**: Diese Komponente ist sehr flexibel. Verschiedene Template-Engines könnten integriert werden, indem eine neue Klasse erstellt wird, die eine ähnliche `render`-Schnittstelle einhält. Benutzerdefinierte Filter, Tests oder Globals für Jinja2 könnten in ihrer `__init__`-Methode hinzugefügt werden.

### 3. `SiteGenerator`

*   **Verantwortlichkeit**: Der Orchestrator. Er verbindet den `MarkdownProcessor` und die `TemplateEngine`, um den End-to-End-Workflow der statischen Website-Generierung zu verwalten. Er handhabt Dateisystemoperationen (Eingabe lesen, Ausgabeverzeichnisse erstellen, Dateien schreiben).
*   **Schlüsselmethoden**:
    *   `__init__(input_dir: str, output_dir: str, template_dir: str, default_template: str = 'page.html')`: Initialisiert den Generator mit Eingabe-/Ausgabepfaden, dem Vorlagenverzeichnis und der zu verwendenden Standardvorlage. Es instanziiert auch `MarkdownProcessor` und `TemplateEngine`.
    *   `_ensure_output_dir() -> None`: Bereitet das Ausgabeverzeichnis vor. Wenn es existiert, wird es geleert, um einen sauberen Build zu gewährleisten; andernfalls wird es erstellt.
    *   `_process_file(input_filepath: str) -> None`: Die Kernlogik zur Verarbeitung einer einzelnen Markdown-Datei. Es liest die Datei, verwendet `MarkdownProcessor`, um HTML und Metadaten zu erhalten, bereitet ein Kontext-Dictionary vor, verwendet `TemplateEngine`, um das endgültige HTML zu rendern, und schreibt das Ergebnis in den entsprechenden Pfad im `output_dir`.
    *   `generate() -> None`: Der Haupteinstiegspunkt für den Generierungsprozess. Es durchläuft rekursiv das `input_dir`, identifiziert Markdown-Dateien und ruft `_process_file` für jede auf.
*   **Abhängigkeiten**: Abhängig von `MarkdownProcessor`- und `TemplateEngine`-Instanzen sowie den integrierten Python-Modulen `os` und `shutil` für Dateisysteminteraktionen.
*   **Erweiterbarkeit**: Diese Klasse ist als Kontrollzentrum konzipiert. Zukünftige Funktionen wie das Kopieren statischer Assets, die Handhabung verschiedener Inhaltstypen (z.B. JSON, YAML), die Implementierung von Permalink-Strukturen oder das Hinzufügen einer Konfigurationsschicht würden hauptsächlich Änderungen oder Erweiterungen innerhalb dieser Klasse oder durch die Einführung neuer Hilfsklassen, die `SiteGenerator` orchestriert, erfordern.

## Datenfluss

1.  `SiteGenerator.generate()` initiiert den Prozess und scannt `input_dir`.
2.  Für jede `.md`-Datei wird `SiteGenerator._process_file()` aufgerufen.
3.  `_process_file` liest den Markdown-Inhalt.
4.  `MarkdownProcessor.convert()` wandelt Markdown in rohes HTML um und speichert Metadaten.
5.  `MarkdownProcessor.extract_metadata()` ruft die gespeicherten Metadaten ab.
6.  `_process_file` erstellt ein `context`-Dictionary, das den HTML-Inhalt und die Metadaten enthält.
7.  `TemplateEngine.render()` verwendet den `context`, um die `default_template` zu füllen.
8.  `_process_file` schreibt das endgültig gerenderte HTML in den entsprechenden Pfad im `output_dir`.

## Zukünftige Überlegungen und Erweiterungspunkte

*   **Konfigurationsschicht**: Einführung einer `Config`-Klasse (z.B. Laden aus `config.json` oder `pyproject.toml`), um Einstellungen wie Eingabe-/Ausgabeverzeichnisse, Vorlagenpfade, Standardvorlagen und potenziell benutzerdefinierte Markdown-Erweiterungen zu zentralisieren.
*   **Kopieren statischer Assets**: Erweiterung des `SiteGenerator`, um Nicht-Markdown-Dateien (Bilder, CSS, JS) aus dem `input_dir` zu identifizieren und in das `output_dir` zu kopieren.
*   **Permalink-Strukturen**: Ermöglichen Sie Benutzern, benutzerdefinierte URL-Strukturen für generierte Seiten zu definieren.
*   **Pluginsystem**: Implementierung einer einfachen Plugin-Architektur, um Benutzern das Einhaken in verschiedene Phasen des Generierungsprozesses zu ermöglichen (z.B. Vorverarbeitung von Markdown, Nachverarbeitung von HTML, benutzerdefinierte Datenquellen).
*   **Fehlerbehandlung und Protokollierung**: Verbesserung der Fehlerberichterstattung und Hinzufügen eines robusten Protokollierungsmechanismus.
*   **Kommandozeilenschnittstelle (CLI)**: Umhüllen des `SiteGenerator` in einer CLI mithilfe von Bibliotheken wie `argparse` oder `Click` für eine einfachere Benutzerinteraktion.
*   **Inhaltstypen**: Unterstützung anderer Inhaltstypen neben Markdown, wie reStructuredText oder AsciiDoc, durch Integration verschiedener Prozessoren.

Dieses modulare Design stellt sicher, dass `mkgen-core` sich auf seine Kernaufgaben konzentriert und gleichzeitig klare Wege für Wachstum und Anpassung bietet, was es zu einer robusten Grundlage für verschiedene Anforderungen an die Generierung statischer Websites macht.
