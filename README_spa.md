<p align="center">
  <img src="images/URTC_DEVTOOLS_BANNER.svg" alt="URTC-DEVTOOLS banner" width="100%">
</p>

# 🧰 URTC-DEVTOOLS

<p align="center"><a href="README.md">🇺🇸 English</a> | 🇪🇸 <b>Español</b> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 简体中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Las herramientas de repositorio compartidas de la familia URTC como un conjunto con versión, con un archivo de bloqueo en cada repositorio

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Python%20%2B%20JSON-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Tests-95-2ea44f.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Comprobación de honestidad - lo que funciona hoy:** este repositorio contiene los 18 archivos que los repositorios de la familia llevan como la misma copia, una pequeña herramienta que los lista y comprueba las copias que lleva el propio repositorio, pruebas y documentación. Todo se ejecuta y se prueba en la CI. El archivo de bloqueo lo escribe y lo comprueba URTC-DOCS; todos los repositorios de la familia llevan uno, y nada de esto se ha ejecutado en hardware.

---

## 📋 De un vistazo

| | |
|---|---|
| Versión | `0.0.5` |
| Madurez | Andamiaje |
| Tests | 95 (`python -m unittest discover -s tests`) |
| Tecnología | Python / GitHub Actions / JSON |
| Destino | El PC de quien lo usa |
| En hardware real | No aplica: nada de esto se ejecuta en hardware |

**Ir a:** [Resumen](#-resumen) · [Arquitectura](#-arquitectura) · [Inicio rápido](#-inicio-rápido) · [Pruebas](#-pruebas) · [Estructura](#-estructura-del-repositorio) · [Relacionados](#-proyectos-relacionados)

## 🚦 Estado del proyecto

🟢 hecho y verificado · 🟡 funciona, con límites conocidos · 🟠 a medias o sin verificar · 🔴 sin hacer o sin funcionar. Nada es verde si nunca corrió en hardware real.

| Parte | Estado | Lo que el repositorio puede demostrar |
| --- | :---: | --- |
| Software | 🟡 | El conjunto, su listado y su comprobación; ejecutado solo en un ordenador. |
| Pruebas | 🟡 | La batería de pruebas pasa en la CI en cada subida. |
| Seguridad | 🟠 | El bloqueo guarda hashes SHA-256 para detectar una edición o una copia desfasada; es una comprobación de coherencia, no una firma. |
| Documentación | 🟡 | README en ocho idiomas y el formato del bloqueo; las traducciones no las ha revisado ningún hablante nativo. |

## 🎯 Resumen

Las herramientas que cada repositorio de la familia lleva como la misma copia, reunidas en un solo sitio y con una versión:

* [`files/`](files): la copia canónica de los 18 archivos compartidos (las comprobaciones de política de documentación y de paridad de README, los generadores de dibujos, el panel en vivo de los scripts de compilación, el que sube la versión del manifiesto, la comprobación de las luces de estado y el aviso al panel). El nombre del repositorio se escribe `<REPO>` y se sustituye al poner un archivo en un repositorio.
* La **versión de este repositorio es la versión del conjunto**; el [registro de cambios](CHANGELOG.md) dice qué cambió en cada versión.
* Un **archivo de bloqueo** en cada repositorio, `tools/devtools.lock.json`, escrito por `tools/sync_repo_tools.py` de URTC-DOCS: la versión del conjunto y el SHA-256 de cada copia. `tools/check_repo_tools.py` encuentra una copia editada a mano y, cuando este repositorio está junto a los demás, una copia desfasada. Véase [el formato del bloqueo](docs/LOCK_FORMAT.md).
* Cada repositorio sigue pudiéndose compilar y comprobar con su propia copia de trabajo: el bloqueo es un archivo del repositorio y nada necesita la red.

## 🧩 Papel en URTC

URTC-DEVTOOLS es donde las herramientas compartidas reciben un nombre y una versión. Un cambio en una de ellas era un cambio en unos diez repositorios sin que nada dijera qué versión llevaba cada uno; ahora el conjunto tiene versión, cada repositorio dice cuál adoptó y se avisa de una copia editada o atrasada. Por sí mismo no cambia nada en los repositorios: URTC-DOCS pone los archivos y escribe los bloqueos, un repositorio cada vez.

## 🏛️ Arquitectura

<p align="center">
  <img src="images/architecture.svg" alt="Arquitectura de URTC-DEVTOOLS: quién toma el conjunto, qué contiene y qué escribe" width="100%">
</p>

Cómo encajan las partes de este repositorio: quién toma el conjunto, qué contiene y qué escribe en cada repositorio. El dibujo se genera desde `docs/architecture.json` y se contrasta con el código.

## 🚀 Inicio rápido

**Requisitos:** Python 3.10 o superior; nada más.

```bash
python tools/devtools_set.py list            # la versión del conjunto y el SHA-256 de cada archivo
python tools/devtools_set.py check           # las copias que lleva este repositorio son los archivos canónicos
python tools/tooling_registry.py check       # el registro de las herramientas que comparten las familias: hashes y fuentes iguales
python -m unittest discover -s tests         # las pruebas
python tools/sync_repo_tools.py --apply      # desde URTC-DOCS: poner el conjunto y los bloqueos en los repositorios de al lado
```

## 🧪 Pruebas

La batería tiene 95 pruebas (`python -m unittest discover -s tests`). Comprueban que `files/` contiene exactamente los archivos compartidos, que cada uno es válido y se genera con el nombre de un repositorio, que se detecta una copia editada o ausente, que el bloqueo de este repositorio coincide con sus archivos y su versión, y el manifiesto, el registro de cambios y los documentos. Una prueba compara `files/` con la plantilla de URTC-DOCS y se omite cuando ese repositorio no está al lado. La lógica del bloqueo se prueba en URTC-DOCS.

## 🏗️ Compilación y publicación

`build.sh` / `build.bat` suben la versión del conjunto, comprueban las copias y ejecutan las pruebas; `build-test.sh` / `build-test.bat` comprueban sin cambiar ninguna versión; `run.sh` / `run.bat` listan el conjunto. Una versión nueva del conjunto se hace cambiando un archivo de `files/` y su copia, subiendo la versión una sola vez por lote y adoptando el conjunto en los repositorios; véase [la guía](docs/TAKING_THE_SET.md).

## 📂 Estructura del repositorio

<p align="center">
  <img src="images/repository-structure.svg" alt="Estructura del repositorio URTC-DEVTOOLS" width="100%">
</p>

<details>
<summary>Versión en texto del árbol</summary>

```text
URTC-DEVTOOLS/
├── files/                                     los 18 archivos canónicos, en la ruta que tienen en cada repositorio
├── tools/                                     la comprobación del conjunto, la validación del repositorio y las copias que lleva este repositorio
├── tests/                                     pruebas del conjunto, del candado y del repositorio
├── docs/                                      el formato del candado y cómo tomar el conjunto
├── .github/                                   CI, comparación nocturna y plantillas de incidencias y pull requests
├── images/                                    banner y dibujos de este README
├── build.sh build.bat                         scripts de compilación
├── build-test.sh build-test.bat               scripts de compilación y pruebas que no cambian nada del repositorio
├── test.sh test.bat                           ejecutan las pruebas
├── run.sh run.bat                             listan el conjunto o lo comprueban
├── urtc.project.json                          manifiesto: versión, papel, madurez y orden de compilación
├── CHANGELOG.md                               qué cambió en cada versión
├── SECURITY.md SUPPORT.md LICENSE             política de seguridad, soporte y licencia
├── CONTRIBUTING.md CODE_OF_CONDUCT.md         cómo contribuir y código de conducta
├── .gitattributes .gitignore                  ajustes de Git
├── bump_version.py bump_manifest_version.py   scripts que suben la versión
└── pyproject.toml ruff.toml                   datos del proyecto y ajustes de lint
```

</details>

## 🗺️ Hoja de ruta y límites conocidos

**Límites conocidos hoy**

* El bloqueo lo escribe y lo comprueba URTC-DOCS (`tools/sync_repo_tools.py` y `tools/check_repo_tools.py`); todos los repositorios de la familia llevan uno ya (`tools/devtools.lock.json`).
* URTC-DOCS conserva su propia plantilla, que es la que lee el sincronizador; una prueba compara ambas cuando están juntas.
* Los archivos que existen en los proyectos hermanos no se mueven aquí por separado: el mismo archivo en todas las familias, o ninguno.
* Nada de esto se ha ejecutado en hardware; las herramientas funcionan en un ordenador.

**Próximamente**

* Hacer de este repositorio la fuente que lee el sincronizador y retirar la plantilla de URTC-DOCS.

## 🌍 Idiomas

README y textos existen en inglés, español, francés, italiano, alemán, chino, japonés y portugués de Portugal.

## 🔗 Proyectos relacionados

URTC se compone de repositorios independientes, cada uno con su versión, sus pruebas y su README. Esta es la familia, por grupos:

* **URTC Tool Platform:**
  * [URTC](https://github.com/JuanenRac/URTC) - firmware de la placa del cabezal de herramienta (25 perfiles de herramienta, bootloader CAN) y la referencia del protocolo CAN.
  * [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) - el protocolo CAN escrito una sola vez como datos (especificación, tablas generadas, vectores de conformidad) y el código que comparten los programas.
  * [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) - herramienta de escritorio que actualiza el firmware de la placa por CAN o por SWD/JTAG.
  * [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) - pasarela delante del bus CAN: solo deja pasar los identificadores de una lista, limita su frecuencia y pide una clave de sesión.
  * [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) - lógica en C independiente del hardware y protocolo de órdenes para un soporte de herramientas con precalentamiento y seguimiento del ciclo de vida.
  * [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) - probador de escritorio del bus CAN en vivo que muestra los controles y la telemetría del perfil de herramienta que informa una placa.
  * [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) - protocolo de tramas de sensor en C y un acompañante en Python térmico/RGB para un cabezal de inspección.
  * [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) - aplicación de navegador que graba y prueba la placa por Web Serial y SLCAN, sin instalar nada.
* **Ecosystem Operations:**
  * **URTC-DEVTOOLS** (este repositorio) - las herramientas de repositorio compartidas de la familia como un conjunto con versión y un fichero de bloqueo que distingue una copia editada de una desfasada.
  * [URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS) - arquitectura, interfaces, línea base de seguridad y catálogo generado del ecosistema, más las herramientas que comparan todos los repositorios.
  * [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) - herramienta de escritorio que detecta, instala y actualiza los repositorios de la familia URTC, una acción explícita cada vez.

**Proyectos hermanos (independientes, con la misma base y herramientas):**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - proyecto hermano: el centro de documentación de HYDRA-UMC, un ecosistema independiente que comparte base y herramientas con este
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - proyecto hermano: el centro de documentación de A.R.M.O.R., el ecosistema de seguridad, también independiente y sobre la misma base
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - el perfil y el panel de estado de todos los ecosistemas

## 📚 Documentación

Dónde leer más:

* [El formato del bloqueo y lo que se comprueba](docs/LOCK_FORMAT.md)
* [Tomar el conjunto y hacer una versión nueva](docs/TAKING_THE_SET.md)
* [Registro de cambios de este repositorio](CHANGELOG.md)
* [Licencia (GPL-3.0-or-later)](LICENSE)
* Preguntas, ideas e informes: electrohobby3d@gmail.com

## 🤝 Contribuir y comunidad

* Antes de una pull request ejecuta `URTC_CI=1 python tools/ci_validate.py`: debe pasar. Véanse [CONTRIBUTING.md](CONTRIBUTING.md) y el [código de conducta](CODE_OF_CONDUCT.md).
* El README existe en ocho idiomas: un cambio en el texto se hace en los ocho archivos.
* No describas como funcionando en una placa lo que solo se ha compilado.
* Informa de una vulnerabilidad en privado: [SECURITY.md](SECURITY.md). Preguntas, ideas e informes: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

GPL-3.0-or-later - véase [LICENSE](LICENSE).
