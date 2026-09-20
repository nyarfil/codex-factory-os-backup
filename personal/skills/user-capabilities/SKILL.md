---
name: user-capabilities
description: Factory OSの担当Factoryから、復元済みの個人用CAD・設計資料・制作プラグインを選ぶための能力カタログ。専門ツール選択や旧資産の利用が必要なときに参照する。
---

# 個人用の下位能力

Factory OSで担当Factoryが決まった後、必要な能力だけを選ぶ。ここでは独自のモデル選択・委譲・予算・完了判定を定義しない。

[C:/Users/nikis/.codex/user-extensions/CATALOG.md](C:/Users/nikis/.codex/user-extensions/CATALOG.md) に用途・読込先・利用条件を記載している。該当する行の資料だけ読む。

- CADは既存正本・指定ツールを維持する。Fusion履歴、ForgeCAD、cadgen間を自動で乗り換えない。
- 一覧掲載は接続成功の証明ではない。MCPは実際のツール検出、CLIは対象環境の起動結果を確認して使う。
- 必要時参照の資料も配置済み。担当Factoryが用途に合うものだけ読む。資料の存在と外部接続・ランタイムの利用可能性を区別し、実行前に確認する。
