# Codex Factory OS v1.1.0

Codex専用の常駐オーケストレーション／モデルルーティング／環境ガバナンス基盤です。Cursorには依存しません。

目的は、ユーザーが毎回モデルやサブエージェントを選ばなくても、Codexがタスクの種類・難易度・不確実性・失敗履歴・検証可能性・コストを見て、適切なFactoryと専門Agentへ仕事を振り分ける状態を作ることです。

## Control Plane

Factory OSは**ユーザー管理のCodexカスタマイズ層における最上位Control Plane**として設計されています。MCP、Rules、Skills、Custom Agents、Hooks、project-local AGENTSは配下の能力・制約として扱います。Codex本体のsystem/admin/security policyを上書きするものではありません。

```text
USER
  │
  ▼
Codex Factory OS
  ├─ Factory / task routing
  ├─ model & reasoning policy
  ├─ subagent scheduling
  ├─ quota/cost guardrails
  ├─ verification policy
  └─ environment governance
       │
       ├─ General Factory
       ├─ Software Factory
       ├─ CAD / 3DP Factory
       ├─ Research Factory
       ├─ Data Factory
       └─ Document Factory
             │
             ├─ Luna  : bounded repetition/extraction
             ├─ Terra : routine worker / exploration
             ├─ Sol   : senior owner / integration / engineering
             └─ Astra : scarce hard-reasoning specialist
```

## Cost/performance defaults

- 普通のCodex親役／高度な所有権: **Sol**
- 大量の探索・明確な実装・テスト: **Terra**
- 単純反復・抽出: **Luna**
- 難しい新規設計・原因不明問題・繰返し失敗: **Astra specialist**
- Astraは原則read-onlyで、難所を解いた後の実装をSol/Terraへ戻す
- trivial taskではsubagentを起動しない
- 通常は1–2 child、3–4は大きな独立read、5–6は例外
- 同じ探索を複数Agentへ重複発注して投票しない
- overlapping writesはsingle owner

詳細: `07-final/TOKEN_EFFICIENCY.md`

## Components

| Phase | Component | Status |
|---|---|---|
| 01 | Deterministic Factory Router | Complete |
| 02 | 31 Custom Agent profiles | Complete |
| 03 | 6 Factory Skills + lazy references | Complete |
| 04 | Hooks / runtime model+quota probe / model audit | Complete |
| 05 | Environment Governor | Complete |
| 06 | Installer / updater / Doctor / safe uninstall / quarantine cleanup | Complete |
| 07 | Full re-read / repair / integration validation / packaging | Complete in packaged build |

## Windows quick start

1. ZIPを展開する。
2. PowerShellで展開先へ移動する。
3. `./install.ps1` を実行する。
4. Codexを再起動する。
5. Codexで `/hooks` を開き、新規Factory OS hooksを確認して信頼する。
6. `./doctor.ps1` を実行する。
7. `./govern.ps1 --md-out governance.md` を実行し、既存MCP / Rules / Skills / Agents / Hooksの棚卸し結果を確認する。
8. cleanupはレポートをレビューしてから実行する。削除ではなくquarantineが既定。

完全手順: `INSTALL_WINDOWS.md`

## Existing environment safety

Installerは既存`config.toml`、MCP、Rules、無関係Skills/Agents/Hooksを勝手に削除しません。

導入前に:
- source bundle完全性チェック
- 同名Agent/Skill競合チェック
- managed marker破損チェック
- hooks.json parseチェック
- timestamped backup
- Governor inventory

を行います。

UninstallもFactory OS所有範囲だけを対象にし、Factory Agent/Skillが導入後にローカル変更されていれば削除せず保全します。

## Model/runtime compatibility

Custom agentsには推奨モデルを設定していますが、モデルIDは将来変わり得ます。Runtime resolverとSubagentStart auditは`model/list`/実行時model情報を使い、`gpt-5.6`と`gpt-5.6-sol`をSol aliasとして扱います。

Astra spawn境界ではのみquota/model availabilityを確認します。通常ターンごとにApp Serverを起動しないため、レイテンシと無駄な処理を抑えます。

## Factory skills

- `factory-general`
- `factory-software`
- `factory-cad-3dp`
- `factory-research`
- `factory-data`
- `factory-document`

詳細手順は各Skillの`references/`へ分離され、必要時のみ読みます。

## cadMCPとの関係

Factory OSはcadMCPを置き換えません。cadMCP完成後は、CAD/3DP Factoryが利用するgeometry / engineering / execution backendの1つとして接続する想定です。

## Important limitations

このビルドはLinux隔離環境でfresh-processの静的・統合テストを実行していますが、ユーザーの実Windows Codex環境そのものはここから実行できません。そのため以下は導入後Doctor/Hook reviewで確認してください。

- 実Codex CLI/IDEでのhooks trust
- 実アカウントのmodel availability / quota
- custom-agent modelが実際に指定どおり起動したか（auditで検査）
- 既存MCP/Rules/Skillsの実棚卸し

レビュー記録: `07-final/REVIEW.md`

Final fresh-process validation: **70/70 tests passed**, Python compileall passed, missing relative imports=0, JSON/TOML parse errors=0, broken Skill references=0.

## Official references used for the final review

- https://developers.openai.com/ja-JP/docs/agent-configuration/subagents
- https://developers.openai.com/ja-JP/docs/customization/overview
- https://developers.openai.com/ja-JP/docs/agent-configuration/agents-md
- https://developers.openai.com/ja-JP/docs/hooks
- https://developers.openai.com/ja-JP/docs/config-file/config-reference
- https://developers.openai.com/ja-JP/docs/models
