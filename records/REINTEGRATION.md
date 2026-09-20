# Factory OSを中心とした再編結果

## 構成

Factory OS → 担当Factory → user-capabilitiesの能力索引 → 必要な専門スキル・CLI・MCP。

Factory標準6スキル、31エージェント、hooks、版別runtimeは変更しない。AGENTS.mdも既存管理ブロックは完全維持し、その外に個人設定を読む短い独立ブロックだけ追加。

## 採用・保留・除外

| 判断 | 対象 | 意図 |
|---|---|---|
| 採用 | CADプラグイン、Fusion MCP | CAD担当Factoryの実行機能。旧CAD統括役は入れない |
| 採用 | documents、spreadsheets、presentations、pdf、template-creator | 各Factoryから必要な形式の実行手順だけ使用 |
| 採用 | GitHub現行版 | ソフト開発の連携。旧GitHub MCPと二重化しない |
| 採用 | browser、chrome、computer-use、unified-computer-use、codex-app-tools、visualize | UI検証、アプリ操作、図解。使用条件は各機能の規則に従う |
| 必要時参照 | HDVS、ForgeCAD基本・制作・ファイル再構築・画像再構築、メッシュ修復 | グローバルな自動スキルを増やさず、単一入口から読む |
| 保留 | AI-CAD、AgentCAD、OpenSCAD、NVIDIA、Hugging Face、ForgeCAD同期・画像プロンプト | 対象案件と依存が明確になった時に追加 |
| 保留 | data-analytics | factory-dataとspreadsheetsを基本にし、分析フローの重複を避ける |
| 除外 | mechanical-cad-orchestrator、company-director、重複配置、JCK固定Serena、旧npm build許可 | 別統括役、重複、固定接続、不要な許可を復元しない |

CAD同梱のロボット・Bambu・外注加工スキルは該当用途のときだけ使用する。標準搭載Templates・Sites・Plugin Managementはサービス管理のまま。

## 個人ルール

日本語・結論優先・コードを読まない利用者向けの操作説明・比較表を個人設定に復元。HDVSを毎回読む指示や旧CAD自動ルーターは復元しない。既存アーキテクチャ・CAD正本を維持し、Factory OSのモデル・委譲・検証方針に従う。

## 物理的な分離

- [入口スキル](C:/Users/nikis/.codex/skills/user-capabilities/SKILL.md)
- [能力カタログ](C:/Users/nikis/.codex/user-extensions/CATALOG.md)
- [個人ルール](C:/Users/nikis/.codex/user-extensions/PREFERENCES.md)
- [所有ファイル一覧](C:/Users/nikis/.codex/user-extensions/manifest.json)
- [拡張の取り外し・復元](C:/Users/nikis/.codex/user-extensions/RESTORE.md)
- 再編前バックアップ：`E:/aiwork/codex-factory-os-v1.1.0/.installation/before-extension-20260920-094446`

## 検証

- Factory管理対象191ファイルと標準管理ブロック：無変更。
- Factoryモデル・エージェント設定：無変更。
- Codex新規プロセスのstrict-config起動・skills/list：34スキル検出、エラー0、名前重複0。追加入口は1個。
- 選定プラグイン13件：実際の一覧で有効を確認。
- 個人入口のskill-creator検証：成功。参照リンク切れ0。
- Factory Doctor：正常、Governor指摘0。
- Fusion：初期化応答HTTP 200。実モデルの編集はしていない。
- ForgeCAD：既存0.13.0起動確認。
- cadgen：旧V:/mouseの0.5.1を変更せず、独立0.6.5環境を導入。doctor・依存整合性チェック成功。
- CAD実動作：10×20×30mmの検証形状でSTEP保存→再読込、1 solid・体積6000mm³を確認。
- 表示基盤：Playwright Chromiumの起動確認。
- 読み取りレビュー：Fusion F3D、Next.js小修正、ForgeCAD案件で適切な担当・正本・資料を選択。

## 反映と限界

Codex再起動・新しいタスクで利用する。Factoryフックの信頼確認が未実施なら `/hooks` で確認する。モデルを実際に起動する委譲テスト、全専門機能の実制作、外部サービスへの書込みは行っていない。

codex-app-toolsは使用中キャッシュの再コピーがアクセス拒否だったため、既存版を保持して有効化。正式一覧で有効を確認済み。その他の選定プラグインはCLIで再導入した。

## 追加更新：必要時参照とSerena

上記の保留判断を更新。8系統47件を必要時参照として配置済み。外部プラグインや実行環境を一括起動・再接続してはいない。Serenaは固定projectを指定せず、cwdから自動検出して使うMCPとして有効化。2つの独立検証プロジェクトで自動選択とシンボル取得、同一接続で絶対パスによる対象切替を確認済み。標準191ファイルは無変更。

- [必要時参照の索引](C:/Users/nikis/.codex/user-extensions/OPTIONAL.md)
- [Serena運用](C:/Users/nikis/.codex/user-extensions/references/serena.md)
- [旧統括役の説明](OLD-ORCHESTRATORS.md)
