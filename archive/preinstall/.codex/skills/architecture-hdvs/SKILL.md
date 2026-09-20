---
name: architecture-hdvs
description: 高密度垂直スライス（High-Density Vertical Slice）アーキテクチャの詳細ルール。UI/DSP/Tauri デスクトップアプリの両方に対応。ディレクトリ構造の設計、featureの追加、依存関係の設計、ARCHITECTURE.mdの更新、f64音質保護が必要な audio/DSP プロジェクトで参照する。
---

# 高密度垂直スライス (High-Density Vertical Slice) アーキテクチャ

StellaSonic 等「UI + オーディオ DSP エンジン + Tauri」型デスクトップアプリ向けに調整された版。
UI 中心 SaaS プロジェクトには §A、DSP / Rust ワークスペース構成には §B を適用する。

---

## 1. 設計思想

Feature-Sliced Design (FSD) を基盤とし、**AI のコンテキストウィンドウ最適化**と
**音質を損なわないコード設計**のために独自進化させたアーキテクチャ。

### 従来手法との比較

| 観点 | レイヤードアーキテクチャ | Clean Architecture | **高密度垂直スライス** |
|---|---|---|---|
| 分割軸 | 技術的責務（横分割） | 依存の方向（同心円） | **機能単位（縦分割）** |
| ファイル数 | 多い（層×機能） | 非常に多い | **最小限** |
| AI 親和性 | 低（複数層を横断） | 低（抽象化が多い） | **最高（1 フォルダ完結）** |
| 機能追加 | 複数層を同時修正 | 複数層を同時修正 | **1 フォルダで完結** |
| DSP 親和性 | 中（層跨ぎで型劣化リスク） | 低（過抽象で f64 保護困難） | **高（feature 内で数値精度を担保）** |

### 5 つの基本原則

1. **スライスの自己完結性** — 1 つの `features/xxx` フォルダだけ読めば、その機能の全てが理解できる
2. **スライス間の壁** — UI feature 同士は互いの存在を知らない。連携は必ず上位層か共通層経由
3. **一方通行の依存（UI 層）** — `app → widgets → features → entities → shared` の順序は絶対不可侵
4. **DSP プリミティブ共有（新規）** — リアルタイム DSP では `shared/dsp/` に数値プリミティブを集約し、feature 間で借用可。UI 層の strict な禁則とは別系統
5. **数値精度の保護（新規）** — DSP パイプラインは `f64` 内、**入出力の最外周のみ `f32` 許可**。型変換を feature 間境界で発生させない

---

## 2. 適用バリエーション

プロジェクトの性質でセクションを使い分ける:

| プロジェクト種別 | 主セクション | 例 |
|---|---|---|
| UI 中心（Web/SaaS） | §A のみ | Next.js SaaS, Nuxt ダッシュボード |
| Tauri + 単一 Rust | §A + §C（縮小版） | Tauri デスクトップツール |
| **Tauri + 複数 Rust crate + DSP（オーディオ等）** | §A + §B + §C | **StellaSonic 等** |

---

# §A. UI 層ルール（フロントエンド）

## A.1 ディレクトリ構造モデル

Next.js App Router を前提とする。Vite/Leptos の場合は `app/` を `routes/` や `entry/` に読み替える。

```
web/                          # フロント root（src/ 挟まず web/ 直下でも可）
├── app/                      # Next.js App Router 専用（ルーティングのみ）
│   ├── layout.tsx            # 全体レイアウト、Provider 群ラップ
│   ├── page.tsx              # ルートページ
│   └── [route]/              # 各ルート（Widget/Feature を配置するだけ）
│       └── page.tsx
│
├── features/                 # ★【絶対コア】高密度垂直スライス
│   └── [feature-name]/       # 例: playback, simulator, eq
│       ├── index.ts          # 公開 API。外部に見せる Component/Hook を re-export
│       ├── [feature-name]-engine.tsx  # UI + Hook + 状態管理（300〜500 行）
│       ├── api/              # Tauri invoke / fetch
│       │   └── [feature-name]-api.ts
│       ├── components/       # この機能専用のサブ UI
│       │   └── [ComponentName].tsx
│       ├── hooks/            # この機能専用 Hook
│       ├── assets/           # この機能専用のアイコン、小音源、json プリセット
│       ├── types.ts          # 機能専用型（entities 未満）
│       └── README.md         # 責務を 1〜3 行で記述
│
├── widgets/                  # 複数 features を組み合わせた画面パーツ
│   └── [widget-name]/
│
├── entities/                 # ビジネスデータの Single Source of Truth
│   ├── generated/            # Rust から自動生成された型（ts-rs / specta）
│   ├── models.ts             # 自動生成型の re-export + Zod スキーマ
│   └── transformers.ts       # DB↔UI 間の変換
│
└── shared/
    ├── ui/                   # shadcn/ui 等の共通デザイン部品
    ├── lib/                  # utils / constants / Tauri クライアント設定
    ├── hooks/                # 汎用 Hook (useDebounce 等)
    ├── store/                # Zustand グローバルストア
    └── assets/               # アプリ全体で使うフォント・背景・アイコン
```

### ⚠ UI 層への厳命

`web/controllers/`、`web/services/`、`web/repositories/`、`web/utils/`（ルート直下）等の
**レイヤード的フォルダ**を勝手に作成することを**固く禁ずる**。

## A.2 UI 層の依存関係（厳格・逆流禁止）

```
  app ──→ widgets ──→ features ──→ entities ──→ shared
   │                      │                        ↑
   │                      └────────────────────────┘
   └────────────────────────────────────────────────┘

  ✗ shared → features       （逆流禁止）
  ✗ entities → features     （逆流禁止）
  ✗ features/A → features/B （横断禁止）
```

**違反検出**: `eslint-plugin-boundaries` で静的チェック。

## A.3 UI 層のファイルサイズ制限

| ルール | 値 | 理由 |
|---|---|---|
| 1 ファイル最大行数 | **500 行** | AI コンテキストウィンドウ閾値 |
| 1 ファイル推奨行数 | 300〜400 行 | 情報密度と可読性の最適点 |
| 1 関数最大行数 | **80 行** | 単一責務の維持 |
| 1 関数推奨行数 | 20〜50 行 | 認知単位の理想 |

---

# §B. DSP / オーディオエンジン層ルール（Rust 複数 crate 構成）

## B.1 Rust ワークスペース構造

```
apps/backend/                 # Cargo workspace root
├── engine/                   # ★ オーディオエンジン（独立 crate）
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs            # 公開 API（登録のみ）
│       ├── features/         # ★ DSP 機能の垂直スライス
│       │   ├── eq/
│       │   │   ├── mod.rs
│       │   │   ├── design.rs      # フィルタ設計
│       │   │   ├── iir.rs         # IIR 実装
│       │   │   ├── linear_phase.rs # 線形位相 EQ
│       │   │   ├── realtime.rs    # リアルタイム処理
│       │   │   └── README.md
│       │   ├── spatial/           # 既存サラウンド
│       │   │   ├── mod.rs
│       │   │   ├── processor.rs
│       │   │   ├── convolver.rs
│       │   │   └── upmix/
│       │   ├── simulator/         # 物理シミュレータ
│       │   │   ├── mod.rs
│       │   │   ├── config.rs
│       │   │   ├── presets/       # プリセット別にサブディレクトリ化
│       │   │   │   ├── cinema/
│       │   │   │   │   ├── thx.rs
│       │   │   │   │   ├── imax.rs
│       │   │   │   │   ├── atmos.rs
│       │   │   │   │   └── mod.rs
│       │   │   │   ├── studio.rs
│       │   │   │   └── concert.rs
│       │   │   ├── acoustic/      # 音響計算（ISM/SH/Reverb を分離）
│       │   │   │   ├── ism.rs
│       │   │   │   ├── statistical_reverb.rs
│       │   │   │   └── spherical_harmonics.rs
│       │   │   ├── sim_processor/ # リアルタイム畳み込み
│       │   │   │   ├── mod.rs
│       │   │   │   ├── block_processor.rs
│       │   │   │   └── crossfade.rs
│       │   │   ├── ray_tracing/
│       │   │   ├── externalization/
│       │   │   └── binaural_decoder.rs
│       │   ├── output/            # WASAPI / ASIO
│       │   ├── resampler/
│       │   ├── pipeline.rs
│       │   └── metadata.rs
│       ├── shared/
│       │   ├── dsp/         # ★ DSP プリミティブ（feature 間で借用可）
│       │   │   ├── partitioned_convolver.rs
│       │   │   ├── circular_delay.rs
│       │   │   ├── biquad.rs
│       │   │   ├── fft.rs
│       │   │   └── window.rs
│       │   ├── types.rs     # f64 パイプライン型（SampleBuffer<f64> 等）
│       │   └── buffers.rs   # アロケーションフリーバッファ
│       └── resources/       # HRTF / SOFA / 材質 DB バイナリアセット
│
├── db/                      # DB クライアント（独立 crate）
│   └── src/
│       ├── lib.rs
│       ├── client.rs
│       ├── schema.rs
│       └── models.rs        # Track / Playlist 等
│
├── analyzer/                # スペクトル分析（独立 crate）
└── server/                  # サーバ機能（独立 crate）
```

## B.2 DSP 層の依存ルール（UI 層より緩和）

```
  Tauri commands
       │
       ▼
  engine::features::*  ──→  engine::shared::dsp
       │                          ↑
       │   (feature 間は shared/dsp 経由でのみ連携)
       ▼
  engine::shared::types (f64 pipeline)

  ✓ features/simulator → shared/dsp::PartitionedConvolver  （OK）
  ✗ features/simulator → features/spatial::SomeHelper      （NG、shared/dsp へ昇格）
  ✗ features/eq → features/simulator                       （NG）
```

**ルール**:
- feature 間で共有したい DSP プリミティブは **必ず `shared/dsp/` に昇格**
- `shared/dsp/` は feature に依存してはならない（純粋な数値計算）
- feature 内に他 feature の型を露出させない

## B.3 DSP 層のファイルサイズ制限（UI 層より緩和）

| ルール | 値 | 理由 |
|---|---|---|
| DSP 実装ファイル最大行数 | **1000 行** | アルゴリズムの連続性を保つ必要がある |
| DSP 実装ファイル推奨行数 | 500〜800 行 | 可読性と f64 計算連続性のバランス |
| DSP 関数最大行数 | **150 行** | ブロック処理ループが長くなる場合あり |
| DSP 関数推奨行数 | 30〜100 行 | |
| **テストコード** | 別ファイル推奨 | `#[cfg(test)] mod tests` が 500 行超えるなら `tests/` ディレクトリへ |

### DSP 分割の判断基準

以下に当てはまるなら分割:
- **責務が複数存在**（例: ISM 鏡像計算 + 統計残響 + SH 係数）→ 責務ごとに分割
- **1 ファイル 1500 行超**（テスト除く）→ 機械的に分割
- **実装とテストで 2500 行超** → テストを外出し

以下なら分割しない:
- アルゴリズム単位で連続した f64 計算が必要
- 分割すると関数呼び出しオーバーヘッドでリアルタイム性が落ちる
- 型が計算内部のみで使われ、公開する意味がない

## B.4 f64 パイプラインの保護ルール（最重要）

**このプロジェクトの音質はこのルールに依存する。**

```rust
// ✓ OK: 内部は全て f64
pub struct SimulatorProcessor {
    scratch: Vec<f64>,
    pending_in: VecDeque<f64>,
    // ...
}

impl SimulatorProcessor {
    pub fn process_block(&mut self, samples: &mut [f64]) { /* ... */ }
}

// ✓ OK: 出力デバイスへの最終変換のみ f32
fn write_to_wasapi(&self, samples: &[f64]) {
    let f32_buf: Vec<f32> = samples.iter().map(|&s| s as f32).collect();
    self.wasapi.write(&f32_buf);
}

// ✗ NG: 中間段で f32 に落とす
pub fn apply_eq(samples: &mut [f32]) { /* ... */ } // ← type を f64 に変更すべき

// ✗ NG: feature 境界で変換
let eq_out: Vec<f32> = apply_eq(input);
let spatial_in: Vec<f64> = eq_out.iter().map(|&s| s as f64).collect();
```

**例外（やむを得ない f32 使用）**:
- FFT ライブラリ（`rustfft`）が f32 しか高速実装を持たない場合（ただし前後で f64↔f32 変換する）
- HRIR / SOFA ファイルの原データが f32（ただし読み込み直後に f64 へ昇格）
- GPU シェーダ境界（CUDA/Vulkan は f32 中心）

**検証**: 型定義で `pub type Sample = f64;` を `shared/types.rs` に置き、検索で `f32` の露出を定期的に監査。

## B.5 アロケーションフリー原則

リアルタイム処理スレッド内では `Vec::push` / `Box::new` / `Arc::clone` を禁止。

```rust
// ✓ OK: 事前確保 scratch バッファを再利用
pub struct Processor {
    scratch_l: Vec<f64>,  // new() で確保
    scratch_r: Vec<f64>,
}

impl Processor {
    pub fn process(&mut self, input: &[f64]) {
        self.scratch_l.clear();  // 容量は維持、長さ 0
        self.scratch_l.extend_from_slice(&input[..half]);
        // ...
    }
}

// ✗ NG: 毎回確保
pub fn process(input: &[f64]) -> Vec<f64> {
    let mut out = Vec::new();  // ← リアルタイムで確保
    // ...
}
```

**BRIR 等の重い計算はバックグラウンドスレッドで実施**し、`SyncSender<Box<T>>` で完成品を再生スレッドへ手渡す。

---

# §C. Tauri バインディング層ルール

## C.1 Tauri `src-tauri/` 構造

```
src-tauri/
├── Cargo.toml
├── tauri.conf.json
├── capabilities/             # Tauri 権限（最小権限原則）
└── src/
    ├── main.rs               # エントリポイント（数行）
    ├── lib.rs                # プラグイン・コマンド登録のみ（< 300 行目標）
    ├── commands/             # ★ features とミラーリング
    │   ├── mod.rs
    │   ├── playback.rs
    │   ├── simulator.rs      # シミュレータ関連 Tauri コマンド
    │   ├── eq.rs
    │   ├── library.rs
    │   ├── youtube.rs
    │   └── spatial.rs
    ├── state/                # Tauri managed state
    │   ├── mod.rs
    │   ├── playback_state.rs
    │   └── simulator_state.rs
    ├── events/               # emit 用イベント定義
    │   └── mod.rs
    └── persistence/          # JSON 永続化（カスタムプリセット等）
        └── mod.rs
```

**lib.rs は `builder.invoke_handler(tauri::generate_handler![...])` の登録で終わる**。
ロジックは `commands/` `state/` へ分離。

## C.2 フロント ↔ Tauri ↔ Engine のミラーリング

```
web/features/simulator/    ↔  src-tauri/commands/simulator.rs  ↔  engine/features/simulator/
web/features/eq/           ↔  src-tauri/commands/eq.rs         ↔  engine/features/eq/
web/features/playback/     ↔  src-tauri/commands/playback.rs   ↔  engine/features/output/
```

**目的**: 機能名から 3 層すべてを O(1) で辿れる。

## C.3 型の Single Source of Truth（Tauri 特有）

**Rust 側の構造体が正**。TS 側は `ts-rs` または `specta` で自動生成。

```rust
// engine/shared/types.rs or src-tauri/src/commands/simulator.rs
#[derive(Serialize, Deserialize, TS)]
#[ts(export, export_to = "../web/entities/generated/")]
#[serde(rename_all = "camelCase")]
pub struct SimulatorConfig {
    pub preset_id: String,
    pub head_width_cm: f32,
    pub upmix_enabled: bool,
    // ...
}
```

→ `web/entities/generated/SimulatorConfig.ts` が自動生成される。
→ `web/features/simulator/types.ts` は `import { SimulatorConfig } from '@/entities/generated'` だけ。

**禁止**: TS 側で Rust 型を手書きで複製すること（StellaSonic の 776 行 `useSimulator.ts` 問題）。

---

# §D. プロジェクト共通ルール

## D.1 ARCHITECTURE.md の更新義務

**AI への義務**: 新機能追加・ディレクトリ変更時は、`ARCHITECTURE.md` の機能マップを
**必ず**更新する。コード変更と同時に実行する。

`ARCHITECTURE.md` は以下を含む:
- プロジェクト全体のレイヤー図（web / src-tauri / engine など）
- feature 一覧表（機能名、責務 1 行、主要ファイル、関連する他 feature）
- f64 パイプライン保証箇所の一覧（DSP プロジェクトのみ）
- 凍結資産一覧（ユーザ検証済みで触ってはいけない要素）

## D.2 README.md の feature 必須化

各 `features/xxx/README.md` は以下を含む（1〜3 行で簡潔に）:
- 責務（何をする機能か）
- 公開 API（index.ts / mod.rs が export するもの）
- 依存（`shared/dsp/XXX` を使う、など）

## D.3 分割の許可制

AI が分割を判断した場合、以下 3 点をユーザーに説明し許可を得ること:
1. なぜ分割が必要か（行数超過? 責務混在? f64 連続性無関係?）
2. どう分割するか（分割後のファイル構成案）
3. 分割後も AI 読み込みで断片化しないかの評価

## D.4 凍結資産（Frozen Assets）ルール

ユーザが「このパラメータは検証済みで触るな」と指定した要素は:
- コメントで `// FROZEN: <reason>` マーカを付与
- `tests/frozen_assets.rs`（または同等）で数値ハッシュ検証を追加
- リファクタ後に BRIR / IR / 係数などの SHA256 を比較

**例**: StellaSonic の THX/IMAX プリセット → リファクタで構造は変えても**数値出力は完全一致**を保証。

## D.5 禁止ディレクトリ（アンチパターン）

ルート直下に以下を作ることを**固く禁ずる**:
- `controllers/` / `services/` / `repositories/`（レイヤード）
- `utils/` / `helpers/` / `common/`（雑多置き場化する）
- `core/`（責務が曖昧）
- `misc/` / `tmp/` / `old/`（即ゴミ化する）

代わりに:
- 機能に紐づくなら `features/xxx/`
- 真に汎用なら `shared/{ui,lib,dsp,hooks,store}/`

---

## 付録: ファイル行数の目安早見表

| 層 | 種別 | 最大 | 推奨 | 備考 |
|---|---|---|---|---|
| UI | React コンポーネント | 500 | 300-400 | 高密度 engine ファイルの理想 |
| UI | Hook | 300 | 100-200 | engine 内 or 別ファイル |
| UI | API wrapper | 200 | 50-150 | Tauri invoke 集約 |
| DSP | アルゴリズム実装 | 1000 | 500-800 | f64 連続性のため |
| DSP | プリミティブ (shared/dsp) | 500 | 200-400 | 再利用前提で簡潔に |
| DSP | テスト（同ファイル内） | +500 | +300 | 超えたら外出し |
| Tauri | commands/*.rs | 800 | 300-500 | 複雑ならサービスに分離 |
| Tauri | lib.rs | 300 | < 200 | 登録のみ |
| 自動生成 | entities/generated/* | 制限なし | — | 手で編集禁止 |

---

## チェックリスト（新機能追加時）

- [ ] `web/features/<name>/` を作成し `README.md` 書いた
- [ ] `src-tauri/src/commands/<name>.rs` を作成
- [ ] `engine/src/features/<name>/` を作成（必要なら）
- [ ] 共通 DSP は `shared/dsp/` へ、UI 共通は `shared/ui/` へ
- [ ] Rust 型は `#[derive(TS)]` で TS 自動生成
- [ ] feature 間で型を直接参照していない（shared 経由）
- [ ] `ARCHITECTURE.md` の機能マップ更新
- [ ] リアルタイム処理なら `f64` 内部 + アロケーションフリー
- [ ] 凍結資産があるなら `// FROZEN:` マーカと数値テスト
