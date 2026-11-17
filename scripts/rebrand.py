#!/usr/bin/env python3
"""
PurpleBros Analytics - Rebranding Engine
Questo script viene invocato durante la GitHub Action per effettuare modifiche mirate
ai componenti del logo, ai titoli, ai layout e ai metadati, preservando il codice sorgente
di backend, database e dipendenze interne.
"""

import base64
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

                    new_text, count = re.subn(r'>\s*umami\s*<', '>PurpleBros Analytics<', text, flags=re.IGNORECASE)
                    
                    if count > 0:
                        with open(full_path, "w", encoding="utf-8") as f:
                            f.write(new_text)
                        print(f"  ✔ Testo JSX aggiornato ({count} occorrenze) in: {full_path}")

def patch_logo_components():
    """
    Sostituisce direttamente i componenti Logo.tsx e LogoWhite.tsx in src/components/svg/
    senza dover eseguire SVGR (evitando di sovrascrivere o eliminare le altre icone di sistema).
    """
    badge_paths = [
        "../custom-config/branding/master-badge-scuro.png",
        "../custom-config/branding/favicon-32x32.png",
    ]
    
    badge_file = None
    for bp in badge_paths:
        if os.path.exists(bp):
            badge_file = bp
            break

    if not badge_file:
        print("  ⚠ Badge PNG non trovato per il componente Logo.")
        return

    with open(badge_file, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")

    logo_component_code = f"""import type {{ SVGProps }} from 'react';

const SvgLogo = (props: SVGProps<SVGSVGElement>) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 512 512"
    width={{20}}
    height={{20}}
    {{...props}}
  >
    <image href="data:image/png;base64,{b64_data}" width="512" height="512" />
  </svg>
);

export default SvgLogo;
"""

    logo_white_code = f"""import type {{ SVGProps }} from 'react';

const SvgLogoWhite = (props: SVGProps<SVGSVGElement>) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 512 512"
    width={{20}}
    height={{20}}
    {{...props}}
  >
    <image href="data:image/png;base64,{b64_data}" width="512" height="512" />
  </svg>
);

export default SvgLogoWhite;
"""

    target_files = [
        ("src/components/svg/Logo.tsx", logo_component_code),
        ("src/components/svg/LogoWhite.tsx", logo_white_code),
    ]

    for path, code in target_files:
        if os.path.exists(os.path.dirname(path)):
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"  ✔ Componente React sostituito: {path}")

def main():
    print("=" * 60)
    print("🚀 Inizio Rebranding: PurpleBros Analytics")
    print("=" * 60)
    
    patch_layout_metadata()
    patch_messages()
    patch_jsx_branding_text()
    patch_logo_components()
    
    print("=" * 60)
    print("✅ Rebranding completato con successo!")
    print("=" * 60)

if __name__ == "__main__":
    main()
