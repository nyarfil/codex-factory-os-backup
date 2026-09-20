> 個人拡張の必要時参照用資料。担当Factoryの下で使い、旧資料のモデル選択・統括・固定出力先より、現在の依頼とプロジェクト設定を優先する。未検証の接続・CLIを利用可能と仮定しない。

# Stella_Agentcad（マウスの AgentCAD 択）

MCP サーバ名は **`Stella_Agentcad`**（`.cursor/mcp.json`）。本家 `vendor\agentcad` は起動しない。

旧環境の部品置場は `E:/aiwork/Stella_CAD_SYSTEM/projects`。現在の依頼ではプロジェクトの正本・出力先を確認し、このパスへ自動で切り替えない。`vendor/agentcad-projects` は生成先にしない。

1. `part_template` のあと、必要なら `load_skill`
2. `create_project` / `create_part` / `update_part_script`
3. 失敗 JSON の `type` / `line` / `hint` を読んで直す
4. `export_part` `format: "step"`

MCP が無いときだけ Stella リポで `uv run python -m stella_cad.bridge health`。
ヘルスがタイムアウトしても、8630 のコマンドラインが Stella の `agentcad serve` なら busy であり未知プロセスではない。第二サーバは立てない。
