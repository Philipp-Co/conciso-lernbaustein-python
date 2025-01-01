# Serverkomponente

Dieser Server implementiert den zentralen Zugriff auf das Labyrinth.
Hier koennen Mitspieler sich anmelden und ihre Zuege veroeffentlichen.

# Den Server bearbeiten

Zunaechst eine venv erstellen

    python3.10 -m venv venv

Anschliessen die Venv aktivieren

    source venv/bin/activate

Danach die Requirements installieren

    pip install -r requirements.txt

Nun kann die Bearbeitung beginnen.

# Server Starten

Um den Server ohne Docker zu starten:

    ./manage.py runserver 0.0.0.0:8000 --settings labyrinth_server.settings

Siehe auch unter https://docs.djangoproject.com/en/5.1/intro/tutorial01/

# Docker

Um das Dockerimage zu bauen

    docker bla

# Docker Compose

Das Dockerimage kann ausserdem mit "docker compose" gebaut werden.

    docker compose build labyrinth_server

Starteb der Compose-Umgebung.

    docker compose up
