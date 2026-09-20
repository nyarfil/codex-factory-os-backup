# Fusion MCP運用

ユーザー拡張のMCP登録 `fusion` が `http://127.0.0.1:27182/mcp` をHTTP MCPとして提供する。Fusion起動中かつ Preferences > General > API のFusion MCP Serverが有効な間だけ利用可能。新しいPlugin/ツールの認識は新規Codexセッションで確認する。

1. まず `fusion_mcp_read` のdocument/openで現在の開いている文書と未保存状態を把握する。このoperationは開く操作ではなく一覧取得。activeCommandも調べ、ダイアログを勝手に確定/取消しない。
2. 実際のtools/listと `fusion_mcp_read` apiDocumentationで現在のAPIを確認する。Pythonスクリプトは `def run(_context: str)` を定義し、読み取り専用なら `fusion_mcp_execute` scriptの `readOnly: true` を設定する。例外を握りつぶさない。
3. Text-to-CAD正本のSTEPは `ImportManager.createSTEPImportOptions` → `importToNewDocument` で**新しいテスト文書**に取り込む。ユーザーのアクティブ文書へ追加しない。開始前の文書を保持し、検証後再アクティブ化する。元文書の保存・閉鎖・undoをしない。
4. Fusionの長さは内部cm、体積cm³。比較時はそれぞれ10倍、1000倍してmm/mm³へ換算する。BRepBody preciseBoundingBox、isSolid、physicalProperties、円筒面radius/axis、MeasureManager.measureMinimumDistanceなどを使う。APIのisValidは参照の有効性であり完全な幾何健全性証明ではない。
5. occurrenceの変換とroot座標を揃える。minimum distance=0だけでは接触と体積干渉を区別できない。干渉解析/共通体積と組み合わせる。静止一姿勢の距離だけで挿入可能性や可動全域を保証しない。
6. screenshot/currentで画像を取得し自分で確認する。検証用文書を残した場合は名称を報告する。破棄は自分が作成した変更のないテスト文書だけを厳密に同定し、既存データは閉じない。

Fusion未起動ならその事実と未実施項目を明記する。非criticalの補助検証ならText-to-CADで継続可能。Fusion必須の設計やcriticalな不確実性が残るなら完成とはしない。

公式: https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_FusionDesktopMcp_connecting_to_the_fusion_mcp_server_html
