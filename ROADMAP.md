# PurpleBros Analytics - Roadmap & Architettura

Progetto di personalizzazione e automazione CI/CD per **Umami Analytics** self-hosted (Branding: **PurpleBros Analytics**).

---

## 🎯 Il Tuo Flusso Operativo Perfetto

1. **Rilevamento e Compilazione 100% Automatica:**
   * La GitHub Action si attiva ogni 6 ore in automatico (oppure tramite lancio manuale).
   * Controlla l'API di GitHub: se rileva una nuova release ufficiale stabile di Umami non ancora presente nel tuo repo, **la compila immediatamente con i tuoi asset e il brand PurpleBros Analytics** (configurata appositamente con `DATABASE_TYPE=postgresql`).
   * La nuova immagine viene pubblicata su GHCR come `:latest` e con il tag della versione (es. `:v2.14.0`).
2. **Watchtower in Sola Lettura (Monitor / Notifiche):**
   * Watchtower rileva che l'immagine `:latest` è stata aggiornata sul registry e ti invia una notifica.
3. **Decisione e Deploy Controllato da Portainer:**
   * Quando decidi tu (dopo aver lasciato sedimentare la nuova release per evitare bug della prima ora), apri Portainer ed esegui l'aggiornamento dello stack con la spunta **"Re-pull image"** (oppure **Recreate** sul container `umami`).

---

## 📂 Struttura del Repository Locale

Tutti i file sono archiviati in: `C:\Users\Max\Umami-Customization-x-Antigravity`

```text
C:\Users\Max\Umami-Customization-x-Antigravity\
├── .github/
│   └── workflows/
│       └── build.yml               # Pipeline GitHub Actions (Controllo auto ogni 6h + build PostgreSQL)
├── branding/
│   ├── README.md                   # Istruzioni sui file grafici da inserire
│   ├── logo.svg                    # [Da inserire] Nuovo logo vettoriale PurpleBros
│   ├── favicon.ico                 # [Da inserire] Favicon principale
│   ├── favicon-16x16.png           # [Opzionale]
│   ├── favicon-32x32.png           # [Opzionale]
│   └── apple-touch-icon.png        # [Opzionale]
├── scripts/
│   └── rebrand.py                  # Script Python per sostituzioni mirate (testo, titoli, Dockerfile)
├── docker-compose.portainer.yml    # Il tuo compose reale integrato con l'immagine PurpleBros
└── ROADMAP.md                      # Questa guida
```

---

## 🛣️ Guida Passo-Passo per la Messa in Produzione

### Passo 1: Inserisci i Tuoi File Grafici
* Copia il tuo file SVG in `branding/logo.svg`.
* Copia la tua favicon in `branding/favicon.ico`.

### Passo 2: Crea il Repository Privato su GitHub
1. Vai su GitHub e crea un nuovo repository (es. `purplebros-analytics`), impostato su **Private**.
2. Da terminale nella cartella locale:
   ```bash
   cd C:\Users\Max\Umami-Customization-x-Antigravity
   git init
   git add .
   git commit -m "feat: setup iniziale rebranding purplebros"
   git branch -M main
   git remote add origin https://github.com/VMax2/purplebros-analytics.git
   git push -u origin main
   ```

### Passo 3: Prima Compilazione su GitHub
1. Vai nella scheda **Actions** del repository GitHub.
2. Troverai il workflow **"Build PurpleBros Analytics"**.
3. Clicca **Run workflow** (lascia il campo vuoto per compilare l'ultima release stabile attuale).
4. In 3-4 minuti l'immagine verrà compilata e pubblicata su GHCR.

### Passo 4: Imposta la Visibilità del Pacchetto Docker su "Public" *(Consigliato)*
1. Sul tuo profilo GitHub, vai su **Packages** -> seleziona `purplebros-analytics`.
2. Clicca su **Package settings** in basso a destra.
3. Nella sezione *Danger Zone*, clicca **Change package visibility** e impostalo su **Public**.
   > **Nota sulla Sicurezza:** L'immagine non contiene password, token o credenziali di database (che restano confinate nel tuo Portainer). Rendendola pubblica, Watchtower e Portainer possono verificarla e scaricarla senza dover configurare Personal Access Token sul server.

### Passo 5: Aggiorna lo Stack su Portainer
Nel tuo Portainer:
1. Apri il tuo stack Umami esistente.
2. Sostituisci l'immagine con:
   ```yaml
   image: ghcr.io/TUO_USERNAME_GITHUB/purplebros-analytics:latest
   ```
   *(Puoi verificare il file completo in `docker-compose.portainer.yml`)*.
3. Clicca **Update the stack** spuntando **"Re-pull image"**.
