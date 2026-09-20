# 検証と完了ゲート

タスクごとに適用項目、合格基準、実測値、手法、artifactを記録。未実施をPASSにしない。

| 項目 | 必要な証拠と注意 |
|---|---|
| Geometry | BRep validity、期待solid数、open shell、異常topology、正の体積。Python実行成功やFusion isValidだけで代用しない |
| Dimension | bboxに加え重要面間距離、穴径/数/中心/貫通長、datumを検査。bboxでは内部寸法を証明できない |
| Interference | 対象部品ペアの共通体積または干渉解析。意図した圧入/接触は仕様として区別 |
| Clearance | ペアごとに最小距離と要求値を比較。製造公差・収縮・組付けばらつきを含める |
| Assembly | 挿入方向と掃引経路、組立順序、captive geometry、ねじ/工具アクセスを確認。完成姿勢だけで判定しない |
| Motion | travel/回転範囲、スイッチ作動、motion envelopeと衝突。サンプル姿勢検査は連続的な非干渉保証とは区別 |
| Structure | 最小肉厚、薄い突起、boss/rib、応力集中。寸法検査は強度証明ではない。荷重/材料と解析または実機試験が必要な場合は未検証とする |
| DfAM | 工法別の肉厚、向き、overhang、support。穴/bridge/閉じ込めsupportの対応範囲を確認し、非対応項目は別測定/スライサーで検証。レイサンプルは完全な最小肉厚保証ではない |
| Visual | 最新STEPのsnapshotと必要時Fusion viewportを実際に見る。画像だけで隠れた干渉や寸法を合格にしない |

Cross-validationは同じ正本由来ファイルのSHA-256、単位、座標、閾値を揃えて比較する。mm精度を謳うならbboxの見かけ丸め値でなく実測値を用いる。テストplateの数値比較には0.001mmを用いるが、実部品の製造clearanceとして流用しない。

失敗時は正本を修正→再生成→関連検証全てを再実行し、旧artifactと新artifactを混同しない。主要FAILやcritical未検証が残る場合は設計候補と呼び、完成品としない。
