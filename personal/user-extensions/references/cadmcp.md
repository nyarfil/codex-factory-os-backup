# cadMCP — Factory OSの下位CAD能力

所有者のMCP優先指示によるローカル暫定利用。Factoryのモデル・予算・委譲・完了判断を置換しない。

- プロジェクト: `E:/aiwork/Stella_CAD_SYSTEM`
- 本体: `E:/aiwork/Stella_CAD_SYSTEM/cadmcp-all-in-one-2026-09-17/01_CURRENT`
- 共通workspace: `E:/aiwork/Stella_CAD_SYSTEM/cadmcp-workspace`
- MCP名: `cadmcp-design-brain`。Codexプロジェクト設定で有効。グローバル登録ではない。
- 製品Skill: `E:/aiwork/Stella_CAD_SYSTEM/.agents/skills/cadmcp-design-brain/SKILL.md`
- 最新手順・制限・証拠: `E:/aiwork/Stella_CAD_SYSTEM/docs/MCP_PREVIEW_JA.md`

物理CADはfactory-cad-3dp、本体開発はfactory-softwareが担当。本体開発では製品Skillを適用しない。
CAD利用時は実工具を検出し、brain_doctor / brain_fs_status / brain_projects / brain_studio_schema(name="FunctionBrief")で確認。見えなければ上記プロジェクトで設定を再読込し、接続済みと推定しない。別backendへ無断切替しない。
製品CADの設計時だけSkillと必須参照を読み、brain_studio_capabilitiesで対応操作を確認する。
参考は原理参考・適合・直接流用を区別。既存正本・元要求・保護形状・検査閾値を保持する。
cadMCPは実行と証拠管理を担当し、Factoryと二重の統括役を作らない。別CLIモデル試験や自動5役試験を無断起動しない。
CAD生成・幾何合格・レビュー実行・レビュー受入・物理性能を別判定する。マウス完成・強度・操作感は未証明。
ZA13正本・未保存Fusion・承認済み配置・プリンタへ明示許可なしで反映しない。
この登録は能力発見の接続点であり、全プロジェクトの自動接続やFactory経由の実CAD完遂の証明ではない。
