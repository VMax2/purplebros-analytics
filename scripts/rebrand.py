#!/usr/bin/env python3
"""
PurpleBros Analytics - Rebranding Engine v2
Rifiniture estetiche:
- Titoli scheda del browser: sostituzione di tutti i template %s | Umami con %s | PurpleBros Analytics
- Favicon cache-buster: aggiunta di ?v=2 in src/app/layout.tsx per forzare il refresh su Cloudflare e browser
- Dimensione logo login: ingrandito a 80x80px
- Dimensione logo sidebar: ingrandito a 26x26px
"""

import base64
import os
import re
import sys

def patch_layout_metadata():
    """Modifica i titoli delle schede del browser e aggiunge il cache-buster ai link delle favicon."""
    print("  🔍 Ricerca e sostituzione metadati layout in src/app...")
    
    app_dir = "src/app"
    if not os.path.exists(app_dir):
        print(f"  ⚠ Cartella {app_dir} non trovata.")
        return

    for root, _, files in os.walk(app_dir):
        for file in files:
            if file.endswith((".tsx", ".ts")):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                modified = False

                # Sostituzione dei template di titolo (es. %s | Umami, %s | Admin | Umami, ecc.)
                new_content, count1 = re.subn(
                    r"template:\s*['\"][^'\"]*\|\s*Umami['\"]",
                    "template: '%s | PurpleBros Analytics'",
                    content,
                    flags=re.IGNORECASE
                )
                if count1 > 0:
                    content = new_content
                    modified = True

                # Sostituzione dei default title (es. default: 'Umami', default: 'Websites | Umami', ecc.)
                new_content, count2 = re.subn(
                    r"default:\s*['\"][^'\"]*Umami['\"]",
                    "default: 'PurpleBros Analytics'",
                    content,
                    flags=re.IGNORECASE
                )
                if count2 > 0:
                    content = new_content
                    modified = True

                # Sostituzione title semplici
                new_content, count3 = re.subn(
                    r"title:\s*['\"]Umami['\"]",
                    "title: 'PurpleBros Analytics'",
                    content,
                    flags=re.IGNORECASE
                )
                if count3 > 0:
                    content = new_content
                    modified = True

                # Cache-buster per favicon in layout.tsx
                if file == "layout.tsx":
                    cache_replacements = [
                        ('href="/favicon.ico"', 'href="/favicon.ico?v=2"'),
                        ('href="/apple-touch-icon.png"', 'href="/apple-touch-icon.png?v=2"'),
                        ('href="/favicon-32x32.png"', 'href="/favicon-32x32.png?v=2"'),
                        ('href="/favicon-16x16.png"', 'href="/favicon-16x16.png?v=2"'),
                    ]
                    for target, replacement in cache_replacements:
                        if target in content:
                            content = content.replace(target, replacement)
                            modified = True
                            print(f"    ✔ Cache-buster aggiunto: {replacement}")

                if modified:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"  ✔ Metadati/Titoli aggiornati in: {file_path}")

def patch_login_logo_size():
    """Ingrandisce il logo nella schermata di login, 2FA e logout a 100x100px (stile WordPress login)."""
    target_files = [
        "src/app/login/LoginForm.tsx",
        "src/app/login/two-factor/LoginTwoFactorPage.tsx",
        "src/app/logout/LogoutPage.tsx",
    ]

    for file_path in target_files:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Sostituisce <Icon size="lg"><Logo /></Icon> con <Logo style={{ width: 100, height: 100 }} />
            new_content = re.sub(
                r'<Icon[^>]*>\s*<Logo\s*/>\s*</Icon>',
                '<Logo style={{ width: 100, height: 100 }} />',
                content
            )
            new_content = re.sub(
                r'<Icon[^>]*>\s*<LogoWhite\s*/>\s*</Icon>',
                '<LogoWhite style={{ width: 100, height: 100 }} />',
                new_content
            )

            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"  ✔ Logo login ingrandito a 100x100px in: {file_path}")

def patch_logo_components():
    """
    Sostituisce i componenti Logo.tsx e LogoWhite.tsx in src/components/svg/
    impostando le dimensioni di default a 26x26px per una resa perfetta nella sidebar.
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

    # default width={26} height={26} per la sidebar
    logo_component_code = f"""import type {{ SVGProps }} from 'react';

const SvgLogo = (props: SVGProps<SVGSVGElement>) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 512 512"
    width={{26}}
    height={{26}}
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
    width={{26}}
    height={{26}}
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
            print(f"  ✔ Componente React (26px) scritto in: {path}")

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

def main():
    print("=" * 60)
    print("🚀 Inizio Rebranding e Rifiniture: PurpleBros Analytics")
    print("=" * 60)
    
    patch_layout_metadata()
    patch_login_logo_size()
    patch_logo_components()
    patch_messages()
    patch_jsx_branding_text()
    
    print("=" * 60)
    print("✅ Rebranding e rifiniture completate!")
    print("=" * 60)

if __name__ == "__main__":
    main()
