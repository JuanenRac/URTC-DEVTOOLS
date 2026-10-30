<p align="center">
  <img src="images/URTC_DEVTOOLS_BANNER.svg" alt="URTC-DEVTOOLS banner" width="100%">
</p>

# 🧰 URTC-DEVTOOLS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | 🇮🇹 <b>Italiano</b> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 简体中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Gli strumenti di repository condivisi della famiglia URTC come un insieme versionato, con un file di lock in ogni repository

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Python%20%2B%20JSON-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Tests-16-2ea44f.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Controllo di onestà - cosa funziona oggi:** questo repository contiene i dieci file che i repository della famiglia portano come la stessa copia, un piccolo strumento che li elenca e controlla le copie che il repository porta, test e documentazione. Tutto viene eseguito e testato in CI. Il file di lock è scritto e controllato da URTC-DOCS; finora solo questo repository ne porta uno, gli altri non hanno ancora preso l'insieme, e niente qui è stato eseguito su hardware.

---

## 📋 In breve

| | |
|---|---|
| Versione | `0.0.1` |
| Maturità | Impalcatura |
| Test | 16 (`python -m unittest discover -s tests`) |
| Tecnologia | Python / GitHub Actions / JSON |
| Destinazione | Il PC di chi lo usa |
| Su hardware reale | Non applicabile: nulla qui gira su hardware |

**Vai a:** [Panoramica](#-panoramica) · [Architettura](#-architettura) · [Avvio rapido](#-avvio-rapido) · [Test](#-test) · [Struttura](#-struttura-del-repository) · [Correlati](#-progetti-correlati)

## 🚦 Stato del progetto

🟢 fatto e verificato · 🟡 funziona, con limiti noti · 🟠 a metà o non verificato · 🔴 non fatto o non funzionante. Nulla è verde se non ha mai girato su hardware reale.

| Parte | Stato | Ciò che il repository può dimostrare |
| --- | :---: | --- |
| Software | 🟡 | L'insieme, il suo elenco e il suo controllo; eseguito solo su un computer. |
| Test | 🟡 | La suite di test passa nella CI a ogni push. |
| Sicurezza | 🟠 | Il lock registra hash SHA-256 per trovare una modifica o una copia rimasta indietro; è un controllo di coerenza, non una firma. |
| Documentazione | 🟡 | README in otto lingue e formato del lock; le traduzioni non sono state riviste da madrelingua. |

## 🎯 Panoramica

Gli strumenti che ogni repository della famiglia porta come la stessa copia, riuniti in un solo posto e dotati di una versione:

* [`files/`](files): la copia canonica dei dieci file condivisi (i controlli della politica di documentazione e della parità dei README, i generatori di immagini, il pannello dal vivo degli script di build, lo strumento che alza la versione del manifesto, il controllo delle luci di stato e l'avviso alla dashboard). Il nome del repository è scritto `<REPO>` e sostituito quando un file viene messo in un repository.
* La **versione di questo repository è la versione dell'insieme**; il [registro delle modifiche](CHANGELOG.md) dice cosa è cambiato in ogni versione.
* Un **file di lock** in ogni repository, `tools/devtools.lock.json`, scritto da `tools/sync_repo_tools.py` di URTC-DOCS: la versione dell'insieme e lo SHA-256 di ogni copia. `tools/check_repo_tools.py` trova una copia modificata a mano e, quando questo repository è accanto agli altri, una copia rimasta indietro. Vedi [il formato del lock](docs/LOCK_FORMAT.md).
* Ogni repository resta compilabile e controllabile con il proprio checkout: il lock è un file del repository e nulla richiede la rete.

## 🧩 Ruolo in URTC

URTC-DEVTOOLS è il posto in cui gli strumenti condivisi ricevono un nome e una versione. Cambiarne uno significava cambiare una decina di repository senza che nulla dicesse quale versione portasse ciascuno; ora l'insieme ha una versione, ogni repository dice quale ha preso, e una copia modificata o rimasta indietro viene segnalata. Da solo non cambia nulla nei repository: URTC-DOCS mette i file e scrive i lock, un repository alla volta.

## 🏛️ Architettura

<p align="center">
  <img src="images/architecture.svg" alt="Architettura di URTC-DEVTOOLS: chi prende l'insieme, cosa contiene e cosa scrive" width="100%">
</p>

Come si incastrano le parti di questo repository: chi prende l'insieme, cosa contiene e cosa scrive in ogni repository. L'immagine è disegnata da `docs/architecture.json` e verificata rispetto al codice.

## 🚀 Avvio rapido

**Requisiti:** Python 3.10 o più recente; nient'altro.

```bash
python tools/devtools_set.py list            # la versione dell'insieme e lo SHA-256 di ogni file
python tools/devtools_set.py check           # le copie di questo repository sono i file canonici
python -m unittest discover -s tests         # i test
python tools/sync_repo_tools.py --apply      # da URTC-DOCS: mettere l'insieme e i lock nei repository accanto
```

## 🧪 Test

La suite ha 16 test (`python -m unittest discover -s tests`). Verificano che `files/` contenga esattamente i file condivisi, che ciascuno sia valido e si generi con il nome di un repository, che una copia modificata o mancante venga trovata, che il lock di questo repository corrisponda ai suoi file e alla sua versione, oltre a manifesto, registro delle modifiche e documenti. Un test confronta `files/` con il modello di URTC-DOCS e viene saltato quando quel repository non è accanto. La logica del lock è testata in URTC-DOCS.

## 🏗️ Compilazione e rilascio

`build.sh` / `build.bat` alzano la versione dell'insieme, controllano le copie ed eseguono i test; `build-test.sh` / `build-test.bat` controllano senza cambiare alcuna versione; `run.sh` / `run.bat` elencano l'insieme. Una nuova versione dell'insieme si fa cambiando un file in `files/` e la sua copia, alzando la versione una sola volta per tutto il lotto e prendendo l'insieme nei repository; vedi [la guida](docs/TAKING_THE_SET.md).

## 📂 Struttura del repository

<p align="center">
  <img src="images/repository-structure.svg" alt="Struttura del repository URTC-DEVTOOLS" width="100%">
</p>

<details>
<summary>Versione testuale dell'albero</summary>

```text
URTC-DEVTOOLS/
├── files/                                     i dieci file canonici, nel percorso che hanno in ogni repository
├── tools/                                     il controllo dell'insieme, la validazione del repository e le copie che porta
├── tests/                                     test dell'insieme, del lock e del repository
├── docs/                                      il formato del lock e come prendere l'insieme
├── .github/                                   CI, confronto notturno, modelli di issue e pull request
├── images/                                    banner e immagini di questo README
├── build.sh build.bat                         script di build
├── build-test.sh build-test.bat               script di build e test che non cambiano nulla nel repository
├── test.sh test.bat                           eseguono i test
├── run.sh run.bat                             elencano l'insieme o lo controllano
├── urtc.project.json                          manifesto: versione, ruolo, maturità e comando di build
├── CHANGELOG.md                               cosa è cambiato in ogni versione
├── SECURITY.md SUPPORT.md LICENSE             politica di sicurezza, supporto e licenza
├── CONTRIBUTING.md CODE_OF_CONDUCT.md         come contribuire e codice di condotta
├── .gitattributes .gitignore                  impostazioni di Git
├── bump_version.py bump_manifest_version.py   script che alzano la versione
└── pyproject.toml ruff.toml                   dati del progetto e impostazioni di lint
```

</details>

## 🗺️ Roadmap e limiti noti

**Limiti noti oggi**

* Il lock è scritto e controllato da URTC-DOCS; questo è finora l'unico repository che ne porta uno.
* URTC-DOCS conserva ancora il proprio modello, che il sincronizzatore legge; un test confronta i due quando sono accanto.
* I file che esistono anche nei progetti fratelli non vengono spostati qui da soli: lo stesso file in tutte le famiglie, o nessuno.
* Niente qui è stato eseguito su hardware; gli strumenti girano su un computer.

**Prossimi passi**

* Portare i repository della famiglia al lock uno alla volta.
* Fare di questo repository la fonte letta dal sincronizzatore e ritirare il modello di URTC-DOCS.

## 🌍 Lingue

README e testi esistono in inglese, spagnolo, francese, italiano, tedesco, cinese, giapponese e portoghese europeo.

## 🔗 Progetti correlati

URTC è fatto di repository indipendenti, ciascuno con la propria versione, i propri test e il proprio README. Ecco la famiglia, per gruppi:

* **URTC Tool Platform:**
  * [URTC](https://github.com/JuanenRac/URTC) - firmware della scheda della testa utensile (25 profili utensile, bootloader CAN) e riferimento del protocollo CAN.
  * [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) - il protocollo CAN scritto una sola volta come dati (specifica, tabelle generate, vettori di conformità) e il codice condiviso dai programmi.
  * [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) - strumento desktop che aggiorna il firmware della scheda via CAN o via SWD/JTAG.
  * [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) - gateway davanti al bus CAN: lascia passare solo gli identificatori di un elenco, ne limita la frequenza e chiede una chiave di sessione.
  * [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) - logica C indipendente dall'hardware e protocollo di comandi per un portautensili con preriscaldamento e tracciamento del ciclo di vita.
  * [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) - tester desktop del bus CAN in tempo reale che mostra i comandi e la telemetria del profilo utensile segnalato da una scheda.
  * [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) - protocollo di frame del sensore in C e un companion Python termico/RGB per una testa utensile di ispezione.
  * [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) - app per browser che programma e collauda la scheda via Web Serial e SLCAN, senza installare nulla.
* **Ecosystem Operations:**
  * **URTC-DEVTOOLS** (questo repository) - gli strumenti di repository condivisi della famiglia come un insieme versionato, con un file di lock che distingue una copia modificata da una rimasta indietro.
  * [URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS) - architettura, interfacce, base di sicurezza e catalogo generato dell'ecosistema, più gli strumenti che confrontano tutti i repository.
  * [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) - strumento desktop che rileva, installa e aggiorna i repository della famiglia URTC, un'azione esplicita alla volta.

**Progetti fratelli (indipendenti, con la stessa base e gli stessi strumenti):**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - progetto fratello: il centro di documentazione di HYDRA-UMC, un ecosistema indipendente che condivide base e strumenti con questo
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - progetto fratello: il centro di documentazione di A.R.M.O.R., l'ecosistema di sicurezza, anch'esso indipendente e sulla stessa base
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - il profilo e il pannello di stato di tutti gli ecosistemi

## 📚 Documentazione

Dove leggere di più:

* [Il formato del lock e cosa viene controllato](docs/LOCK_FORMAT.md)
* [Prendere l'insieme e fare una nuova versione](docs/TAKING_THE_SET.md)
* [Registro delle modifiche di questo repository](CHANGELOG.md)
* [Licenza (GPL-3.0-or-later)](LICENSE)
* Domande, idee e segnalazioni: electrohobby3d@gmail.com

## 🤝 Contribuire e comunità

* Prima di una pull request esegui `URTC_CI=1 python tools/ci_validate.py`: deve passare. Vedi [CONTRIBUTING.md](CONTRIBUTING.md) e il [codice di condotta](CODE_OF_CONDUCT.md).
* Il README esiste in otto lingue: una modifica al testo si fa in tutti e otto i file.
* Non descrivere come funzionante su una scheda ciò che è stato solo compilato.
* Segnala una vulnerabilità in privato: [SECURITY.md](SECURITY.md). Domande, idee e segnalazioni: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTORE

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENZA

GPL-3.0-or-later - vedi [LICENSE](LICENSE).
