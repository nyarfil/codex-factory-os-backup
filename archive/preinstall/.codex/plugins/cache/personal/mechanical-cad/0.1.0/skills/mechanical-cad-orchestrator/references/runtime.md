# このPCのruntime

- 公式native Plugin: `cad@text-to-cad`。現在インストールされたPluginのSkillパスを優先して読む。ユーザー/プロジェクトの `.agents/skills` にSkills CLI版も残っているため、更新時はpinの一致を確認し混在実行を避ける。
- 2026-09-06検証済みPython: `V:\mouse\.venv-text-to-cad\Scripts\python.exe`。cadgen: 同じScriptsフォルダの `cadgen.exe`。グローバルSkillからも使用可能だがVドライブに依存する。
- `cadgen doctor --skill-dir <実際のcad Skill>` と `python -m pip check` を起動確認に使う。0.5.0では古いscripts/gen等ではなく、モデルPython実行、`cadgen step inspect`、`cadgen snapshot` 等を使う。各コマンドの `--help` で現在の構文を調べる。
- この環境が失われた場合、インストール済みcad Skillのpinに従い専用venvを再作成する。別用途のグローバルPythonを大量依存で汚さない。
- 正本例と検証成果物: `V:\mouse\text-to-cad-e2e`。これはサンプルであり、毎回の作業出力先ではない。
