# ZA13：実測済みケースと再生成

記録日2026-09-06。寸法はmm。以下はこのケースの実績であり、全てのメッシュで達成可能という保証ではない。

## 実績

| 段階 | 結果 | 範囲・注意 |
|---|---|---|
| 精密修復03 | 163有効閉ソリッド、360316面、自己交差0 | ファセットBRepであり重いまま |
| 上面軽量化01 | 66854→15549面、約175.7→46.5 MB | 代表部品単体。全アセンブリは軽量化していない |
| 表面差 | 元→軽量版最大0.008767 mm、逆0.007958 mm | 200564/1577503サンプル、deflection 0.001 mm、連続最大保証ではない |
| 上面ロゴ除去01 | 13823面、約41.7 MB、1有効閉ソリッド | 内面と保持13822面一致、外接箱一致、SI異常なし |

全体修復時はUSB清掃部分に最大0.150162/0.035829 mm、内部固定部品の追加壁から元面まで0.584577 mmの局所差がある。外形維持の数値に混ぜない。その他表面は元→修復最大0.004714 mm。承認されたゴミ7個24面を削除した。

上面軽量化時のsharp-edge頂点2954点中22点が移動、最大0.004879 mm。全境界点が厳密不変だったとは説明しない。Fusionの一組の測定では読み込み33.43→16.31秒、コピー0.460→0.082秒、一時円筒カット0.031→0.089秒。全演算の高速化を主張しない。

## 保存ソースの順序

`za13-sources/` は依存先を含むPythonソースの保存版。ハッシュは `replay_manifest.json`。スクリプト名にtrialとあるものにも成功段階が含まれるが、ファイル名だけで合格判定しない。

精密修復:

1. `official_solid_full_diagnose.py`：元STEPをハッシュ固定、読込キャッシュ、縫合診断。
2. `official_solid_patch_loops.py`：開口の意味を区別した局所パッチ。`official_solid_exact_boundary_trial.py`：共有境界を通る面の再構築。上面66853、底面29246、内部固定908はこのケースの識別面数。
3. `official_solid_regularize.py`：材料セル判定。`official_solid_contacts_regularize.py`：元部品160/161。側面は101603の再構築→regularize→`official_solid_side_second_pass.py`。USBは13058の再構築→regularize→`official_solid_union_cells.py`→`official_solid_usb_second_pass.py`。
4. `official_solid_prepare_precision_manifest.py`：7修復チェックポイントの合否/ハッシュ固定。
5. `official_solid_precision_package.py`：元の正常部品と検証済み7部品を組み立てて03版へ出力。
6. 保存STEP再読込、全部品SI、表面差、画像、Fusionを検証。

`ZA13_OFFICIAL_PRECISION_REPAIR_02/ZA13_DW_OFFICIAL_repaired.step` は**不合格の旧候補**。その生成スクリプトは途中のパッチ記録用に保存される場合があるが、完成モデルの入力にしない。許容差だけの閉鎖を合格とする旧assertを、新案件の採用条件にしない。

軽量化:

1. `official_upper_rebuild_diagnose.py`：修復済み上面から向き付き参照メッシュを抽出。
2. `official_upper_feature_regions.py` と各fit probe：領域分割と近似の可否を調査。
3. `official_upper_hybrid_rebuild.py`：2曲面と細部/遷移面を作り縫合。
4. `official_upper_hybrid_export.py`：軽量版と比較用上面STEP。
5. `official_upper_hybrid_validate.py` / `official_upper_feature_preservation.py` / `official_upper_section_compare.py`：表面差・境界・断面。
6. `official_upper_no_logo.py`：同じ再構築正本でロゴだけ除去。`official_upper_no_logo_validate.py`：面一致と独立再読込検査。

## 隔離再生の例

```powershell
$py='V:\mouse\.venv-text-to-cad\Scripts\python.exe'
$env:PYTHONUTF8='1'
& $py '<skill-dir>\scripts\prepare_za13_replay.py' --mode upper-no-logo --dest 'V:\mouse\outputs\ZA13_REPLAY_NEW'
$env:CADGEN_CACHE_DIR='V:\mouse\outputs\ZA13_REPLAY_NEW\outputs\.cadgen-cache'
Set-Location 'V:\mouse\outputs\ZA13_REPLAY_NEW'
& $py scripts/official_upper_no_logo.py
& $py scripts/official_upper_no_logo_validate.py
```

末尾validateは参照として前のロゴ付き候補BREP/曲面を使用する。入力は元の `V:/mouse` に必要で、消失/変更した場合は準備段階で停止する。固有パスを書き換えたソースは派生した隔離レシピで、元の完成品やスクリプトを編集しない。

`precision-assembly` は原本から全修復を再探索する処理ではなく、ハッシュ検証済み7チェックポイントからの最終組立再生成。原本からの修復過程は上記の段階別ソースと診断を用い、各出力を都度再検証する。新しい入力で面番号を盲目的に使わない。

大きい入力ファイルはSkillに複製しない。`replay_manifest.json` に外部ファイルの相対パスとSHA-256を保存する。ポータブルに保管したい場合はその一覧の原本/チェックポイントも一緒に保管する。

## Skill保存時の再現試験

保存した23スクリプトと6入力を隔離フォルダへ展開して、ロゴなし上面を実際に再生成。BREPとSTEPの両方が前回完成品とSHA-256一致した。STEP SHA-256は `dc96cbe46fa7c12fa0834b96fbebf1f7d0acad0f399d185be85550783f70861f`。再読み込みで1solid/13823面/外接箱一致、画像も確認。精密組立とロゴ付き軽量版は準備・入力ハッシュ照合まで検証し、このSkill保存作業では大規模な再生成を重複実行していない。

汎用auditツールは閉じた箱を合格、開いた面および期待部品数不一致を不合格とする実行試験に合格。これは未知メッシュを自動で修復できることや、将来の全タスクでの選択を実証した試験ではない。
