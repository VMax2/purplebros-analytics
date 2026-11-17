# Cartella Risorse Grafiche (Branding)

Posiziona qui dentro i file grafici per il tuo brand **PurpleBros Analytics**.

---

### File Supportati e Richiesti:

1. **`logo.svg`** *(Fondamentale)*
   * Il tuo logo in formato vettoriale SVG.
   * Verrà automaticamente convertito in componente React da SVGR durante la build e sostituirà l'icona/logo ufficiale nella barra di navigazione e nella schermata di login.
   * Suggerimento: mantieni un viewBox proporzionato (es. `0 0 32 32` o `0 0 100 100` o orizzontale).

2. **`favicon.ico`** *(Consigliato)*
   * La favicon del browser per la scheda.

3. **`favicon-16x16.png`** e **`favicon-32x32.png`** *(Opzionali)*
   * Icone ad alta definizione per browser desktop.

4. **`apple-touch-icon.png`** *(Opzionale)*
   * Icona visualizzata se l'applicazione viene aggiunta alla schermata Home di dispositivi iOS o Android (180x180 px).

---

> **Nota:** Tutti i file inseriti in questa cartella (ad eccezione di `logo.svg` che va in `src/assets/`) vengono copiati automaticamente nella cartella `public/` di Umami al momento del build.
