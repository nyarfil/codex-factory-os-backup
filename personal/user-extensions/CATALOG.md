# Factory OS下位の個人能力カタログ

本書は追加能力の索引。Factory OS標準の担当Factoryが必要な行だけ使う。プラグインのSKILLは現在のスキル一覧から読み、ここに複製しない。旧オーケストレーターは復元していない。

CADの作成・変更・評価では [旧CAD専門要件の引継ぎ](references/cad-handoff.md) を読み、必要な検証を取りこぼさない。

| 担当Factory | 用途 | 能力・参照先 | 条件 |
|---|---|---|---|
| factory-software | 設計・GitHub | [ソフト開発補助](references/software.md)、GitHubプラグイン | 既存アーキテクチャを優先 |
| factory-cad-3dp | cadMCPの型付きCAD生成・原理参考・証拠管理 | [cadMCP暫定利用](references/cadmcp.md) | Stella_CAD_SYSTEMで有効。Factoryが統括。本体開発はfactory-software |
| factory-cad-3dp | パラメトリックCAD、表示、造形性、スライス、DXF、市販部品 | cadプラグインの cad / cad-viewer / dfam-check / gcode / dxf / step-parts | 一度に必要なスキルだけ読み込む |
| factory-cad-3dp | Fusion文書・履歴の検査と編集 | MCP `fusion`、[Fusion手順](references/fusion.md) | Fusion起動・MCP有効化が必要。初回は文書状態を読み取り確認 |
| factory-cad-3dp | 既存ForgeCAD・明示指定 | [ForgeCAD](capabilities/forgecad/GUIDE.md)、[制作手順](capabilities/forgecad-build-model/GUIDE.md) | CLIはforgecad.cmd。API資料参照先を移設済み |
| factory-cad-3dp | 既存ファイルの再構築 | [CADファイルから再構築](capabilities/forgecad-reconstruct-cad-file/GUIDE.md) | 再構築が目的の場合。単なる部品挿入では使わない |
| factory-cad-3dp | 画像から再構築 | [画像から再構築](capabilities/forgecad-reconstruct-from-images/GUIDE.md) | 図示されていない寸法を測定済みと扱わない |
| factory-cad-3dp | メッシュ修復・軽量化 | [メッシュ修復](capabilities/mesh-to-precision-solid/GUIDE.md) | 同梱ZA13事例は参考。別案件へ座標・許可を流用しない |
| factory-cad-3dp | ロボット、Bambu、外注加工 | cadプラグインの urdf / srdf / sdf / bambu-labs / sendcutsend | 該当用途・対象機器が指定されたときだけ |
| factory-document | Word・PDF・スライド | documents / pdf / presentations | 個別形式の生成・表示検証手順として利用 |
| factory-data | 表計算・数値分析 | spreadsheets / Excel live control | Factoryの分析・検証方針の下で利用 |
| factory-document | 再利用テンプレート | template-creator | テンプレート化を依頼されたとき |
| 各Factory | UI確認・ブラウザー操作 | browser / chrome / unified-computer-use / computer-use | 用途に合うAPIがあれば優先。各ツールの利用可能範囲に従う |
| 各Factory | 図解・対話表示 | visualize | 説明や比較に必要な場合 |
| factory-general | Codexタスク・プロジェクト操作 | codex-app-tools | タスク作成・メッセージ等は個別の指示範囲内で使用 |

[CADの実行環境と旧案件の版分離](references/cad-runtime.md) をCAD実行前に確認する。

[Serenaのプロジェクト自動検出・確認手順](references/serena.md) をコード構造の調査・シンボル編集で利用する。

## 必要時参照・除外

- [必要時参照の追加能力](OPTIONAL.md)：AI-CAD、AgentCAD、OpenSCAD、NVIDIA、Hugging Face、ForgeCAD同期・画像プロンプト、Data Analytics。資料は配置済み。担当Factoryが必要と判断した項目だけ読む。
- 除外：旧mechanical-cad-orchestrator、company-director、単独CADスキルの重複、ForgeCADの二重配置、Serenaの旧JCK固定設定、旧GitHub MCP、旧npm build許可。
- Data Analyticsの専門手法も必要時参照できる。担当・モデル・委譲・完了判断はfactory-dataが持つ。
- 標準搭載のTemplates・Sites・Plugin Managementはサービス管理。存在をFactoryの代替統括役と解釈しない。SitesはWeb公開の依頼時だけ利用する。
