#!/usr/bin/env python3
"""
PurpleBros Analytics - Rebranding Engine
Questo script viene invocato durante la GitHub Action per effettuare modifiche mirate
ai file grafici, ai titoli, ai layout e ai metadati, preservando il codice sorgente
di backend, database e dipendenze interne.
"""

import os
import re
import sys

def patch_layout_metadata():
    """Modifica i titoli delle schede del browser e i metadati Next.js."""
    layout_files = [
        "src/app/layout.tsx",
        "src/app/(main)/layout.tsx",
    ]
    
    patterns = [
        (r"default:\s*['\"]umami['\"]", "default: 'PurpleBros Analytics'"),
        (r"template:\s*['\"]%s\s*\|\s*umami['\"]", "template: '%s | PurpleBros Analytics'"),
        (r"title:\s*['\"]umami['\"]", "title: 'PurpleBros Analytics'"),
        (r"title:\s*['\"]Umami['\"]", "title: 'PurpleBros Analytics'"),
        (r"<title>Umami</title>", "<title>PurpleBros Analytics</title>"),
        (r"<title>umami</title>", "<title>PurpleBros Analytics</title>"),
    ]

    for file_path in layout_files:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            modified = False
            for pattern, replacement in patterns:
                new_content, count = re.subn(pattern, replacement, content)
                if count > 0:
                    content = new_content
                    modified = True

            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  ✔ Metadati aggiornati in: {file_path}")

def patch_messages():
    """Aggiorna le etichette di traduzione/messaggi visibili."""
    msg_files = [
        "src/components/messages.ts",
        "src/messages/en-US.json",
    ]

    for file_path in msg_files:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Sostituisce solo menzioni visibili e isolate
            new_content = re.sub(r'\bUmami\b', 'PurpleBros Analytics', content)
            new_content = re.sub(r'\bumami\b', 'PurpleBros Analytics', new_content)

            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"  ✔ File messaggi aggiornato: {file_path}")

def patch_jsx_branding_text():
    """Cerca e sostituisce testo visibile 'umami' nelle etichette e nei tag JSX."""
    target_dirs = ["src/app", "src/components"]
    
    for directory in target_dirs:
        if not os.path.exists(directory):
            continue
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith((".tsx", ".jsx")):
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8") as f:
                        text = f.read()

                    # Sostituzione sicura solo per elementi visibili tra tag JSX: >umami< o >Umami<
                    new_text, count = re.subn(r'>\s*umami\s*<', '>PurpleBros Analytics<', text, flags=re.IGNORECASE)
                    
                    if count > 0:
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.write(new_text)
                        print(f"  ✔ Testo JSX aggiornato ({count} occorrenze) in: {full_path}")

def patch_dockerfile():
    """Assicura che le icone SVG vengano rigenerate durante la compilazione dell'immagine Docker."""
    dockerfile_path = "Dockerfile"
    if os.path.exists(dockerfile_path):
        with open(dockerfile_path, "r", encoding="utf-8") as f:
            df = f.read()

        if "pnpm build:icons" not in df:
            if "RUN pnpm build:docker" in df:
                df = df.replace("RUN pnpm build:docker", "RUN pnpm build:icons\nRUN pnpm build:docker")
                with open(dockerfile_path, "w", encoding="utf-8") as f:
                    f.write(df)
                print("  ✔ Dockerfile aggiornato con step 'pnpm build:icons'")
            else:
                print("  ℹ Nessun comando 'pnpm build:docker' trovato nel Dockerfile standard.")

def main():
    print("=" * 60)
    print("🚀 Inizio Rebranding: PurpleBros Analytics")
    print("=" * 60)
    
    patch_layout_metadata()
    patch_messages()
    patch_jsx_branding_text()
    patch_dockerfile()
    
    print("=" * 60)
    print("✅ Rebranding completato con successo!")
    print("=" * 60)

if __name__ == "__main__":
    main()
