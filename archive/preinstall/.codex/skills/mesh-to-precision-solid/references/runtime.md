# 実行環境

ZA13で検証したWindows環境:

- Python: `V:/mouse/.venv-text-to-cad/Scripts/python.exe`
- CLI: `V:/mouse/.venv-text-to-cad/Scripts/cadgen.exe`、cadgen 0.5.0
- PowerShell: `$env:CADGEN_CACHE_DIR='V:\mouse\outputs\.cadgen-cache'`
- 日本語のSkill/JSONを扱うWindows Pythonは `$env:PYTHONUTF8='1'` または `python -X utf8` を使用する。既定cp932のままUTF-8のSkillを読むと検証ツールが文字コードエラーになる。
- CAD側は `from cadgen import build123d as bd`。グローバルPythonへ依存を追加しない。
- native skill: `C:/Users/nikis/.codex/plugins/cache/text-to-cad/cad/0.5.0/skills/`。バージョン更新後は実際のインストール先とdoctor/pip checkを確認する。
- `runtime_versions.json` にSkill保存時のインストール済みバージョンを記録。固定環境でのビット一致を万能に保証するものではない。

他PC/他プロジェクトでは上記ドライブを前提にせず、プロジェクトのruntimeを探す。再現ソースは歴史的ケースであり、upstream skillの代用品にはしない。

設定変更なしの静的なSkill選択であり、常駐タスクや時刻スケジュールは作らない。`agents/openai.yaml` の `allow_implicit_invocation: true` とSkillのdescriptionで自動選択を許可する。`V:/mouse/AGENTS.md` とCursorのCAD ruleにも参照を設定する。既に始まっているタスクのSkill一覧へ即時追加されるかはクライアント次第なので、新しいタスクで確認する。
