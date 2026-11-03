<p align="center">
  <img src="images/URTC_DEVTOOLS_BANNER.svg" alt="URTC-DEVTOOLS banner" width="100%">
</p>

# 🧰 URTC-DEVTOOLS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | 🇩🇪 <b>Deutsch</b> | <a href="README_zho.md">🇨🇳 简体中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Die gemeinsamen Repository-Werkzeuge der URTC-Familie als versionierter Satz, mit einer Sperrdatei in jedem Repository

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Python%20%2B%20JSON-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Tests-28-2ea44f.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Ehrlichkeits-Check - was heute wirklich läuft:** Dieses Repository enthält die 15 Dateien, die die Repositories der Familie als dieselbe Kopie tragen, ein kleines Werkzeug, das sie auflistet und die Kopien des Repositorys selbst prüft, Tests und Dokumentation. Alles läuft und wird in der CI getestet. Die Sperrdatei schreibt und prüft URTC-DOCS; bisher trägt nur dieses Repository eine, die anderen haben den Satz noch nicht übernommen, und nichts davon lief auf Hardware.

---

## 📋 Auf einen Blick

| | |
|---|---|
| Version | `0.0.2` |
| Reifegrad | Gerüst |
| Tests | 28 (`python -m unittest discover -s tests`) |
| Technik | Python / GitHub Actions / JSON |
| Ziel | Der PC der Person, die es benutzt |
| Auf echter Hardware | Nicht zutreffend: nichts hiervon läuft auf Hardware |

**Springe zu:** [Überblick](#-überblick) · [Architektur](#-architektur) · [Schnellstart](#-schnellstart) · [Tests](#-tests) · [Struktur](#-struktur-des-repositorys) · [Verwandte](#-verwandte-projekte)

## 🚦 Projektstatus

🟢 fertig und überprüft · 🟡 funktioniert, mit bekannten Grenzen · 🟠 halb fertig oder nicht überprüft · 🔴 nicht gemacht oder funktioniert nicht. Nichts ist grün, wenn es nie auf echter Hardware lief.

| Teil | Status | Was das Repository belegen kann |
| --- | :---: | --- |
| Software | 🟡 | Der Satz, seine Auflistung und seine Prüfung; nur auf einem Computer ausgeführt. |
| Tests | 🟡 | Die Testsuite besteht bei jedem Push in der CI. |
| Sicherheit | 🟠 | Die Sperrdatei hält SHA-256-Hashes fest, um eine Änderung oder eine veraltete Kopie zu finden; sie ist eine Konsistenzprüfung, keine Signatur. |
| Dokumentation | 🟡 | README in acht Sprachen und das Format der Sperrdatei; die Übersetzungen wurden nicht von Muttersprachlern geprüft. |

## 🎯 Überblick

Die Werkzeuge, die jedes Repository der Familie als dieselbe Kopie trägt, an einem Ort gesammelt und mit einer Version versehen:

* [`files/`](files): die kanonische Kopie der 15 gemeinsamen Dateien (die Prüfungen der Dokumentationsregeln und der README-Parität, die Bildgeneratoren, die Live-Anzeige der Build-Skripte, das Hochzählen der Manifest-Version, die Prüfung der Statusampeln und die Meldung an das Dashboard). Der Name des Repositorys steht als `<REPO>` und wird beim Ablegen einer Datei ersetzt.
* Die **Version dieses Repositorys ist die Version des Satzes**; das [Änderungsprotokoll](CHANGELOG.md) sagt, was sich in jeder Version geändert hat.
* Eine **Sperrdatei** in jedem Repository, `tools/devtools.lock.json`, geschrieben von `tools/sync_repo_tools.py` aus URTC-DOCS: die Version des Satzes und der SHA-256 jeder Kopie. `tools/check_repo_tools.py` findet eine von Hand geänderte Kopie und, wenn dieses Repository neben den anderen liegt, eine veraltete Kopie. Siehe [das Format der Sperrdatei](docs/LOCK_FORMAT.md).
* Jedes Repository bleibt mit seinem eigenen Checkout baubar und prüfbar: Die Sperrdatei ist eine Datei des Repositorys und nichts braucht das Netz.

## 🧩 Rolle in URTC

URTC-DEVTOOLS ist der Ort, an dem die gemeinsamen Werkzeuge einen Namen und eine Version bekommen. Eine Änderung an einem von ihnen war eine Änderung in etwa zehn Repositories, ohne dass etwas sagte, welche Version jedes trug; jetzt hat der Satz eine Version, jedes Repository sagt, welche es übernommen hat, und eine geänderte oder zurückgebliebene Kopie wird gemeldet. Von selbst ändert es nichts in den Repositories: URTC-DOCS legt die Dateien ab und schreibt die Sperrdateien, ein Repository nach dem anderen.

## 🏛️ Architektur

<p align="center">
  <img src="images/architecture.svg" alt="Architektur von URTC-DEVTOOLS: wer den Satz übernimmt, was er enthält und was er schreibt" width="100%">
</p>

Wie die Teile dieses Repositorys zusammenpassen: wer den Satz übernimmt, was er enthält und was er in jedem Repository schreibt. Das Bild wird aus `docs/architecture.json` gezeichnet und gegen den Code geprüft.

## 🚀 Schnellstart

**Voraussetzungen:** Python 3.10 oder neuer; sonst nichts.

```bash
python tools/devtools_set.py list            # die Version des Satzes und der SHA-256 jeder Datei
python tools/devtools_set.py check           # die Kopien dieses Repositorys sind die kanonischen Dateien
python tools/tooling_registry.py check       # das Register der Werkzeuge, die die Familien teilen: Hashes und gleiche Quellen
python -m unittest discover -s tests         # die Tests
python tools/sync_repo_tools.py --apply      # aus URTC-DOCS: den Satz und die Sperrdateien in die Nachbar-Repositories legen
```

## 🧪 Tests

Die Suite hat 28 Tests (`python -m unittest discover -s tests`). Sie prüfen, dass `files/` genau die gemeinsamen Dateien enthält, dass jede gültig ist und sich mit dem Namen eines Repositorys erzeugen lässt, dass eine geänderte oder fehlende Kopie gefunden wird, dass die Sperrdatei dieses Repositorys zu seinen Dateien und seiner Version passt, sowie Manifest, Änderungsprotokoll und Dokumente. Ein Test vergleicht `files/` mit der Vorlage von URTC-DOCS und wird übersprungen, wenn dieses Repository nicht daneben liegt. Die Logik der Sperrdatei wird in URTC-DOCS getestet.

## 🏗️ Build und Veröffentlichung

`build.sh` / `build.bat` erhöhen die Version des Satzes, prüfen die Kopien und führen die Tests aus; `build-test.sh` / `build-test.bat` prüfen, ohne eine Version zu ändern; `run.sh` / `run.bat` listen den Satz auf. Eine neue Version des Satzes entsteht, indem man eine Datei in `files/` und ihre Kopie ändert, die Version einmal für den ganzen Stapel erhöht und den Satz in die Repositories übernimmt; siehe [die Anleitung](docs/TAKING_THE_SET.md).

## 📂 Struktur des Repositorys

<p align="center">
  <img src="images/repository-structure.svg" alt="Struktur des Repositorys URTC-DEVTOOLS" width="100%">
</p>

<details>
<summary>Textversion des Baums</summary>

```text
URTC-DEVTOOLS/
├── files/                                     die 15 kanonischen Dateien, unter dem Pfad, den sie in jedem Repository haben
├── tools/                                     die Prüfung des Satzes, die Validierung des Repositorys und die Kopien, die es selbst trägt
├── tests/                                     Tests des Satzes, der Sperrdatei und des Repositorys
├── docs/                                      das Format der Sperrdatei und wie man den Satz übernimmt
├── .github/                                   CI, nächtlicher Vergleich, Vorlagen für Issues und Pull Requests
├── images/                                    Banner und Bilder dieser README
├── build.sh build.bat                         Build-Skripte
├── build-test.sh build-test.bat               Build- und Testskripte, die nichts im Repository ändern
├── test.sh test.bat                           führen die Tests aus
├── run.sh run.bat                             listen den Satz auf oder prüfen ihn
├── urtc.project.json                          Manifest: Version, Rolle, Reifegrad und Build-Befehl
├── CHANGELOG.md                               was sich in jeder Version geändert hat
├── SECURITY.md SUPPORT.md LICENSE             Sicherheitsrichtlinie, Support und Lizenz
├── CONTRIBUTING.md CODE_OF_CONDUCT.md         wie man beiträgt und der Verhaltenskodex
├── .gitattributes .gitignore                  Git-Einstellungen
├── bump_version.py bump_manifest_version.py   Skripte, die die Version erhöhen
└── pyproject.toml ruff.toml                   Projektdaten und Lint-Einstellungen
```

</details>

## 🗺️ Roadmap und bekannte Grenzen

**Bekannte Grenzen heute**

* Die Sperrdatei schreibt und prüft URTC-DOCS (`tools/sync_repo_tools.py` und `tools/check_repo_tools.py`); inzwischen trägt jedes Repository der Familie eine (`tools/devtools.lock.json`).
* URTC-DOCS hält noch seine eigene Vorlage, die der Synchronisierer liest; ein Test vergleicht beide, wenn sie nebeneinander liegen.
* Dateien, die es auch in den Schwesterprojekten gibt, werden nicht allein hierher verschoben: dieselbe Datei in allen Familien oder keine.
* Nichts davon lief auf Hardware; die Werkzeuge laufen auf einem Computer.

**Als Nächstes**

* Die Repositories der Familie nacheinander auf die Sperrdatei umstellen.
* Dieses Repository zur Quelle des Synchronisierers machen und die Vorlage von URTC-DOCS abschaffen.

## 🌍 Sprachen

README und Texte gibt es auf Englisch, Spanisch, Französisch, Italienisch, Deutsch, Chinesisch, Japanisch und europäischem Portugiesisch.

## 🔗 Verwandte Projekte

URTC besteht aus unabhängigen Repositories mit jeweils eigener Version, eigenen Tests und eigenem README. Das ist die Familie, nach Gruppen:

* **URTC Tool Platform:**
  * [URTC](https://github.com/JuanenRac/URTC) - Firmware der Werkzeugkopf-Platine (25 Werkzeugprofile, CAN-Bootloader) und die Referenz des CAN-Protokolls.
  * [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) - das CAN-Protokoll einmal als Daten geschrieben (Spezifikation, erzeugte Tabellen, Konformitätsvektoren) und der Code, den die Programme teilen.
  * [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) - Desktop-Werkzeug, das die Platinen-Firmware über CAN oder über SWD/JTAG aktualisiert.
  * [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) - Gateway vor dem CAN-Bus: lässt nur gelistete Kennungen durch, begrenzt ihre Rate und verlangt einen Sitzungsschlüssel.
  * [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) - hardwareunabhängige C-Logik und Befehlsprotokoll für eine Werkzeugablage mit Vorheizen und Lebenszyklusverfolgung.
  * [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) - Desktop-Live-Tester für den CAN-Bus, der die Bedienelemente und die Telemetrie des von einer Platine gemeldeten Werkzeugprofils zeigt.
  * [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) - Sensorrahmen-Protokoll in C und ein Python-Thermo-/RGB-Begleiter für einen Inspektions-Werkzeugkopf.
  * [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) - Browser-App, die die Platine über Web Serial und SLCAN flasht und testet, ohne Installation.
* **Ecosystem Operations:**
  * **URTC-DEVTOOLS** (dieses Repository) - die gemeinsamen Repository-Werkzeuge der Familie als versionierter Satz, mit einer Sperrdatei, die eine bearbeitete von einer veralteten Kopie unterscheidet.
  * [URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS) - Architektur, Schnittstellen, Sicherheitsbasis und erzeugter Katalog des Ökosystems sowie die Werkzeuge, die alle Repositories vergleichen.
  * [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) - Desktop-Werkzeug, das die Repositories der URTC-Familie erkennt, installiert und aktualisiert, jeweils eine ausdrückliche Aktion.

**Schwesterprojekte (unabhängig, mit derselben Basis und denselben Werkzeugen):**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - Schwesterprojekt: das Dokumentationszentrum von HYDRA-UMC, einem unabhängigen Ökosystem, das Basis und Werkzeuge mit diesem teilt
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - Schwesterprojekt: das Dokumentationszentrum von A.R.M.O.R., dem Sicherheits-Ökosystem, ebenfalls unabhängig und auf derselben Basis
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - das Profil und das Status-Dashboard aller Ökosysteme

## 📚 Dokumentation

Wo man mehr liest:

* [Das Format der Sperrdatei und was geprüft wird](docs/LOCK_FORMAT.md)
* [Den Satz übernehmen und eine neue Version machen](docs/TAKING_THE_SET.md)
* [Änderungsprotokoll dieses Repositorys](CHANGELOG.md)
* [Lizenz (GPL-3.0-or-later)](LICENSE)
* Fragen, Ideen und Meldungen: electrohobby3d@gmail.com

## 🤝 Mitwirken und Community

* Führe vor einem Pull Request `URTC_CI=1 python tools/ci_validate.py` aus: Es muss bestehen. Siehe [CONTRIBUTING.md](CONTRIBUTING.md) und den [Verhaltenskodex](CODE_OF_CONDUCT.md).
* Die README gibt es in acht Sprachen: Eine Textänderung wird in allen acht Dateien gemacht.
* Beschreibe nicht als auf einer Platine funktionierend, was nur gebaut wurde.
* Melde eine Sicherheitslücke privat: [SECURITY.md](SECURITY.md). Fragen, Ideen und Meldungen: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LIZENZ

GPL-3.0-or-later - siehe [LICENSE](LICENSE).
