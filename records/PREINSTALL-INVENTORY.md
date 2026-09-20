# Factory OS導入前のMCP・スキル・ルール・プラグイン一覧

## 調査範囲と読み方

基準資料：[20260920-092704-before-factory-os](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os) の初期化前snapshot。
用途は実ファイルの説明・設定から確認した役割。個々のスキルの実行履歴や使用回数は調べていないため、配置をもって「実際に使用済み」とは扱わない。プロジェクト固有のMCP・AGENTSはこのグローバルバックアップの対象外。
Sitesは最初のsnapshotに存在せず、後の削除直前調査で確認されたため別枠。

- グローバル直登録MCP：2件。プラグイン内MCP定義：4件。
- 単独配置のカスタムスキル：22種類／29配置。組み込みスキル：6種類。
- プラグイン：設定で有効16登録、キャッシュのmanifest確認20登録（GitHubの新旧を別登録として計上）。
- ユーザールール：AGENTS.md 1件、コマンド許可ルール1件。

## MCP

| 名前 | 登録元 | 用途・注意点 |
|---|---|---|
| node_repl | グローバルconfig.toml | JavaScriptを継続実行するローカル実行環境。Codexの操作ランタイム配下。 |
| serena | グローバルconfig.toml | ソースコードの構造・シンボル検索等。起動対象はE:/aiwork/JCKに固定。別プロジェクトへそのまま戻すと対象違いになる。 |
| fusion | mechanical-cad | ローカルFusion連携。http://127.0.0.1:27182/mcp。 |
| github | 旧GitHubプラグイン | GitHub操作。https://api.githubcopilot.com/mcp/。接続成功はこの調査では未確認。 |
| cua_repl | unified-computer-use | ブラウザー操作用Nodeランタイム。 |
| codex_app | codex-app-tools | Codexアプリ内のタスク・プロジェクト等の操作。 |

## 単独配置のカスタムスキル

| スキル | 用途 | 配置・補足 |
|---|---|---|
| agentcad | Stella_Agentcad MCPを使うCAD制作。ほかのCAD方式との混用を制限。 | agents。 |
| ai-cad | CadQueryを使う機械設計、製造・組立チェック、複数方向のレンダリング。 | agents。 |
| architecture-hdvs | UI・Tauri・DSPの機能別設計ルール、f64精度保護、ファイル分割・検証済み資産の保護。 | codex / agents。2か所に重複。agents側のみ無効化設定あり。codex側には配置あり。 |
| bambu-labs | Bambu Labプリンターへの転送・印刷開始。 | agents。 |
| cad | Text-to-CAD／cadgenによるパラメトリックCAD作成・修正・測定・出力。 | agents。 |
| cad-viewer | STEP・STL・3MFなどの3D形状をブラウザーで確認。 | agents。 |
| dfam-check | 3Dプリントの肉厚・張り出し・支持・造形方向を評価。 | agents。 |
| dxf | レーザー加工等に使う2D DXF図面の作成・検証。 | agents。 |
| forgecad | ForgeCADのJavaScriptモデル作成・編集・実行。 | codex / agents。2か所に重複。 |
| forgecad-build-model | ForgeCADで設計から評価・修正まで進める製品制作手順。 | codex / agents。2か所に重複。 |
| forgecad-image-prompt | 実際のCAD構造と矛盾しない画像生成プロンプト作成。 | codex / agents。2か所に重複。 |
| forgecad-project-sync | ForgeCADのクラウド同期・共有・公開管理。 | codex / agents。2か所に重複。 |
| forgecad-reconstruct-cad-file | 既存STEP・STL等から編集可能なForgeCADモデルを再構築。 | codex / agents。2か所に重複。 |
| forgecad-reconstruct-from-images | 写真・画像を根拠にForgeCADモデルを再構築。 | codex / agents。2か所に重複。 |
| gcode | スライサーを使うG-code生成と静的検証。 | agents。 |
| mesh-to-precision-solid | STLや多数の三角面を持つ形状を測定し、ソリッドへ修復・軽量化。 | codex。 |
| openscad-design | OpenSCAD MCPによるパラメトリック部品設計・出力。 | agents。 |
| sdf | Gazebo等のシミュレーター用ロボット・環境・センサー定義。 | agents。 |
| sendcutsend | SendCutSend外注加工向けの図面・材料・加工条件チェック。 | agents。 |
| srdf | MoveIt2の動作計画グループ・姿勢・衝突除外を定義。 | agents。 |
| step-parts | 購入部品のSTEPモデルをstep.partsで検索・取得。 | agents。 |
| urdf | ロボットのリンク・関節・慣性・衝突形状を定義。 | agents。 |

`company-director`、`codex-primary-runtime`はフォルダーだけが残り、バックアップ内は空。使用可能なスキルとして数えていない。

## 組み込みスキル

| 名前 | 用途 |
|---|---|
| imagegen | 画像生成・編集 |
| openai-docs | OpenAI製品の公式情報確認 |
| plugin-creator | プラグイン作成 |
| review-agent | コードの欠陥レビュー |
| skill-creator | スキル作成・更新 |
| skill-installer | スキル導入 |

## ルール

| ルール | 内容・目的 |
|---|---|
| 日本語・説明方針 | 日本語で回答。コード文法の説明より、役割・適用手順を明確にする。 |
| 設計判断 | メリット・デメリットの比較、結論を先に説明。architecture-hdvsを毎回参照。 |
| CAD自動振分け | 物理設計でmechanical-cad-orchestratorを使用。正本を1つにし、寸法・干渉・動作・造形性を検証。未検証を完成扱いしない。 |
| default.rules | Windows PowerShellから実行する `npm.cmd run build` の指定コマンドをallow。一般的な全コマンド許可ではない。 |

## プラグイン

「有効設定」は導入前config.tomlにenabled=trueがあったもの。「キャッシュ確認」は実体を確認したが、その設定だけでは有効性・使用実績を断定できないもの。

| 登録ID | 用途 | 導入前の証拠 | 同梱SKILL.md数 |
|---|---|---|---|
| browser@openai-bundled | Codex内蔵ブラウザーでWeb画面やローカルUIを確認・操作。 | 有効設定あり | 0 |
| cad@text-to-cad | CAD・ロボット・加工用スキル一式。 | 有効設定あり | 12 |
| chrome@openai-bundled | 既存Chromeタブやログイン済みブラウザーの操作支援。 | 有効設定あり | 0 |
| codex-app-tools@openai-bundled | Codexのタスク・プロジェクト・サイドバー・自動実行等の操作。 | 有効設定あり | 0 |
| computer-use@openai-bundled | Windowsデスクトップアプリの画面操作。 | 有効設定あり | 1 |
| data-analytics@openai-curated-remote | データ品質、KPI、分析、レポート・ダッシュボード。 | キャッシュ確認 | 20 |
| documents@openai-primary-runtime | Word／Google Docs向け文書作成・編集。 | 有効設定あり | 1 |
| github@openai-curated | リポジトリ・PR・Issue・CIの調査と操作。 | 有効設定あり | 4 |
| github@openai-curated-remote | リポジトリ・PR・Issue・CIの調査と操作。 | キャッシュ確認 | 0 |
| hugging-face@openai-curated | モデル・データセット・Spaces・学習・評価・論文の操作。 | 有効設定あり | 11 |
| mechanical-cad@personal | CAD方式選択、単一の設計正本、Fusionとの相互検証を統括。 | 有効設定あり | 1 |
| nvidia@openai-curated | GPU・CUDA・AI推論・Omniverse・物理シミュレーション支援。 | 有効設定あり | 11 |
| openai-templates@openai-curated-remote | 文書・スライド・表の標準テンプレート集。 | キャッシュ確認 | 20 |
| pdf@openai-primary-runtime | PDFの読取・生成・レイアウト確認。 | 有効設定あり | 1 |
| plugin-management@openai-curated-remote | プラグイン検索・権限確認・連携管理。 | キャッシュ確認 | 1 |
| presentations@openai-primary-runtime | PowerPoint／Google Slides向け資料作成・検証。 | 有効設定あり | 1 |
| spreadsheets@openai-primary-runtime | Excel・CSV等の作成・分析、Excelのライブ操作。 | 有効設定あり | 2 |
| template-creator@openai-primary-runtime | 文書・表・スライド等を再利用可能なテンプレートにする。 | 有効設定あり | 1 |
| unified-computer-use@openai-bundled | ブラウザー操作を実行する共通ランタイム。 | 有効設定あり | 0 |
| visualize@openai-bundled | チャート・地図・図解・シミュレーション等の対話表示。 | 有効設定あり | 1 |

### 後の調査で確認されたもの

Sites：Webサイトの作成・公開・プレビュー診断。最初のsnapshotにはなく、追加バックアップに保存。初回導入直前に存在したとは断定しない。

## 見直しで分かった点

1. CAD系が中心で、複数のCAD方式と同用途のスキルが並存。併用可能だが、設計ごとに正本と方式を決める必要がある。
2. ForgeCAD 6種類とarchitecture-hdvsは二重配置。CADプラグインと単独スキルにも同名がある。
3. SerenaはJCK専用設定。全プロジェクト共通のMCPとして復元する前に接続先を見直す必要がある。
4. 旧会社システムcompany-directorは空フォルダーのみ。新Factory OSとは別の稼働中オーケストレーターが確認されたわけではない。
5. config.tomlだけでなくプラグイン内にもMCPがあるため、直登録MCPの件数だけでは全体を把握できない。
6. この調査では設定を復元・有効化していない。

## 詳細根拠：各スキルの保存元と説明

以下はバックアップ中のSKILL.mdから抽出した説明。プラグイン内の補助・テンプレート用SKILL.mdも含み、すべてが当時のメニューに公開されていたことを意味しない。

- **agentcad** — [.agents/skills/agentcad/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/agentcad/SKILL.md)
  - >- Mouse CAD choice 5: Stella_Agentcad MCP. Do not run n3r/AgentCAD at vendor\agentcad. Do not use during text-to-cad, ForgeCAD, OpenSCAD, or AI-CAD sessions.

- **ai-cad** — [.agents/skills/ai-cad/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/ai-cad/SKILL.md)
  - >- Run the ai-cad-labs AI-CAD harness (CadQuery, DFM/DFA gates, 8-view renders, multi-agent design runs). Use when the user picks AI-CAD / aicad / ai-cad-labs, or cad-session.json tool is ai-cad. Do not use for ZA13 mouse work, cadgen, build123d, ForgeCAD, OpenSCAD, or AgentCAD sessions.

- **architecture-hdvs** — [.codex/skills/architecture-hdvs/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/skills/architecture-hdvs/SKILL.md)
  - 高密度垂直スライス（High-Density Vertical Slice）アーキテクチャの詳細ルール。UI/DSP/Tauri デスクトップアプリの両方に対応。ディレクトリ構造の設計、featureの追加、依存関係の設計、ARCHITECTURE.mdの更新、f64音質保護が必要な audio/DSP プロジェクトで参照する。

- **architecture-hdvs** — [.agents/skills/architecture-hdvs/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/architecture-hdvs/SKILL.md)
  - 高密度垂直スライス（High-Density Vertical Slice）アーキテクチャの詳細ルール。UI/DSP/Tauri デスクトップアプリの両方に対応。ディレクトリ構造の設計、featureの追加、依存関係の設計、ARCHITECTURE.mdの更新、f64音質保護が必要な audio/DSP プロジェクトで参照する。

- **bambu-labs** — [.agents/skills/bambu-labs/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/bambu-labs/SKILL.md)
  - Dry-run, upload, and cautiously initiate local Bambu Lab print jobs from validated plain `.gcode`, using Bambu LAN FTPS/MQTT handoffs.

- **cad** — [.agents/skills/cad/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/cad/SKILL.md)
  - Create, modify, inspect, and validate parametric CAD parts and assemblies authored as cadgen model scripts. Use for natural-language CAD specs, reference images, 2D technical drawings, STEP/STP generation or direct inspection, Python CAD source, source-level joints, selector references, geometry facts, measurements, mating deltas, snapshots, and STL/3MF/native GLB outputs from CAD geometry. Also covers project structure for multi-part CAD work - src/ for model scripts and shared code, format folders (STEP/, DXF/, STL/) for raw outputs, naming, and commit policy for projects with several @step/@dxf model scripts and imported source files; use it when starting a CAD project with more than a couple of models, when asked how to organize CAD code and artifacts, or when growing a flat folder of models into a project.

- **cad-viewer** — [.agents/skills/cad-viewer/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/cad-viewer/SKILL.md)
  - Start CAD Viewer and return review links for CAD and robot-description files. Use when visually reviewing `.step`, `.stp`, `.glb`, `.stl`, `.3mf`, `.dxf`, `.urdf`, `.srdf`, or `.sdf` files, especially when handed off from CAD, URDF, SRDF, or SDF generation skills.

- **dfam-check** — [.agents/skills/dfam-check/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/dfam-check/SKILL.md)
  - Measure mesh files against Design for Additive Manufacturing (DfAM) rules and report printability findings per process (FDM, SLS, SLA/DLP, metal PBF, MJF). Use when the user asks whether a part is printable, wants overhang/wall-thickness/support analysis of an `.stl`, `.obj`, `.ply`, or `.3mf` mesh, wants a build-orientation recommendation, or wants DfAM redesign guidance before slicing with `$gcode` or regenerating geometry with `$cad`.

- **dxf** — [.agents/skills/dxf/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/dxf/SKILL.md)
  - Generate, regenerate, and validate 2D DXF drawings from Python build123d sources. Use for DXF files, `.py` drawing scripts, @dxf models, 2D profiles, outlines, templates, gaskets, panels, flat patterns, laser/plasma/waterjet cut layouts, and 2D drawing exports of CAD geometry.

- **forgecad** — [.codex/skills/forgecad/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/skills/forgecad/SKILL.md)
  - ForgeCAD model authoring, editing, debugging, and execution guidance for .forge.js, SVG-import, assembly, and CLI workflows. Use when building or modifying ForgeCAD geometry, structuring multi-file projects, validating scripts, or using ForgeCAD export/render tooling.

- **forgecad** — [.agents/skills/forgecad/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/forgecad/SKILL.md)
  - ForgeCAD model authoring, editing, debugging, and execution guidance for .forge.js, SVG-import, assembly, and CLI workflows. Use when building or modifying ForgeCAD geometry, structuring multi-file projects, validating scripts, or using ForgeCAD export/render tooling.

- **forgecad-build-model** — [.codex/skills/forgecad-build-model/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/skills/forgecad-build-model/SKILL.md)
  - Build or edit `.forge.js` real product models through design, automatic/manual feedback gathering, inspection/simulation/FEA evidence, and iteration until ready.

- **forgecad-build-model** — [.agents/skills/forgecad-build-model/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/forgecad-build-model/SKILL.md)
  - Build or edit `.forge.js` real product models through design, automatic/manual feedback gathering, inspection/simulation/FEA evidence, and iteration until ready.

- **forgecad-image-prompt** — [.codex/skills/forgecad-image-prompt/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/skills/forgecad-image-prompt/SKILL.md)
  - Write builder-honest AI image prompts from a concrete ForgeCAD model, build brief, HLD, or LLD without hiding how the artifact is built.

- **forgecad-image-prompt** — [.agents/skills/forgecad-image-prompt/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/forgecad-image-prompt/SKILL.md)
  - Write builder-honest AI image prompts from a concrete ForgeCAD model, build brief, HLD, or LLD without hiding how the artifact is built.

- **forgecad-project-sync** — [.codex/skills/forgecad-project-sync/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/skills/forgecad-project-sync/SKILL.md)
  - Manage hosted ForgeCAD project sync from the CLI: init, clone, pull, push, file operations, members, publishing, and shares.

- **forgecad-project-sync** — [.agents/skills/forgecad-project-sync/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/forgecad-project-sync/SKILL.md)
  - Manage hosted ForgeCAD project sync from the CLI: init, clone, pull, push, file operations, members, publishing, and shares.

- **forgecad-reconstruct-cad-file** — [.codex/skills/forgecad-reconstruct-cad-file/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/skills/forgecad-reconstruct-cad-file/SKILL.md)
  - Reconstruct a readable parametric ForgeCAD model from an existing CAD or mesh file such as STL, OBJ, 3MF, STEP, or STP.

- **forgecad-reconstruct-cad-file** — [.agents/skills/forgecad-reconstruct-cad-file/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/forgecad-reconstruct-cad-file/SKILL.md)
  - Reconstruct a readable parametric ForgeCAD model from an existing CAD or mesh file such as STL, OBJ, 3MF, STEP, or STP.

- **forgecad-reconstruct-from-images** — [.codex/skills/forgecad-reconstruct-from-images/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/skills/forgecad-reconstruct-from-images/SKILL.md)
  - Reconstruct a real parametric ForgeCAD object from reference images by using images as evidence, not as a one-view facade.

- **forgecad-reconstruct-from-images** — [.agents/skills/forgecad-reconstruct-from-images/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/forgecad-reconstruct-from-images/SKILL.md)
  - Reconstruct a real parametric ForgeCAD object from reference images by using images as evidence, not as a one-view facade.

- **gcode** — [.agents/skills/gcode/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/gcode/SKILL.md)
  - Generate, inspect, dry-run, and statically validate plain FDM `.gcode` from 3D mesh files by orchestrating real slicer CLIs. Use when Codex needs to slice `.stl`, `.obj`, unsliced `.3mf`, `.ply`, `.glb`, or `.gltf` into printer-profiled G-code, discover local slicer backends, inspect whether a mesh is slice-ready, or validate generated G-code before any printer-specific handoff.

- **mesh-to-precision-solid** — [.codex/skills/mesh-to-precision-solid/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/skills/mesh-to-precision-solid/SKILL.md)
  - メッシュ・STL・三角面の多いSTEPを、形状と寸法を測定しながら閉じたソリッドへ修復する。形状をほぼ保った軽量化、曲面再構築、メッシュ由来のFusionモデルが重い場合にも使う。単なるファイル移動や新規CAD設計には適用しない。

- **openscad-design** — [.agents/skills/openscad-design/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/openscad-design/SKILL.md)
  - Design, modify, and verify 3D-printable parts and assemblies in OpenSCAD through the openscad-mcp tools. Use when the user asks for a bracket, enclosure, adapter, jig, or other parametric part, or wants an existing .scad file changed, measured, fit-checked, or exported for printing.

- **sdf** — [.agents/skills/sdf/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/sdf/SKILL.md)
  - SDFormat/SDF model and world authoring, validation, and simulator handoff. Use for `.sdf` files, SDFormat XML, models, worlds, links, joints, poses, frames, inertials, visual/collision geometry, mesh URIs, sensors, lights, physics, plugins, includes, Gazebo, static SDF review, or simulator-specific metadata. Do not use for signed-distance-field geometry.

- **sendcutsend** — [.agents/skills/sendcutsend/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/sendcutsend/SKILL.md)
  - Review DXF and STEP/STP uploads for SendCutSend.com orders using its ordering guide, catalog, and specs. Use only for SendCutSend.com preflight reports covering upload readiness, selected material/SKU/thickness/service availability, and service-specific checks for laser cutting, CNC routing, bending, tapping, countersinking, hardware insertion, and finishing.

- **srdf** — [.agents/skills/srdf/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/srdf/SKILL.md)
  - MoveIt2 SRDF authoring, validation, and planning-semantics workflow. Use when creating, editing, inspecting, or validating `.srdf` files, MoveIt planning groups, virtual joints, passive joints, end effectors, group states, disabled collisions, URDF-paired planning semantics, or SRDF handoff for live review. Use the URDF skill for robot structure, the SDF skill for simulator descriptions, and the cad-viewer skill for rendering and live review links.

- **step-parts** — [.agents/skills/step-parts/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/step-parts/SKILL.md)
  - Find, evaluate, and download common purchasable CAD parts from step.parts, including named off-the-shelf actuators, servos, motors, electronics boards, connectors, screws, bolts, nuts, washers, bearings, standoffs, and other catalog components. Use when Codex needs to search the hosted step.parts catalog before creating simplified placeholder geometry, resolve fuzzy part names, standards, aliases, or dimensions, choose a matching part, fetch a canonical .step file, verify checksums, or use the step.parts API/OpenAPI/catalog endpoints for standard part discovery.

- **urdf** — [.agents/skills/urdf/SKILL.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.agents/skills/urdf/SKILL.md)
  - URDF robot description authoring and validation. Use when creating, editing, inspecting, validating, or debugging `.urdf` files, robot links, joints, limits, inertials, visual/collision geometry, mesh references, frame conventions, or robot-description artifacts. Use the SRDF skill for MoveIt2 semantic groups and IK/path-planning semantics; use the CAD skill for STEP/STL/3MF/DXF/GLB outputs.

### browser@openai-bundled

### cad@text-to-cad
- **bambu-labs**：Dry-run, upload, and cautiously initiate local Bambu Lab print jobs from validated plain `.gcode`, using Bambu LAN FTPS/MQTT handoffs.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/text-to-cad/cad/0.6.5/skills/bambu-labs/SKILL.md)
- **cad**：Create/edit parametric CAD models, organize CAD projects, export STEP/STL/3MF/GLB files, resolve prompt references, and measure geometry with cadgen.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/text-to-cad/cad/0.6.5/skills/cad/SKILL.md)
- **cad-viewer**：Start CAD Viewer and return review links for CAD and robot-description files. Use when visually reviewing `.step`, `.stp`, `.glb`, `.stl`, `.3mf`, `.dxf`, `.urdf`, `.srdf`, or `.sdf` files, especially when handed off from CAD, URDF, SRDF, or SDF generation skills.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/text-to-cad/cad/0.6.5/skills/cad-viewer/SKILL.md)
- **dfam-check**：Measure mesh files against Design for Additive Manufacturing (DfAM) rules and report printability findings per process (FDM, SLS, SLA/DLP, metal PBF, MJF). Use when the user asks whether a part is printable, wants overhang/wall-thickness/support analysis of an `.stl`, `.obj`, `.ply`, or `.3mf` mesh, wants a build-orientation recommendation, or wants DfAM redesign guidance before slicing with `$gcode` or regenerating geometry with `$cad`.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/text-to-cad/cad/0.6.5/skills/dfam-check/SKILL.md)
- **dxf**：Generate, regenerate, and validate 2D DXF drawings from Python build123d sources. Use for DXF files, `.py` drawing scripts, @dxf models, 2D profiles, outlines, templates, gaskets, panels, flat patterns, laser/plasma/waterjet cut layouts, and 2D drawing exports of CAD geometry.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/text-to-cad/cad/0.6.5/skills/dxf/SKILL.md)
- **gcode**：Generate, inspect, dry-run, and statically validate plain FDM `.gcode` from 3D mesh files by orchestrating real slicer CLIs. Use when Codex needs to slice `.stl`, `.obj`, unsliced `.3mf`, `.ply`, `.glb`, or `.gltf` into printer-profiled G-code, discover local slicer backends, inspect whether a mesh is slice-ready, or validate generated G-code before any printer-specific handoff.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/text-to-cad/cad/0.6.5/skills/gcode/SKILL.md)
- **sdf**：SDFormat/SDF model and world authoring, validation, and simulator handoff. Use for `.sdf` files, SDFormat XML, models, worlds, links, joints, poses, frames, inertials, visual/collision geometry, mesh URIs, sensors, lights, physics, plugins, includes, Gazebo, static SDF review, or simulator-specific metadata. Do not use for signed-distance-field geometry.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/text-to-cad/cad/0.6.5/skills/sdf/SKILL.md)
- **sendcutsend**：Review DXF and STEP/STP uploads for SendCutSend.com orders using its ordering guide, catalog, and specs. Use only for SendCutSend.com preflight reports covering upload readiness, selected material/SKU/thickness/service availability, and service-specific checks for laser cutting, CNC routing, bending, tapping, countersinking, hardware insertion, and finishing.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/text-to-cad/cad/0.6.5/skills/sendcutsend/SKILL.md)
- **srdf**：MoveIt2 SRDF authoring, validation, and planning-semantics workflow. Use when creating, editing, inspecting, or validating `.srdf` files, MoveIt planning groups, virtual joints, passive joints, end effectors, group states, disabled collisions, URDF-paired planning semantics, or SRDF handoff for live review. Use the URDF skill for robot structure, the SDF skill for simulator descriptions, and the cad-viewer skill for rendering and live review links.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/text-to-cad/cad/0.6.5/skills/srdf/SKILL.md)
- **step-parts**：Find, evaluate, and download common purchasable CAD parts from step.parts, including named off-the-shelf actuators, servos, motors, electronics boards, connectors, screws, bolts, nuts, washers, bearings, standoffs, and other catalog components. Use when Codex needs to search the hosted step.parts catalog before creating simplified placeholder geometry, resolve fuzzy part names, standards, aliases, or dimensions, choose a matching part, fetch a canonical .step file, verify checksums, or use the step.parts API/OpenAPI/catalog endpoints for standard part discovery.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/text-to-cad/cad/0.6.5/skills/step-parts/SKILL.md)
- **urdf**：URDF robot description authoring and validation. Use when creating, editing, inspecting, validating, or debugging `.urdf` files, robot links, joints, limits, inertials, visual/collision geometry, mesh references, frame conventions, or robot-description artifacts. Use the SRDF skill for MoveIt2 semantic groups and IK/path-planning semantics; use the CAD skill for STEP/STL/3MF/DXF/GLB outputs.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/text-to-cad/cad/0.6.5/skills/urdf/SKILL.md)
- **smui**：説明メタデータなし
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/text-to-cad/cad/0.6.5/apps/viewer/skills/smui/SKILL.md)

### chrome@openai-bundled

### codex-app-tools@openai-bundled

### computer-use@openai-bundled
- **computer-use**：Control Windows apps from ChatGPT
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-bundled/computer-use/26.915.31945/skills/computer-use/SKILL.md)

### data-analytics@openai-curated-remote
- **analyze-data-quality**：Investigate whether structured datasets and query results are trustworthy enough to use. Use for underlying data-quality risks such as freshness, grain, missingness, duplicates, broken joins, schema drift, and conflicting source results.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/analyze-data-quality/SKILL.md)
- **build-dashboard**：Build or update a source-backed interactive dashboard for monitoring, exploration, and operational decisions from connected data, uploaded spreadsheets, CSVs, or other structured sources.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/build-dashboard/SKILL.md)
- **build-report**：Build polished analytical reports for executive, product, business, or technical audiences. Use when the task needs a durable narrative answer supported by inspectable evidence.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/build-report/SKILL.md)
- **convert-to-doc**：Create a polished DOCX or Google Doc from an existing Data app.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/convert-to-doc/SKILL.md)
- **convert-to-slides**：Create a polished PowerPoint or Google Slides deck from an existing Data app.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/convert-to-slides/SKILL.md)
- **create-data-context**：Create, update, or share reusable context for analysis, reports, and dashboards, including tool preferences, look and feel, analysis practices, and data definitions. Use when asked to remember a working instruction for future tasks, save conventions, or maintain existing context.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/create-data-context/SKILL.md)
- **design-kpis**：Design KPI frameworks, metric definitions, targets, guardrails, and measurement plans for product or business decisions. Use when success metrics, drivers, guardrails, targets, or the measurement approach need to be defined or improved.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/design-kpis/SKILL.md)
- **gather-business-context**：Gather business context from connected or provided sources so downstream analysis starts with the right framing. Use when an analytical question depends on missing context, such as what a metric means, what changed recently, or which sources should be checked. If the same prompt asks for diagnosis, recommendation, or a deliverable, gather context first and continue to the focused skill.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/gather-business-context/SKILL.md)
- **index**：Use Data for analysis, metric definitions and diagnostics, KPI reporting, data quality checks, market sizing, and evidence-based product or business decisions; creating, updating, validating, exporting, or sharing dashboards, data-driven reports, charts, and analytical notebooks; and managing reusable Data context. Do not use Data for general writing, editing, coding, or explanations that require none of these workflows.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/index/SKILL.md)
- **jupyter-notebooks**：Create, edit, or validate reproducible SQL or Python notebooks. Use for notebooks, SQL/Python scratchpads, reproducible exploration, audit trails, or runnable companions where the analysis should be reviewable or rerunnable.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/jupyter-notebooks/SKILL.md)
- **kpi-reporting**：Prepare KPI readouts, scorecards, WBR/MBR/QBR updates, and executive summaries from quantitative business or product metrics; use when the task is to report status, compare against targets, explain validated drivers, and state operating implications.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/kpi-reporting/SKILL.md)
- **market-sizing**：Estimate market, segment, or opportunity size with transparent assumptions and uncertainty. Use for TAM/SAM/SOM, sizing scenarios, or comparing the scale of possible opportunities.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/market-sizing/SKILL.md)
- **metric-diagnostics**：Diagnose why a metric changed or differs from expectation. Use when the task is to identify likely drivers of a metric movement, anomaly, gap, or discrepancy.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/metric-diagnostics/SKILL.md)
- **product-business-analysis**：Analyze product or business data to support a decision or recommendation. Use when a decision depends on metric-backed evidence, such as choosing a direction, prioritizing an opportunity, evaluating a change, segmenting users, sizing tradeoffs, or deciding what to do next.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/product-business-analysis/SKILL.md)
- **publish-artifact-to-sites**：Publish an existing Data report or dashboard to Sites, automatically for web/cloud tasks or when the user requests publication.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/publish-artifact-to-sites/SKILL.md)
- **report-to-pdf**：Create a polished PDF from an existing Data dashboard or report.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/report-to-pdf/SKILL.md)
- **schedule-refresh-jobs**：Create or update recurring cloud refresh jobs for an existing Data dashboard or report, including requests to keep it up to date.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/schedule-refresh-jobs/SKILL.md)
- **share-artifact-summary**：Share or provide a concise Data dashboard, report, chart, or component summary.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/share-artifact-summary/SKILL.md)
- **validate-data**：Validate analysis methodology, sources, calculations, visuals, and conclusions, including report and dashboard completeness, usability, and supported repairs.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/validate-data/SKILL.md)
- **visualize-data**：Design, build, revise, and verify quantitative charts and figures while authoring reports, dashboards, notebooks, and other durable artifacts. Do not use for inline chat charts.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.9/skills/visualize-data/SKILL.md)

### documents@openai-primary-runtime
- **documents**：Create, edit, redline, and comment on `.docx`, Word, and Google Docs-targeted document artifacts inside the container, with a strict render-and-verify workflow. Use `render_docx.py` to generate page PNGs (and optional PDF) for visual QA, then iterate until layout is flawless before delivering the final document.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-primary-runtime/documents/26.904.11930/skills/documents/SKILL.md)

### github@openai-curated
- **gh-address-comments**：Address actionable GitHub pull request review feedback. Use when the user wants to inspect unresolved review threads, requested changes, or inline review comments on a PR, then implement selected fixes. Use the GitHub app for PR metadata and flat comment reads, and use the bundled GraphQL script via `gh` whenever thread-level state, resolution status, or inline review context matters.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/github/bd2122cb/skills/gh-address-comments/SKILL.md)
- **gh-fix-ci**：Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions. Use the GitHub app from this plugin for PR metadata and patch context, and use `gh` for Actions check and log inspection before implementing any approved fix.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/github/bd2122cb/skills/gh-fix-ci/SKILL.md)
- **github**：Triage and orient GitHub repository, pull request, and issue work through the connected GitHub app. Use when the user asks for general GitHub help, wants PR or issue summaries, or needs repository context before choosing a more specific GitHub workflow.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/github/bd2122cb/skills/github/SKILL.md)
- **yeet**：Publish local changes to GitHub by confirming scope, committing intentionally, pushing the branch, and opening a draft PR through the GitHub app from this plugin, with `gh` used only as a fallback where connector coverage is insufficient.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/github/bd2122cb/skills/yeet/SKILL.md)

### github@openai-curated-remote

### hugging-face@openai-curated
- **hf-cli**：Hugging Face Hub CLI (`hf`) for downloading, uploading, and managing repositories, models, datasets, and Spaces on the Hugging Face Hub. Replaces now deprecated `huggingface-cli` command.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/hugging-face/bd2122cb/skills/cli/SKILL.md)
- **huggingface-community-evals**：Run evaluations for Hugging Face Hub models using inspect-ai and lighteval on local hardware. Use for backend selection, local GPU evals, and choosing between vLLM / Transformers / accelerate. Not for HF Jobs orchestration, model-card PRs, .eval_results publication, or community-evals automation.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/hugging-face/bd2122cb/skills/community-evals/SKILL.md)
- **huggingface-datasets**：Use this skill for Hugging Face Dataset Viewer API workflows that fetch subset/split metadata, paginate rows, search text, apply filters, download parquet URLs, and read size or statistics.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/hugging-face/bd2122cb/skills/datasets/SKILL.md)
- **huggingface-gradio**：Build Gradio web UIs and demos in Python. Use when creating or editing Gradio apps, components, event listeners, layouts, or chatbots.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/hugging-face/bd2122cb/skills/gradio/SKILL.md)
- **huggingface-jobs**：This skill should be used when users want to run any workload on Hugging Face Jobs infrastructure. Covers UV scripts, Docker-based jobs, hardware selection, cost estimation, authentication with tokens, secrets management, timeout configuration, and result persistence. Designed for general-purpose compute workloads including data processing, inference, experiments, batch jobs, and any Python-based tasks. Should be invoked for tasks involving cloud compute, GPU workloads, or when users mention running jobs on Hugging Face infrastructure without local setup.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/hugging-face/bd2122cb/skills/jobs/SKILL.md)
- **huggingface-llm-trainer**：This skill should be used when users want to train or fine-tune language models using TRL (Transformer Reinforcement Learning) on Hugging Face Jobs infrastructure. Covers SFT, DPO, GRPO and reward modeling training methods, plus GGUF conversion for local deployment. Includes guidance on the TRL Jobs package, UV scripts with PEP 723 format, dataset preparation and validation, hardware selection, cost estimation, Trackio monitoring, Hub authentication, and model persistence. Should be invoked for tasks involving cloud GPU training, GGUF conversion, or when users mention training on Hugging Face Jobs without local GPU setup.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/hugging-face/bd2122cb/skills/llm-trainer/SKILL.md)
- **huggingface-paper-publisher**：Publish and manage research papers on Hugging Face Hub. Supports creating paper pages, linking papers to models/datasets, claiming authorship, and generating professional markdown-based research articles.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/hugging-face/bd2122cb/skills/paper-publisher/SKILL.md)
- **huggingface-papers**：Look up and read Hugging Face paper pages in markdown, and use the papers API for structured metadata such as authors, linked models/datasets/spaces, Github repo and project page. Use when the user shares a Hugging Face paper page URL, an arXiv URL or ID, or asks to summarize, explain, or analyze an AI research paper.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/hugging-face/bd2122cb/skills/papers/SKILL.md)
- **huggingface-trackio**：Track and visualize ML training experiments with Trackio. Use when logging metrics during training (Python API), firing alerts for training diagnostics, or retrieving/analyzing logged metrics (CLI). Supports real-time dashboard visualization, alerts with webhooks, HF Space syncing, and JSON output for automation.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/hugging-face/bd2122cb/skills/trackio/SKILL.md)
- **transformers-js**：Use Transformers.js to run state-of-the-art machine learning models directly in JavaScript/TypeScript. Supports NLP (text classification, translation, summarization), computer vision (image classification, object detection), audio (speech recognition, audio classification), and multimodal tasks. Works in Node.js and browsers (with WebGPU/WASM) using pre-trained models from Hugging Face Hub.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/hugging-face/bd2122cb/skills/transformers.js/SKILL.md)
- **huggingface-vision-trainer**：Trains and fine-tunes vision models for object detection (D-FINE, RT-DETR v2, DETR, YOLOS), image classification (timm models — MobileNetV3, MobileViT, ResNet, ViT/DINOv3 — plus any Transformers classifier), and SAM/SAM2 segmentation using Hugging Face Transformers on Hugging Face Jobs cloud GPUs. Covers COCO-format dataset preparation, Albumentations augmentation, mAP/mAR evaluation, accuracy metrics, SAM segmentation with bbox/point prompts, DiceCE loss, hardware selection, cost estimation, Trackio monitoring, and Hub persistence. Use when users mention training object detection, image classification, SAM, SAM2, segmentation, image matting, DETR, D-FINE, RT-DETR, ViT, timm, MobileNet, ResNet, bounding box models, or fine-tuning vision models on Hugging Face Jobs.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/hugging-face/bd2122cb/skills/vision-trainer/SKILL.md)

### mechanical-cad@personal
- **mechanical-cad-orchestrator**：Design, modify, and evaluate physical mechanical parts and assemblies using Text-to-CAD, Fusion MCP and DfAM. Use implicitly for CAD/3D CAD, STEP/STP, STL/3MF, Fusion 360, build123d, 機械設計, 部品設計, PCB cases/enclosures, brackets, mounts, holders, jigs/fixtures, chassis, screw bosses, ribs, hinges, physical buttons/switch mechanisms, gaming mouse shells/internals, dimensioned or moving objects and 3Dプリント部品, even without CAD keywords. Do not use for software UI buttons, programming classes/cases, or purely illustrative 3D art; resolve ambiguous physical versus UI context first.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/personal/mechanical-cad/0.1.0/skills/mechanical-cad-orchestrator/SKILL.md)

### nvidia@openai-curated
- **aiq-deploy**：| Use when asked to install, deploy, run, validate, troubleshoot, or stop NVIDIA AI-Q Blueprint infrastructure.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/nvidia/bd2122cb/skills/aiq-deploy/SKILL.md)
- **aiq-research**：| Use when asked to run deep research or AI-Q research through a reachable NVIDIA AI-Q Blueprint backend.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/nvidia/bd2122cb/skills/aiq-research/SKILL.md)
- **cuopt-user-rules**：Base rules for end users calling NVIDIA cuOpt (routing/LP/MILP/QP/install/server). Not for cuOpt internals — use cuopt-developer for those.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/nvidia/bd2122cb/skills/cuopt-user-rules/SKILL.md)
- **dynamo-interconnect-check**：Validate that a Dynamo deployment's NIXL/UCX/NCCL interconnect is ready for disaggregated serving over RDMA/NVLink. Use after recipe-runner brings a deployment up (especially disagg/multi-node) to confirm the KV transport is correct; use troubleshoot for diagnosing already-failed pods.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/nvidia/bd2122cb/skills/dynamo-interconnect-check/SKILL.md)
- **dynamo-router-starter**：Start or patch Dynamo router modes and run router endpoint smoke checks. Use for round-robin, KV-aware, least-loaded, or device-aware routing setup; use recipe-runner for recipe deployment and troubleshoot for failure diagnosis.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/nvidia/bd2122cb/skills/dynamo-router-starter/SKILL.md)
- **nemoclaw-user-get-started**：Installs NemoClaw, launches a sandbox, and runs the first agent prompt. Use when onboarding, installing, or launching a NemoClaw sandbox for the first time. Trigger keywords - nemoclaw quickstart, install nemoclaw openclaw sandbox, nemohermes quickstart, hermes agent nemoclaw, run hermes openshell sandbox, nemoclaw prerequisites, nemoclaw supported platforms, nemoclaw hardware software, nemoclaw windows wsl2 setup, nemoclaw install windows docker desktop.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/nvidia/bd2122cb/skills/nemoclaw-user-get-started/SKILL.md)
- **omniverse-cad-to-simready**：Coordinate the end-to-end CAD/source-asset to SimReady workflow. Use for broad requests such as CAD to SimReady, source asset to simulation-ready USD, or prop packaging that require conversion, material/physics assignment, SimReady conformance, validation, and optional package creation; deploy or verify Content Agents services first when property assignment is enabled; route single-stage work through nested references.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/nvidia/bd2122cb/skills/omniverse-cad-to-simready/SKILL.md)
- **omniverse-realtime-viewer**：Use as the top-level router for Omniverse Realtime Viewer USD app requests and focused viewer reference documents.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/nvidia/bd2122cb/skills/omniverse-realtime-viewer/SKILL.md)
- **omniverse-usd-performance-tuning**：Top-level workflow skill for USD performance diagnosis and optimization. Use for slow loading, high memory, low FPS, or 'optimize my scene' requests; delegates auth/runtime setup to Phase 0 owners.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/nvidia/bd2122cb/skills/omniverse-usd-performance-tuning/SKILL.md)
- **physical-ai-infrastructure-setup-and-resilient-scaling**：>- Use when the user wants to set up, scale, validate, or harden NVIDIA physical AI infrastructure for synthetic data generation workflows across local MicroK8s or Azure AKS, including Kubernetes clusters, inference endpoint deployment, OSMO deployment, workload submission readiness, and infrastructure failure recovery. Trigger keywords: physical ai infrastructure, resilient scaling, SDG infrastructure, microk8s, azure aks, NVCF deployment, NIM Operator, OSMO deploy, workflow scaling. Don't trigger for: OSMO log summarization or workload-only operations unless infrastructure setup, scaling, validation, or recovery is requested.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/nvidia/bd2122cb/skills/physical-ai-infrastructure-setup-and-resilient-scaling/SKILL.md)
- **physical-ai-neural-reconstruction**：Router for NVIDIA NuRec/NRE: USDZ rendering, NCore conversion, 3DGS, gRPC sensor sim, PhysicalAI HF datasets. Do NOT use for SimReady or infra setup.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated/nvidia/bd2122cb/skills/physical-ai-neural-reconstruction/SKILL.md)

### openai-templates@openai-curated-remote
- **artifact-template-analytics-dashboard**：Create a spreadsheet using the Analytics Dashboard template and its retained reference file. Use when the user selects or names Analytics Dashboard. Monitor acquisition, engagement, retention, revenue, and conversion funnel KPIs with charts.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-analytics-dashboard/SKILL.md)
- **artifact-template-business-review**：Create a presentation using the Business Review template and its retained reference file. Use when the user selects or names Business Review. Review business performance, KPIs, segment results, strategic priorities, decisions, and outlook.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-business-review/SKILL.md)
- **artifact-template-design-report**：Create a document using the Design Report template and its retained reference file. Use when the user selects or names Design Report. Produce design reports with an executive summary, key findings, implications, recommendations, and appendix.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-design-report/SKILL.md)
- **artifact-template-experiment-analysis**：Create a document using the Experiment Analysis template and its retained reference file. Use when the user selects or names Experiment Analysis. Analyze experiments with hypotheses, methodology, results, interpretation, limitations, and next steps.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-experiment-analysis/SKILL.md)
- **artifact-template-financial-budget**：Create a spreadsheet using the Financial Budget template and its retained reference file. Use when the user selects or names Financial Budget. Model actuals, budget and scenario forecasts, variances, cash runway, and departmental plans.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-financial-budget/SKILL.md)
- **artifact-template-investment-committee-memo**：Create a document using the Investment Committee Memo template and its retained reference file. Use when the user selects or names Investment Committee Memo. Prepare investment committee memos with the thesis, transaction details, financial analysis, risks, and recommendation.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-investment-committee-memo/SKILL.md)
- **artifact-template-legal-memorandum**：Create a document using the Legal Memorandum template and its retained reference file. Use when the user selects or names Legal Memorandum. Draft legal memoranda with the issue, brief answer, relevant facts, analysis, and conclusion.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-legal-memorandum/SKILL.md)
- **artifact-template-market-trends-report**：Create a presentation using the Market Trends Report template and its retained reference file. Use when the user selects or names Market Trends Report. Communicate market or industry trends, supporting evidence, implications, and recommended responses.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-market-trends-report/SKILL.md)
- **artifact-template-minimal-letterhead**：Create a document using the Minimal Letterhead template and its retained reference file. Use when the user selects or names Minimal Letterhead. Write professional business letters with sender, recipient, message, and signature fields in a minimal letterhead layout.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-minimal-letterhead/SKILL.md)
- **artifact-template-operating-calendar**：Create a spreadsheet using the Operating Calendar template and its retained reference file. Use when the user selects or names Operating Calendar. Plan annual and monthly operating milestones, campaigns, launches, deadlines, and recurring events.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-operating-calendar/SKILL.md)
- **artifact-template-operating-review**：Create a presentation using the Operating Review template and its retained reference file. Use when the user selects or names Operating Review. Run weekly operating reviews with scorecards, functional updates, risks, decisions, and action items.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-operating-review/SKILL.md)
- **artifact-template-project-kickoff**：Create a presentation using the Project Kickoff template and its retained reference file. Use when the user selects or names Project Kickoff. Align teams on project goals, scope, roles, milestones, risks, and the working model.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-project-kickoff/SKILL.md)
- **artifact-template-project-tracker**：Create a spreadsheet using the Project Tracker template and its retained reference file. Use when the user selects or names Project Tracker. Manage workstreams, tasks, owners, status, priority, dates, launch pulse, and a Gantt schedule.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-project-tracker/SKILL.md)
- **artifact-template-sales-pipeline**：Create a spreadsheet using the Sales Pipeline template and its retained reference file. Use when the user selects or names Sales Pipeline. Track opportunities, stages, owners, deal sizes, probabilities, forecasts, next steps, and risks.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-sales-pipeline/SKILL.md)
- **artifact-template-simple-dark-mode**：Create a presentation using the Simple Dark Mode template and its retained reference file. Use when the user selects or names Simple Dark Mode. Create clean dark-mode presentations with bold typography, simple sections, charts, and imagery.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-simple-dark-mode/SKILL.md)
- **artifact-template-simple-light-mode**：Create a presentation using the Simple Light Mode template and its retained reference file. Use when the user selects or names Simple Light Mode. Create clean light-mode presentations with spacious typography, simple sections, charts, and imagery.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-simple-light-mode/SKILL.md)
- **artifact-template-strategy-memorandum**：Create a document using the Strategy Memorandum template and its retained reference file. Use when the user selects or names Strategy Memorandum. Present strategic context, choices, rationale, risks, milestones, and a clear recommendation.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-strategy-memorandum/SKILL.md)
- **artifact-template-system-design**：Create a document using the System Design template and its retained reference file. Use when the user selects or names System Design. Document system architecture, requirements, components, data flows, APIs, tradeoffs, and operational considerations.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-system-design/SKILL.md)
- **artifact-template-team-alignment**：Create a presentation using the Team Alignment template and its retained reference file. Use when the user selects or names Team Alignment. Facilitate team offsites and planning with context, goals, priorities, decisions, and action items.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-team-alignment/SKILL.md)
- **artifact-template-three-statement-forecast**：Create a spreadsheet using the Three-Statement Forecast template and its retained reference file. Use when the user selects or names Three-Statement Forecast. Build an integrated income statement, balance sheet, and cash flow forecast with assumptions, checks, and an executive summary.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-three-statement-forecast/SKILL.md)

### pdf@openai-primary-runtime
- **pdf**：Read, create, inspect, render, and verify PDF files where visual layout matters, including fillable AcroForms. Use Poppler rendering plus Python tools such as reportlab, pdfplumber, and pypdf for generation and extraction.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-primary-runtime/pdf/26.904.11930/skills/pdf/SKILL.md)

### plugin-management@openai-curated-remote
- **plugin-management**：Discover and suggest relevant plugins, inspect app permissions and dependencies, and manage plugin connections or removal. Use when the user asks about plugins or when a task would materially benefit from an external app, account, service, or data source that available tools cannot access.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-curated-remote/plugin-management/0.1.0/skills/plugin-management/SKILL.md)

### presentations@openai-primary-runtime
- **Presentations**：Read, create or edit PowerPoint or Google Slides decks. Use for presentation, slide deck, PowerPoint, PPT, PPTX, or Google Slides requests.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations/SKILL.md)

### spreadsheets@openai-primary-runtime
- **excel-live-control**：Control an open or active Microsoft Excel workbook through the ChatGPT add-in or connected session. Use when the user tags the Microsoft Excel app in Codex or follows up on an established live Excel task. Do not use for standalone spreadsheet files or Google Sheets.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.904.11930/skills/excel-live-control/SKILL.md)
- **Spreadsheets**：Create, edit, analyze, and verify standalone spreadsheet files or Google Sheets-ready workbooks, including .xlsx, .xls, .csv, and .tsv. Do not use for live controlling Microsoft Excel app or a live Excel session.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.904.11930/skills/spreadsheets/SKILL.md)

### template-creator@openai-primary-runtime
- **template-creator**：Create or update a reusable personal Codex artifact-template skill. Use when the user invokes $template-creator or asks in natural language to create a reusable template from a reference document, presentation, spreadsheet, Google Docs, Slides, or Sheets link, ImageGen or Product Design image, email, Slack message, or Site project, or explicitly asks to edit or update a passed artifact-template skill. Do not use for one-off creation from an existing template.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-primary-runtime/template-creator/26.904.11930/skills/template-creator/SKILL.md)

### unified-computer-use@openai-bundled

### visualize@openai-bundled
- **visualize**：Create visualizations and interactive tools directly in conversation. Proactively use to show how something works; explore 'what happens when', 'what changes', or 'help me understand'; compare or inspect; create simulations, maps, charts, graphs, and mockups. Use standard tools for static scientific figures.
  - [保存元](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/plugins/cache/openai-bundled/visualize/1.0.38/skills/visualize/SKILL.md)

## 設定の根拠ファイル

- [導入前config.toml](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/config.toml)
- [導入前AGENTS.md](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/AGENTS.md)
- [導入前default.rules](C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os/snapshot/.codex/rules/default.rules)
