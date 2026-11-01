<p align="center">
  <img src="images/URTC_DEVTOOLS_BANNER.svg" alt="URTC-DEVTOOLS banner" width="100%">
</p>

# 🧰 URTC-DEVTOOLS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | 🇨🇳 <b>简体中文</b> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### URTC 家族共用的仓库工具，作为带版本的整套工具，并在每个仓库中放一份锁文件

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Python%20%2B%20JSON-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Tests-28-2ea44f.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**诚实声明 - 今天真正能运行的内容：** 本仓库包含家族各仓库作为同一份副本携带的14 个文件、一个列出它们并检查本仓库自带副本的小工具，以及测试和文档。这些全部可以运行，并在 CI 中测试。锁文件由 URTC-DOCS 写入和检查；目前只有本仓库带有锁，其他仓库还没有采用这套工具，这里的任何内容也都没有在硬件上运行过。

---

## 📋 速览

| | |
|---|---|
| 版本 | `0.0.1` |
| 成熟度 | 雏形 |
| 测试 | 28 (`python -m unittest discover -s tests`) |
| 技术栈 | Python / GitHub Actions / JSON |
| 目标 | 使用者的电脑 |
| 真实硬件 | 不适用：这里的内容不在硬件上运行 |

**跳转到：** [概述](#-概述) · [架构](#-架构) · [快速开始](#-快速开始) · [测试](#-测试) · [结构](#-仓库结构) · [相关项目](#-相关项目)

## 🚦 项目状态

🟢 已完成并已验证 · 🟡 可用，但有已知限制 · 🟠 做了一半或未验证 · 🔴 未完成或不能用。从未在真实硬件上运行过的内容不会是绿色。

| 部分 | 状态 | 仓库能够证明的内容 |
| --- | :---: | --- |
| 软件 | 🟡 | 整套工具、它的列表和检查；只在电脑上运行过。 |
| 测试 | 🟡 | 每次推送时测试套件都会在 CI 中通过。 |
| 安全 | 🟠 | 锁文件记录 SHA-256 哈希，用来发现被改动的副本或已过时的副本；它是一致性检查，不是签名。 |
| 文档 | 🟡 | 提供八种语言的 README 和锁文件格式；翻译未经母语者审阅。 |

## 🎯 概述

家族中每个仓库都作为同一份副本携带的工具，集中在一处并带有版本：

* [`files/`](files)：14 个共用文件的规范副本（文档规则检查和 README 一致性检查、图片生成器、构建脚本的实时面板、清单版本提升工具、状态灯检查和给仪表板的通知）。仓库名写作 `<REPO>`，文件放入仓库时会被替换。
* **本仓库的版本就是整套工具的版本**；[变更日志](CHANGELOG.md)说明每个版本改了什么。
* 每个仓库中的**锁文件** `tools/devtools.lock.json`，由 URTC-DOCS 的 `tools/sync_repo_tools.py` 写入：整套工具的版本和每个副本的 SHA-256。`tools/check_repo_tools.py` 能发现被手工改动的副本，并且在本仓库与其他仓库并排放置时，发现已过时的副本。参见[锁文件格式](docs/LOCK_FORMAT.md)。
* 每个仓库仍可凭自己的检出内容构建和检查：锁是仓库里的一个文件，任何操作都不需要网络。

## 🧩 在 URTC 中的角色

URTC-DEVTOOLS 是共用工具获得名称和版本的地方。以前改动其中一个工具，就要改动大约十个仓库，而没有任何东西说明各仓库带的是哪个版本；现在整套工具有了版本，每个仓库说明自己采用的是哪一版，被改动或落后的副本会被报告。它本身不会改动任何仓库：由 URTC-DOCS 放入文件并写入锁，一次一个仓库。

## 🏛️ 架构

<p align="center">
  <img src="images/architecture.svg" alt="URTC-DEVTOOLS 架构：谁采用这套工具、它包含什么、它写入什么" width="100%">
</p>

本仓库各部分如何配合：谁采用这套工具、它包含什么、它在每个仓库中写入什么。图由 `docs/architecture.json` 绘制，并与代码核对。

## 🚀 快速开始

**要求：** Python 3.10 或更新版本；无需其他东西。

```bash
python tools/devtools_set.py list            # 整套工具的版本和每个文件的 SHA-256
python tools/devtools_set.py check           # 本仓库自带的副本就是规范文件
python tools/tooling_registry.py check       # 各系列共用工具的登记表：校验哈希与相同来源
python -m unittest discover -s tests         # 测试
python tools/sync_repo_tools.py --apply      # 在 URTC-DOCS 中：把整套工具和锁放入相邻的仓库
```

## 🧪 测试

测试套件共有 28 个测试（`python -m unittest discover -s tests`）。它们检查 `files/` 恰好包含共用文件，每个文件都有效并能用仓库名生成，被改动或缺失的副本能被发现，本仓库的锁与其文件和版本一致，以及清单、变更日志和文档。一个测试把 `files/` 与 URTC-DOCS 的模板比较，该仓库不在旁边时会跳过。锁的逻辑在 URTC-DOCS 中测试。

## 🏗️ 构建与发布

`build.sh` / `build.bat` 提升整套工具的版本、检查副本并运行测试；`build-test.sh` / `build-test.bat` 在不改变任何版本的情况下检查；`run.sh` / `run.bat` 列出整套工具。新版本的做法是：改动 `files/` 中的文件及其副本，整批只提升一次版本，然后把这套工具带入各仓库；参见[指南](docs/TAKING_THE_SET.md)。

## 📂 仓库结构

<p align="center">
  <img src="images/repository-structure.svg" alt="URTC-DEVTOOLS 的仓库结构" width="100%">
</p>

<details>
<summary>目录树的文本版本</summary>

```text
URTC-DEVTOOLS/
├── files/                                     14 个规范文件，路径与它们在每个仓库中的相同
├── tools/                                     整套工具的检查、仓库校验以及本仓库自带的副本
├── tests/                                     整套工具、锁文件和仓库的单元测试
├── docs/                                      锁文件的格式以及如何采用整套工具
├── .github/                                   CI、夜间比较、议题和拉取请求模板
├── images/                                    横幅和本 README 的图片
├── build.sh build.bat                         构建脚本
├── build-test.sh build-test.bat               不改动仓库的构建与测试脚本
├── test.sh test.bat                           运行测试
├── run.sh run.bat                             列出整套工具或检查它
├── urtc.project.json                          清单：版本、角色、成熟度和构建命令
├── CHANGELOG.md                               每个版本的变更
├── SECURITY.md SUPPORT.md LICENSE             安全策略、支持与许可证
├── CONTRIBUTING.md CODE_OF_CONDUCT.md         如何贡献及行为准则
├── .gitattributes .gitignore                  Git 设置
├── bump_version.py bump_manifest_version.py   提升版本的脚本
└── pyproject.toml ruff.toml                   项目信息和 lint 设置
```

</details>

## 🗺️ 路线图与已知限制

**目前已知的限制**

* 锁由 URTC-DOCS（`tools/sync_repo_tools.py` 和 `tools/check_repo_tools.py`）写入和检查；现在家族中的每个仓库都带有锁（`tools/devtools.lock.json`）。
* URTC-DOCS 仍保留自己的模板，同步工具读取的就是它；两者并排放置时由一个测试比较。
* 姊妹项目中同样存在的文件不会单独搬到这里：要么所有家族一起搬，要么都不搬。
* 这里的任何内容都没有在硬件上运行过；这些工具在电脑上运行。

**下一步**

* 让家族的仓库逐个改用锁。
* 让本仓库成为同步工具读取的来源，并停用 URTC-DOCS 的模板。

## 🌍 语言

README 和文本提供英语、西班牙语、法语、意大利语、德语、中文、日语和欧洲葡萄牙语版本。

## 🔗 相关项目

URTC 由相互独立的仓库组成，每个仓库都有自己的版本、测试和 README。以下是按组划分的家族：

* **URTC Tool Platform:**
  * [URTC](https://github.com/JuanenRac/URTC) - 工具头电路板的固件(25 个工具配置、CAN 引导程序)以及 CAN 协议参考。
  * [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) - 只写一次的 CAN 协议数据(规范、生成的表格、一致性向量)以及各程序共享的代码。
  * [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) - 通过 CAN 或 SWD/JTAG 更新电路板固件的桌面工具。
  * [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) - 位于 CAN 总线前的网关:只放行列表中的标识符,限制其速率,并要求会话密钥。
  * [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) - 用于带预热和生命周期跟踪的工具架的、与硬件无关的 C 逻辑和命令协议。
  * [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) - 桌面实时 CAN 总线测试器,显示电路板所报告工具配置的控件和遥测。
  * [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) - C 语言的传感器帧协议,以及用于检测工具头的 Python 热成像/RGB 配套程序。
  * [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) - 通过 Web Serial 和 SLCAN 烧录并测试电路板的浏览器应用,无需安装。
* **Ecosystem Operations:**
  * **URTC-DEVTOOLS** (本仓库) - 家族共用的仓库工具，作为带版本的整套工具，并用锁文件区分被改动的副本和已过时的副本。
  * [URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS) - 生态系统的架构、接口、安全基线和生成的目录,以及比较所有仓库的工具。
  * [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) - 检测、安装并更新 URTC 家族仓库的桌面工具,每次只执行一个明确的操作。

**姊妹项目（相互独立，共用同一基础和工具）：**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - 姊妹项目：HYDRA-UMC 的文档中心，一个独立的生态，与本生态共用基础和工具
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - 姊妹项目：A.R.M.O.R. 安全生态的文档中心，同样独立，建立在同一基础上
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - 所有生态的个人主页和状态面板

## 📚 文档

更多内容：

* [锁文件格式及检查内容](docs/LOCK_FORMAT.md)
* [采用整套工具并制作新版本](docs/TAKING_THE_SET.md)
* [本仓库的变更日志](CHANGELOG.md)
* [许可证（GPL-3.0-or-later）](LICENSE)
* 问题、想法和报告：electrohobby3d@gmail.com

## 🤝 参与贡献与社区

* 提交拉取请求之前运行 `URTC_CI=1 python tools/ci_validate.py`：必须通过。参见 [CONTRIBUTING.md](CONTRIBUTING.md) 和[行为准则](CODE_OF_CONDUCT.md)。
* README 提供八种语言：修改文本时要同时修改八个文件。
* 不要把仅仅构建过的内容描述成已在板子上运行。
* 请私下报告漏洞：[SECURITY.md](SECURITY.md)。问题、想法和报告：electrohobby3d@gmail.com（[SUPPORT.md](SUPPORT.md)）。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 许可证

GPL-3.0-or-later - 参见 [LICENSE](LICENSE)。
