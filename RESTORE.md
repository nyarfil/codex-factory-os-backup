# 復元手順（Windows）

## 1. 取得・照合

Windowsの長いパスに対応させてクローンし、Python 3.11以上の環境でリポジトリ直下から実行する。

```powershell
git -c core.longpaths=true clone https://github.com/nyarfil/codex-factory-os-backup.git
cd codex-factory-os-backup
```

```powershell
$env:PYTHONUTF8='1'
python restore.py
```

全ファイルのSHA-256を照合する。復元スクリプトは既存の設定を勝手に初期化しない。

## 2. 新しい環境へ復元

Codexを終了し、必要な既存設定を退避した新しい環境で次を実行する。

```powershell
python restore.py --apply
```

既存設定があれば停止する。検証用の別フォルダーへ復元する場合は`--home C:\任意の検証先 --apply`を使う。Factory OS標準、個人拡張、可搬設定、独立した個人ルール参照を復元する。ユーザープロファイルの変更に合わせて個人拡張内の参照パスを置換する。

## 3. ランタイム・プラグイン

- Codex、GitHub CLI、uvは公式手順で導入してログインする。
- Codexのプラグイン画面からCAD、GitHub、文書・表計算・スライド・PDF、テンプレート作成、画面操作・可視化を導入する。採用対象はpersonal/user-extensions/manifest.jsonのconfig_ownership.plugins_enabledに記録。
- アプリ管理のマーケットプレイス・node_replなどは新しいCodex環境のものを利用する。古い実行パスやパイプ接続をコピーしない。
- Fusion MCPはFusionを起動して有効化する。設定はlocalhost:27182。Serenaはuvx経由で記録済みコミットから起動する。
- 新規CAD用の独立環境を作る。既存プロジェクトのPython環境は上書きしない。

```powershell
uv venv "$env:USERPROFILE\.codex\user-runtimes\cadgen-0.6.5"
uv pip install --python "$env:USERPROFILE\.codex\user-runtimes\cadgen-0.6.5\Scripts\python.exe" -r records/cad-runtime-requirements.txt
& "$env:USERPROFILE\.codex\user-runtimes\cadgen-0.6.5\Scripts\python.exe" -m playwright install chromium
```

ForgeCADは0.13.0を使用していた。インストール後にCLIの実パスを確認する。AI-CADやAgentCAD等の個別プロジェクト環境はこのバックアップの対象外で、必要時に接続先と依存関係を確認する。

## 4. 検証

Codexを再起動し、`/hooks`でFactory OSのフックを確認・信頼する。`factory-os/doctor.ps1`で診断する。署名制約でラッパーを実行できない場合は`factory-os/06-lifecycle`へ移動し、`python -m factory_lifecycle.cli doctor`を実行する。個人拡張カタログ・MCP接続は新環境でも確認する。

archiveは当時の資料保存用。現行構成と重複するスキルや旧統括役を含むため、通常のスキル配置先へ丸ごとコピーしない。
