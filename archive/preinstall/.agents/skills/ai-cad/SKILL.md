---
name: ai-cad
description: >-
  Run the ai-cad-labs AI-CAD harness (CadQuery, DFM/DFA gates, 8-view renders,
  multi-agent design runs). Use when the user picks AI-CAD / aicad / ai-cad-labs,
  or cad-session.json tool is ai-cad. Do not use for ZA13 mouse work, cadgen,
  build123d, ForgeCAD, OpenSCAD, or AgentCAD sessions.
---

# AI-CAD（ai-cad-labs）

Cursor から選ぶ CAD 工具のひとつ。正本は `E:\aiwork\Stella_CAD_SYSTEM\ai-cad-labs`。
マウスの `V:\mouse\vendor\ai-cad` は使わない。
この Skill は入口だけ。CadQuery cookbook 一式は `.cursor/skills` に置かない。

## 使うとき

- ユーザーが AI-CAD / aicad / ai-cad-labs を指定した
- `.cursor/cad-session.json` の `tool` が `ai-cad`

既存マウス（ZA13 など）の正本作業では使わない。

## 使わないもの

- `V:\mouse\.venv-text-to-cad` と `cadgen`
- ForgeCAD / OpenSCAD MCP / AgentCAD HTTP
- mcp.json の編集

## 手順（エージェントが自分でやる）

1. `.cursor/cad-session.json` に `status=in_progress`、`tool=ai-cad`、部品名を書く。
2. すぐ実行する:

```powershell
powershell -File V:\mouse\.cursor\cad-boot.ps1 prepare ai-cad
```

3. 作業ディレクトリを `E:\aiwork\Stella_CAD_SYSTEM\ai-cad-labs` にする。その `AGENTS.md` を読む。
4. Python は `ai-cad-labs\.venv\Scripts\python.exe`、または `uv --directory ai-cad-labs run python -m tools.<name>`。
5. 成果は `E:\aiwork\Stella_CAD_SYSTEM\ai-cad-labs\projects\<name>/` だけ。
6. ダッシュボード（5199）はユーザーが求めたときだけ。完成時は `cad-boot.ps1 complete`。
