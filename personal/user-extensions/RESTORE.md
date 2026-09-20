# 個人拡張の管理・復元

所有範囲はmanifest.jsonに記録。Factory OSのruntime、6スキル、31エージェント、hooksは本拡張の対象外。

再編前バックアップ：`E:/aiwork/codex-factory-os-v1.1.0/.installation/before-extension-20260920-094446`
初回初期化前バックアップ：`C:/Users/nikis/codex-customization-backups/20260920-092704-before-factory-os`

拡張を取り外す場合は、Codex終了後、現在の設定を別途保存してから次を行う。

1. グローバルAGENTS.mdのUSER_CAPABILITIES:BEGINからENDまでだけを除去。CODEX_FACTORY_OSブロックを保持。
2. `.codex/skills/user-capabilities`と`.codex/user-extensions`を探索対象外へ退避。
3. 今回追加したfusion MCPと有効化したプラグイン設定を再編前config.tomlとの差分で戻す。後から追加した他の設定を一括上書きしない。
4. GitHubはリモート登録のため、不要ならCodexプラグイン画面で個別にアンインストールする。
5. `.codex/user-runtimes/cadgen-0.6.5`は今回の独立環境。使用中案件がなければ退避できる。既存のV:/mouse/.venv-text-to-cadは触らない。

キャッシュやインストール済みChromiumは他の機能でも利用される可能性があるため、設定解除と同時に一括削除しない。

更新は個人拡張側だけを行い、Factory標準は公式更新手順で別に更新する。公式更新後は新しい標準ファイルを基準として再照合する。

## 必要時参照・Serenaの追加

追加前バックアップ：`E:/aiwork/codex-factory-os-v1.1.0/.installation/before-optional-serena-20260920-100010`。今回の追加対象はoptional配下の資料、索引、Serena運用手順、config.tomlのmcp_servers.serena。取り外す際はこの登録と参照を個別に戻す。Factory標準は変更していない。
