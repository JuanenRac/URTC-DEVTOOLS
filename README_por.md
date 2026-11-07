<p align="center">
  <img src="images/URTC_DEVTOOLS_BANNER.svg" alt="URTC-DEVTOOLS banner" width="100%">
</p>

# 🧰 URTC-DEVTOOLS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 简体中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | 🇵🇹 <b>Português</b></p>

### As ferramentas de repositório partilhadas da família URTC como um conjunto com versão, com um ficheiro de bloqueio em cada repositório

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Python%20%2B%20JSON-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Tests-95-2ea44f.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Verificação de honestidade - o que funciona hoje:** este repositório contém os 15 ficheiros que os repositórios da família levam como a mesma cópia, uma pequena ferramenta que os lista e verifica as cópias que o próprio repositório leva, testes e documentação. Tudo é executado e testado na CI. O ficheiro de bloqueio é escrito e verificado pelo URTC-DOCS; até agora só este repositório leva um, os outros ainda não tomaram o conjunto, e nada disto foi executado em hardware.

---

## 📋 Num relance

| | |
|---|---|
| Versão | `0.0.4` |
| Maturidade | Estrutura inicial |
| Testes | 95 (`python -m unittest discover -s tests`) |
| Tecnologia | Python / GitHub Actions / JSON |
| Destino | O PC de quem o usa |
| Em hardware real | Não aplicável: nada aqui corre em hardware |

**Ir para:** [Visão geral](#-visão-geral) · [Arquitetura](#-arquitetura) · [Início rápido](#-início-rápido) · [Testes](#-testes) · [Estrutura](#-estrutura-do-repositório) · [Relacionados](#-projetos-relacionados)

## 🚦 Estado do projeto

🟢 feito e verificado · 🟡 funciona, com limites conhecidos · 🟠 a meio ou por verificar · 🔴 por fazer ou a não funcionar. Nada é verde se nunca correu em hardware real.

| Parte | Estado | O que o repositório consegue demonstrar |
| --- | :---: | --- |
| Software | 🟡 | O conjunto, a sua listagem e a sua verificação; executado só num computador. |
| Testes | 🟡 | A bateria de testes passa na CI em cada envio. |
| Segurança | 🟠 | O bloqueio guarda hashes SHA-256 para encontrar uma edição ou uma cópia desatualizada; é uma verificação de coerência, não uma assinatura. |
| Documentação | 🟡 | README em oito línguas e o formato do bloqueio; as traduções não foram revistas por falantes nativos. |

## 🎯 Visão geral

As ferramentas que cada repositório da família leva como a mesma cópia, reunidas num só sítio e com uma versão:

* [`files/`](files): a cópia canónica dos 15 ficheiros partilhados (as verificações da política de documentação e da paridade dos README, os geradores de imagens, o painel em direto dos scripts de compilação, a ferramenta que sobe a versão do manifesto, a verificação das luzes de estado e o aviso ao painel). O nome do repositório escreve-se `<REPO>` e é substituído quando um ficheiro é colocado num repositório.
* A **versão deste repositório é a versão do conjunto**; o [registo de alterações](CHANGELOG.md) diz o que mudou em cada versão.
* Um **ficheiro de bloqueio** em cada repositório, `tools/devtools.lock.json`, escrito por `tools/sync_repo_tools.py` do URTC-DOCS: a versão do conjunto e o SHA-256 de cada cópia. `tools/check_repo_tools.py` encontra uma cópia editada à mão e, quando este repositório está ao lado dos outros, uma cópia desatualizada. Veja [o formato do bloqueio](docs/LOCK_FORMAT.md).
* Cada repositório continua a poder ser compilado e verificado com o seu próprio checkout: o bloqueio é um ficheiro do repositório e nada precisa da rede.

## 🧩 Papel no URTC

O URTC-DEVTOOLS é onde as ferramentas partilhadas recebem um nome e uma versão. Alterar uma delas era alterar cerca de dez repositórios sem que nada dissesse que versão cada um levava; agora o conjunto tem versão, cada repositório diz qual adotou e uma cópia editada ou atrasada é assinalada. Por si só não altera nada nos repositórios: o URTC-DOCS coloca os ficheiros e escreve os bloqueios, um repositório de cada vez.

## 🏛️ Arquitetura

<p align="center">
  <img src="images/architecture.svg" alt="Arquitetura do URTC-DEVTOOLS: quem toma o conjunto, o que contém e o que escreve" width="100%">
</p>

Como se encaixam as partes deste repositório: quem toma o conjunto, o que contém e o que escreve em cada repositório. A imagem é desenhada a partir de `docs/architecture.json` e verificada contra o código.

## 🚀 Início rápido

**Requisitos:** Python 3.10 ou superior; nada mais.

```bash
python tools/devtools_set.py list            # a versão do conjunto e o SHA-256 de cada ficheiro
python tools/devtools_set.py check           # as cópias que este repositório leva são os ficheiros canónicos
python tools/tooling_registry.py check       # o registo das ferramentas que as famílias partilham: hashes e fontes iguais
python -m unittest discover -s tests         # os testes
python tools/sync_repo_tools.py --apply      # a partir do URTC-DOCS: pôr o conjunto e os bloqueios nos repositórios ao lado
```

## 🧪 Testes

A bateria tem 95 testes (`python -m unittest discover -s tests`). Verificam que `files/` contém exatamente os ficheiros partilhados, que cada um é válido e se gera com o nome de um repositório, que uma cópia editada ou em falta é encontrada, que o bloqueio deste repositório corresponde aos seus ficheiros e à sua versão, e o manifesto, o registo de alterações e os documentos. Um teste compara `files/` com o modelo do URTC-DOCS e é ignorado quando esse repositório não está ao lado. A lógica do bloqueio é testada no URTC-DOCS.

## 🏗️ Compilação e publicação

`build.sh` / `build.bat` sobem a versão do conjunto, verificam as cópias e executam os testes; `build-test.sh` / `build-test.bat` verificam sem alterar nenhuma versão; `run.sh` / `run.bat` listam o conjunto. Uma nova versão do conjunto faz-se alterando um ficheiro de `files/` e a sua cópia, subindo a versão uma só vez por lote e adotando o conjunto nos repositórios; veja [o guia](docs/TAKING_THE_SET.md).

## 📂 Estrutura do repositório

<p align="center">
  <img src="images/repository-structure.svg" alt="Estrutura do repositório URTC-DEVTOOLS" width="100%">
</p>

<details>
<summary>Versão em texto da árvore</summary>

```text
URTC-DEVTOOLS/
├── files/                                     os 15 ficheiros canónicos, no caminho que têm em cada repositório
├── tools/                                     a verificação do conjunto, a validação do repositório e as cópias que este repositório leva
├── tests/                                     testes do conjunto, do bloqueio e do repositório
├── docs/                                      o formato do bloqueio e como tomar o conjunto
├── .github/                                   CI, comparação noturna e modelos de problemas e pull requests
├── images/                                    faixa e imagens deste README
├── build.sh build.bat                         scripts de compilação
├── build-test.sh build-test.bat               scripts de compilação e testes que não alteram nada no repositório
├── test.sh test.bat                           executam os testes
├── run.sh run.bat                             listam o conjunto ou verificam-no
├── urtc.project.json                          manifesto: versão, papel, maturidade e comando de compilação
├── CHANGELOG.md                               o que mudou em cada versão
├── SECURITY.md SUPPORT.md LICENSE             política de segurança, suporte e licença
├── CONTRIBUTING.md CODE_OF_CONDUCT.md         como contribuir e código de conduta
├── .gitattributes .gitignore                  definições do Git
├── bump_version.py bump_manifest_version.py   scripts que sobem a versão
└── pyproject.toml ruff.toml                   dados do projeto e definições de lint
```

</details>

## 🗺️ Roteiro e limites conhecidos

**Limites conhecidos hoje**

* O bloqueio é escrito e verificado pelo URTC-DOCS (`tools/sync_repo_tools.py` e `tools/check_repo_tools.py`); todos os repositórios da família levam agora um (`tools/devtools.lock.json`).
* O URTC-DOCS ainda guarda o seu próprio modelo, que é o que o sincronizador lê; um teste compara os dois quando estão lado a lado.
* Os ficheiros que existem também nos projetos irmãos não se movem para aqui sozinhos: o mesmo ficheiro em todas as famílias, ou nenhum.
* Nada disto foi executado em hardware; as ferramentas funcionam num computador.

**A seguir**

* Passar os repositórios da família para o bloqueio um de cada vez.
* Fazer deste repositório a fonte que o sincronizador lê e retirar o modelo do URTC-DOCS.

## 🌍 Idiomas

O README e os textos existem em inglês, espanhol, francês, italiano, alemão, chinês, japonês e português europeu.

## 🔗 Projetos relacionados

O URTC é feito de repositórios independentes, cada um com a sua versão, os seus testes e o seu README. Esta é a família, por grupos:

* **URTC Tool Platform:**
  * [URTC](https://github.com/JuanenRac/URTC) - firmware da placa da cabeça de ferramenta (25 perfis de ferramenta, bootloader CAN) e a referência do protocolo CAN.
  * [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) - o protocolo CAN escrito uma só vez como dados (especificação, tabelas geradas, vetores de conformidade) e o código que os programas partilham.
  * [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) - ferramenta de ambiente de trabalho que atualiza o firmware da placa por CAN ou por SWD/JTAG.
  * [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) - gateway à frente do barramento CAN: só deixa passar os identificadores de uma lista, limita a sua taxa e pede uma chave de sessão.
  * [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) - lógica em C independente do hardware e protocolo de comandos para um suporte de ferramentas com pré-aquecimento e acompanhamento do ciclo de vida.
  * [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) - testador de ambiente de trabalho do barramento CAN em direto que mostra os controlos e a telemetria do perfil de ferramenta que uma placa reporta.
  * [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) - protocolo de tramas de sensor em C e um companheiro em Python térmico/RGB para uma cabeça de ferramenta de inspeção.
  * [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) - aplicação de navegador que grava e testa a placa por Web Serial e SLCAN, sem instalar nada.
* **Ecosystem Operations:**
  * **URTC-DEVTOOLS** (este repositório) - as ferramentas de repositório partilhadas da família como um conjunto com versão e um ficheiro de bloqueio que distingue uma cópia editada de uma desatualizada.
  * [URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS) - arquitetura, interfaces, base de segurança e catálogo gerado do ecossistema, mais as ferramentas que comparam todos os repositórios.
  * [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) - ferramenta de ambiente de trabalho que deteta, instala e atualiza os repositórios da família URTC, uma ação explícita de cada vez.

**Projetos irmãos (independentes, com a mesma base e as mesmas ferramentas):**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - projeto irmão: o centro de documentação do HYDRA-UMC, um ecossistema independente que partilha a base e as ferramentas com este
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - projeto irmão: o centro de documentação do A.R.M.O.R., o ecossistema de segurança, também independente e sobre a mesma base
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - o perfil e o painel de estado de todos os ecossistemas

## 📚 Documentação

Onde ler mais:

* [O formato do bloqueio e o que é verificado](docs/LOCK_FORMAT.md)
* [Tomar o conjunto e fazer uma nova versão](docs/TAKING_THE_SET.md)
* [Registo de alterações deste repositório](CHANGELOG.md)
* [Licença (GPL-3.0-or-later)](LICENSE)
* Perguntas, ideias e relatórios: electrohobby3d@gmail.com

## 🤝 Contribuir e comunidade

* Antes de um pull request execute `URTC_CI=1 python tools/ci_validate.py`: tem de passar. Veja [CONTRIBUTING.md](CONTRIBUTING.md) e o [código de conduta](CODE_OF_CONDUCT.md).
* O README existe em oito línguas: uma alteração ao texto faz-se nos oito ficheiros.
* Não descreva como a funcionar numa placa o que apenas foi compilado.
* Comunique uma vulnerabilidade em privado: [SECURITY.md](SECURITY.md). Perguntas, ideias e relatórios: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENÇA

GPL-3.0-or-later - veja [LICENSE](LICENSE).
