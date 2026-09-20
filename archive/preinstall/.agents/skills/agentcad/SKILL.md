---
name: agentcad
description: >-
  Mouse CAD choice 5: Stella_Agentcad MCP. Do not run n3r/AgentCAD at
  vendor\agentcad. Do not use during text-to-cad, ForgeCAD, OpenSCAD, or
  AI-CAD sessions.
---

# Stella_Agentcad（マウスの AgentCAD 択）

MCP サーバ名は **`Stella_Agentcad`**（`.cursor/mcp.json`）。本家 `vendor\agentcad` は起動しない。

部品は `E:\aiwork\Stella_CAD_SYSTEM\projects`。`vendor\agentcad-projects` には書かない。

1. `part_template` のあと、必要なら `load_skill`
2. `create_project` / `create_part` / `update_part_script`
3. 失敗 JSON の `type` / `line` / `hint` を読んで直す
4. `export_part` `format: "step"`

MCP が無いときだけ Stella リポで `uv run python -m stella_cad.bridge health`。
ヘルスがタイムアウトしても、8630 のコマンドラインが Stella の `agentcad serve` なら busy であり未知プロセスではない。第二サーバは立てない。
