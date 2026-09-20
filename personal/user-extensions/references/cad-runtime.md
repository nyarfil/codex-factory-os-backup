# CAD実行環境

- 新規のcadgen 0.6.5案件：`C:/Users/nikis/.codex/user-runtimes/cadgen-0.6.5/Scripts/python.exe` を使用。`python -m cadgen.cli`でCLIを呼べる。
- この環境は0.6.5のインストール済みcadプラグインと一致。doctorとpip checkを実行済み。
- `V:/mouse/.venv-text-to-cad` は既存案件のcadgen 0.5.1であり変更していない。既存案件ではプロジェクトの固定環境と正本を先に確認する。新しいスキルの例を古い環境へ無条件で流用しない。
- 旧案件の再現に必要な過去スキルは導入前バックアップにある。旧版を自動検出先へ再配置せず、必要時だけ参照する。移行は別作業として扱う。
- ForgeCAD：`C:/Users/nikis/AppData/Roaming/npm/forgecad.cmd`。0.13.0の起動確認済み。PowerShell署名制限がある環境では既存のcmdエントリポイントを使う。
- Fusion：`http://127.0.0.1:27182/mcp`。接続初期化応答を確認済み。各作業開始時に文書・未保存状態・ツールの利用可否を再確認する。
