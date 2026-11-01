<p align="center">
  <img src="images/URTC_DEVTOOLS_BANNER.svg" alt="URTC-DEVTOOLS banner" width="100%">
</p>

# 🧰 URTC-DEVTOOLS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 简体中文</a> | 🇯🇵 <b>日本語</b> | <a href="README_por.md">🇵🇹 Português</a></p>

### URTC ファミリー共通のリポジトリツールを、版数付きの一つのセットとして提供し、各リポジトリにロックファイルを置きます

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Python%20%2B%20JSON-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Tests-28-2ea44f.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**正直さの確認 - 現時点で実際に動くもの：** このリポジトリには、ファミリーの各リポジトリが同一のコピーとして持つ 10 個のファイル、それらを一覧し自身が持つコピーを検査する小さなツール、テスト、ドキュメントがあります。すべて動作し、CI でテストされています。ロックファイルは URTC-DOCS が書き込み検査します。現在ロックを持つのはこのリポジトリだけで、他のリポジトリはまだこのセットを取り込んでおらず、ここにあるものはどれもハードウェア上では動かしていません。

---

## 📋 ひと目で

| | |
|---|---|
| バージョン | `0.0.1` |
| 成熟度 | 足場段階 |
| テスト | 28 (`python -m unittest discover -s tests`) |
| 技術 | Python / GitHub Actions / JSON |
| 対象 | 利用者の PC |
| 実機での確認 | 対象外：ここにあるものはハードウェア上では動きません |

**移動先：** [概要](#-概要) · [アーキテクチャ](#-アーキテクチャ) · [クイックスタート](#-クイックスタート) · [テスト](#-テスト) · [構成](#-リポジトリの構成) · [関連](#-関連プロジェクト)

## 🚦 プロジェクトの状況

🟢 完了・検証済み · 🟡 動作するが既知の制限あり · 🟠 途中、または未検証 · 🔴 未実施または動作しない。実機で一度も動いていないものは緑になりません。

| 項目 | 状態 | リポジトリが示せること |
| --- | :---: | --- |
| ソフトウェア | 🟡 | セット、その一覧と検査。コンピューター上でのみ実行しています。 |
| テスト | 🟡 | テストスイートはプッシュごとに CI で通ります。 |
| セキュリティ | 🟠 | ロックは SHA-256 ハッシュを記録し、編集されたコピーや古いコピーを見つけます。整合性の検査であり、署名ではありません。 |
| ドキュメント | 🟡 | 8 言語の README とロックの形式があります。翻訳はネイティブによるレビューを受けていません。 |

## 🎯 概要

ファミリーの各リポジトリが同一のコピーとして持つツールを、一か所にまとめて版数を付けたものです：

* [`files/`](files)：10 個の共有ファイルの正規コピー（ドキュメント規則と README 整合性の検査、図の生成、ビルドスクリプトのライブパネル、マニフェスト版数の更新、状態ランプの検査、ダッシュボードへの通知）。リポジトリ名は `<REPO>` と書かれ、ファイルをリポジトリに置くときに置き換えられます。
* **このリポジトリの版数がセットの版数**です。[変更履歴](CHANGELOG.md)に各バージョンの変更点があります。
* 各リポジトリの**ロックファイル** `tools/devtools.lock.json` は URTC-DOCS の `tools/sync_repo_tools.py` が書き込みます。セットの版数と各コピーの SHA-256 です。`tools/check_repo_tools.py` は手で編集されたコピーを見つけ、このリポジトリが他のリポジトリの隣にあるときは古いままのコピーも見つけます。[ロックの形式](docs/LOCK_FORMAT.md)を参照してください。
* 各リポジトリは自分のチェックアウトだけでビルドと検査ができます。ロックはリポジトリ内のファイルで、ネットワークは不要です。

## 🧩 URTC での役割

URTC-DEVTOOLS は、共有ツールに名前と版数を与える場所です。これまでは一つ変更すると約 10 のリポジトリを変更する必要があり、各リポジトリがどの版を持つのかを示すものもありませんでした。今はセットに版数があり、各リポジトリは取り込んだ版を示し、編集されたコピーや古いコピーは報告されます。単独ではリポジトリを何も変更しません。URTC-DOCS がファイルを置きロックを書き込みます。一度に一つのリポジトリずつです。

## 🏛️ アーキテクチャ

<p align="center">
  <img src="images/architecture.svg" alt="URTC-DEVTOOLS のアーキテクチャ：誰がセットを取り込み、何を含み、何を書き込むか" width="100%">
</p>

このリポジトリの各部分がどう組み合わさるか：誰がセットを取り込み、何を含み、各リポジトリに何を書き込むか。図は `docs/architecture.json` から描かれ、コードと照合されます。

## 🚀 クイックスタート

**必要なもの：** Python 3.10 以降。ほかには何も要りません。

```bash
python tools/devtools_set.py list            # セットの版数と各ファイルの SHA-256
python tools/devtools_set.py check           # このリポジトリのコピーが正規ファイルと一致
python tools/tooling_registry.py check       # 各ファミリーが共有するツールの登録簿：ハッシュと同一ソースの確認
python -m unittest discover -s tests         # テスト
python tools/sync_repo_tools.py --apply      # URTC-DOCS から：隣のリポジトリにセットとロックを置く
```

## 🧪 テスト

テストスイートは 28 件のテストがあります（`python -m unittest discover -s tests`）。`files/` が共有ファイルだけを含むこと、各ファイルが有効でリポジトリ名で生成できること、編集または欠落したコピーが見つかること、このリポジトリのロックがファイルと版数に一致すること、そしてマニフェスト、変更履歴、ドキュメントを確認します。1 件は `files/` を URTC-DOCS のテンプレートと比較し、そのリポジトリが隣にないときはスキップされます。ロックの処理自体は URTC-DOCS でテストしています。

## 🏗️ ビルドとリリース

`build.sh` / `build.bat` はセットの版数を上げ、コピーを検査し、テストを実行します。`build-test.sh` / `build-test.bat` は版数を変えずに検査します。`run.sh` / `run.bat` はセットを一覧します。セットの新しい版は、`files/` のファイルとそのコピーを変更し、まとまり全体で版数を一度だけ上げ、リポジトリにセットを取り込むことで作ります。[ガイド](docs/TAKING_THE_SET.md)を参照してください。

## 📂 リポジトリの構成

<p align="center">
  <img src="images/repository-structure.svg" alt="URTC-DEVTOOLS のリポジトリ構成" width="100%">
</p>

<details>
<summary>ツリーのテキスト版</summary>

```text
URTC-DEVTOOLS/
├── files/                                     10 個の正規ファイル。各リポジトリでのパスと同じ場所に置かれています
├── tools/                                     セットの検査、リポジトリの検証、このリポジトリが持つコピー
├── tests/                                     セット、ロック、リポジトリの単体テスト
├── docs/                                      ロックの形式とセットの取り込み方
├── .github/                                   CI、夜間比較、Issue と PR のテンプレート
├── images/                                    バナーとこの README の図
├── build.sh build.bat                         ビルドスクリプト
├── build-test.sh build-test.bat               リポジトリを変更しないビルドとテストのスクリプト
├── test.sh test.bat                           テストを実行
├── run.sh run.bat                             セットを一覧または検査
├── urtc.project.json                          マニフェスト：版数、役割、成熟度、ビルドコマンド
├── CHANGELOG.md                               各バージョンの変更点
├── SECURITY.md SUPPORT.md LICENSE             セキュリティ方針、サポート、ライセンス
├── CONTRIBUTING.md CODE_OF_CONDUCT.md         貢献方法と行動規範
├── .gitattributes .gitignore                  Git の設定
├── bump_version.py bump_manifest_version.py   版数を上げるスクリプト
└── pyproject.toml ruff.toml                   プロジェクト情報と lint 設定
```

</details>

## 🗺️ ロードマップと既知の制限

**現時点で分かっている制限**

* ロックは URTC-DOCS（`tools/sync_repo_tools.py` と `tools/check_repo_tools.py`）が書き込み検査します。現在はファミリーのすべてのリポジトリがロック（`tools/devtools.lock.json`）を持っています。
* URTC-DOCS は今も独自のテンプレートを持ち、同期ツールはそれを読みます。両方が隣にあるときはテストで比較します。
* 姉妹プロジェクトにも存在するファイルは、ここだけで移動しません。すべてのファミリーで同じファイルにするか、何もしないかです。
* ここにあるものはどれもハードウェア上では動かしていません。ツールはコンピューター上で動きます。

**今後**

* ファミリーのリポジトリを一つずつロックに移行する。
* このリポジトリを同期ツールが読む元にし、URTC-DOCS のテンプレートを廃止する。

## 🌍 言語

README とテキストは、英語、スペイン語、フランス語、イタリア語、ドイツ語、中国語、日本語、ヨーロッパ・ポルトガル語で提供されています。

## 🔗 関連プロジェクト

URTC は独立したリポジトリで構成され、それぞれに固有のバージョン、テスト、README があります。グループ別のファミリーは次のとおりです：

* **URTC Tool Platform:**
  * [URTC](https://github.com/JuanenRac/URTC) - ツールヘッド基板のファームウェア(25 のツールプロファイル、CAN ブートローダー)と CAN プロトコルのリファレンス。
  * [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) - 一度だけデータとして書かれた CAN プロトコル(仕様、生成された表、適合ベクトル)と、各プログラムが共有するコード。
  * [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) - CAN または SWD/JTAG で基板のファームウェアを更新するデスクトップツール。
  * [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) - CAN バスの手前に置くゲートウェイ。一覧にある識別子だけを通し、レートを制限し、セッション鍵を求めます。
  * [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) - 予熱とライフサイクル追跡を備えたツールラック向けの、ハードウェア非依存の C ロジックとコマンドプロトコル。
  * [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) - 基板が報告するツールプロファイルの操作部とテレメトリを表示する、デスクトップ用のライブ CAN バステスター。
  * [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) - C のセンサーフレームプロトコルと、検査用ツールヘッド向けの Python サーマル/RGB コンパニオン。
  * [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) - Web Serial と SLCAN で基板の書き込みとテストを行うブラウザアプリ。インストール不要。
* **Ecosystem Operations:**
  * **URTC-DEVTOOLS** (このリポジトリ) - ファミリー共通のリポジトリツールを、版数付きの一つのセットとして提供します。ロックファイルで、編集されたコピーと古いままのコピーを見分けられます。
  * [URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS) - エコシステムのアーキテクチャ、インターフェース、セキュリティベースライン、生成されたカタログと、全リポジトリを比較するツール。
  * [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) - URTC ファミリーのリポジトリを検出・インストール・更新するデスクトップツール。操作は一つずつ明示的に行います。

**姉妹プロジェクト（独立しており、基盤とツールを共有）：**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - 姉妹プロジェクト：HYDRA-UMC のドキュメントハブ。基盤とツールを共有する独立したエコシステム
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - 姉妹プロジェクト：A.R.M.O.R. セキュリティエコシステムのドキュメントハブ。こちらも独立し、同じ基盤の上にある
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - すべてのエコシステムのプロフィールとステータスダッシュボード

## 📚 ドキュメント

詳しくは：

* [ロックの形式と検査内容](docs/LOCK_FORMAT.md)
* [セットの取り込みと新しい版の作り方](docs/TAKING_THE_SET.md)
* [このリポジトリの変更履歴](CHANGELOG.md)
* [ライセンス（GPL-3.0-or-later）](LICENSE)
* 質問、アイデア、報告：electrohobby3d@gmail.com

## 🤝 コントリビュートとコミュニティ

* プルリクエストの前に `URTC_CI=1 python tools/ci_validate.py` を実行してください。通る必要があります。[CONTRIBUTING.md](CONTRIBUTING.md) と[行動規範](CODE_OF_CONDUCT.md)を参照してください。
* README は 8 言語で提供されています。文章を変更するときは 8 つのファイルすべてを変更します。
* ビルドしただけのものを、基板上で動作していると書かないでください。
* 脆弱性は非公開で報告してください：[SECURITY.md](SECURITY.md)。質問、アイデア、報告：electrohobby3d@gmail.com（[SUPPORT.md](SUPPORT.md)）。

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 ライセンス

GPL-3.0-or-later - [LICENSE](LICENSE) を参照してください。
