# Client Komponente

Hier implementieren Mitspieler ihren Client um auf das Labyrinth zuzugreifen.

## Aufbau

Fuer die Anweundung ist ein einfachers Schichtenmodell vorgesehen.

    +---------------+
    |   tests       |
    +---------------+
    |   interfaces  |
    +---------------+
    |   domain      |
    +---------------+
    |   models      |
    +---------------+

Interfaces enthaelt all die Logig die Schnittstellen zur Aussenwelt implementiert / ueber die ein Benutzer mit dem Skript interagieren kann.
Domain soll die Skiptlogik enthalten.
In Modells soll das Datenmodell des Skripts umgesetzt werden.

## venv

Eine virtuelle Entwicklungsumgebung erstellen.
    
    python -m venv my_venv
    source my_venv/bin/activate
    pip install -r requirements.txt    
    

## main.py

Das Skript ausfuehren

    main.py --help

um den Hilfe-Text anzuzeigen.

## Funktionsweise

Implementiere einen IClient im Ordner "interfaces". Ueber die "main.py" kann der erstellte IClient ueber den Aufruf ausgefuehrt werden.

    python main.py --class-name DefaulClient --module-path interfaces.default_client

## Entwicklung starten

Eine eigene Klasse unter interfaces/ anlegen, die von interfaces/iclient.py:IClient erbt.
Entsprechend der Schichtenarchitektur weitere Klassen und Funktionen anlegen. 
Waehrend der Umsetzung Unittests unter tests/ erstellen und die geschriebenen Klassen testen.

## Linter / Pre-Commit Hooks

Fuer dieses Projekt sind einige Linter vorkonfiguriert. Die Konfiguration und Ausfuehrung wird ueber das Tool pre-commit gemacht.

    pre-commit run --files ./*

## Unittests

Das Testprogramm sucht rekursiv in den Verzeichenissen nach Dateien mit dem Suffix "test_" und fuer die von TestCase erbenden Testmethoden aus.

    python -m unittest
