---
name: mechanical-cad-orchestrator
description: Design, modify, and evaluate physical mechanical parts and assemblies using Text-to-CAD, Fusion MCP and DfAM. Use implicitly for CAD/3D CAD, STEP/STP, STL/3MF, Fusion 360, build123d, 機械設計, 部品設計, PCB cases/enclosures, brackets, mounts, holders, jigs/fixtures, chassis, screw bosses, ribs, hinges, physical buttons/switch mechanisms, gaming mouse shells/internals, dimensioned or moving objects and 3Dプリント部品, even without CAD keywords. Do not use for software UI buttons, programming classes/cases, or purely illustrative 3D art; resolve ambiguous physical versus UI context first.
---

# Mechanical CAD orchestrator

日本語で、要求を設計・検証可能な機能要件に変換する。これは上流Text-to-CADの代替実装ではなく統括層。インストール済みの該当upstream Skillを読み、そのruntime/APIを正本とする。upstreamファイルは改造しない。

## 正本とツール選択

開始時に `SOURCE OF TRUTH: TEXT-TO-CAD` と宣言。パラメトリックPython/build123dを編集し、STEP-firstで生成する。Fusionのインポート結果は検証用派生物であり、そこで形状修正して分岐させない。

明示的Fusion指定、既存Fusion project/F3D、保持すべきtimeline/features、Fusion native機能が明らかに適切、または変換で重要情報を失う場合は、理由とともに `SOURCE OF TRUTH: FUSION` に切り替える。F3Dを正本、STEP/STLを派生物にする。正本変更は明記し、異なる正本を同時編集しない。

- 通常の生成・BRep検査: `cad`。視覚レビュー: `cad-viewer`。市販部品は `step-parts` で実物CADを探してから、必要なら明示した近似を使う。
- 3Dプリント品は `dfam-check`。材料/プリンタ/ノズル/向きの指定を優先。未指定なら一般的FDMを暫定条件として明記し、プリンタ固有の保証をしない。
- 複数部品、PCBとshell、可動部、ねじ、重要clearance、複雑な形状、独立検証の価値が高い場合は、利用可能なFusion MCPを自発的に使う。単純スペーサーに無意味な全ツール実行は不要。
- Fusion利用時は [references/fusion.md](references/fusion.md) を読む。ローカルruntime利用時は [references/runtime.md](references/runtime.md) を読む。
- ユーザーが評価だけを求めたら読み取り中心。Skill選択は既存文書変更・クラウド保存・印刷開始の包括的許可ではない。

## 設計 → 検証 → 修正

1. 入力CAD/PCB/寸法/画像を調べ、用途・固定・荷重・可動・製造・組立の要求を整理する。実寸がない画像から精密寸法を確定しない。
2. 合理的なengineering assumptionsを記録し、datum、座標系、単位、部品構成、重要寸法と許容差を決める。安全・適合・不可逆な設計判断だけ確認し、小さな設計判断は提案・採用して進める。
3. 正本をパラメトリックに作成/変更し、派生ファイルを分離して生成する。既存の入力や未保存Fusion文書を保護する。
4. [references/verification.md](references/verification.md) の該当項目を実測する。適用外と未検証を分け、各項目に根拠と閾値を残す。STEP inspectと生成後snapshotを含め、画像を自分で見る。
5. Fusionで同じcritical propertyを測定する際は座標系、単位、許容差を揃える。不一致は平均化して隠さず原因調査する。
6. NGの原因が設計なら正本を修正し、再生成して関連検証を再実行する。環境エラーと幾何エラーは区別する。安全な範囲で修復し、同じ失敗を根拠なく反復しない。必要な新権限/入力なしでは進めない場合は具体的に報告する。
7. 最後に正本、出力、採用仮定、PASS/FAIL/未検証/適用外、残るリスクを示す。重大な干渉・clearance不足・invalid geometry・組立/動作/製造不能が残れば完成扱いしない。critical項目の未検証も合格ではない。

## 拡張

将来mouse-design等の特化Skillを追加する場合、機種固有寸法と操作感の知識だけを委譲する。本Skillの単一正本・検証根拠・既存データ保護を維持する。
