# raspi-ai-agent-kit — ラズパイで動くAIエージェント構築キット

```
# ============================================================
#  ⚠️⚠️⚠️  重要な注意（必ずお読みください）  ⚠️⚠️⚠️
#
#  1. 機密性の高い書類（契約書・個人情報・社外秘資料など）は
#     くれぐれもこのシステムで扱わないでください。
#  2. ラズパイに入れる資料は「コピー」にしてください。
#     オリジナルは必ず別途（PC・社内サーバー等）保存してください。
#  3. APIキー・トークン等の秘密情報はファイルに直書きせず、
#     環境変数（.bashrc）で管理してください。
# ============================================================
```

Raspberry Pi 1台で動く、AIエージェント（LLMボット）の構築キットです。
教育用途（中高生の学習パートナー）を想定して実運用で検証した構成を、汎用化したものです。

## できること

- DiscordからAIに話しかけると、資料をもとに回答するボットが動く
- 画像（写真・図・手書きノート）を送ると内容を見て答える（マルチモーダル）
- AIが作った図解・資料をWebhookでチャンネルに返信する
- コピペだけでセットアップ可能（bashが苦手な人向けに設計）

## 構成

```
raspi-ai-agent-kit/
├── README.md                 ← このファイル
├── docs/
│   ├── SETUP.md              セットアップ手順書（コピペで進められる）
│   ├── opencode.json.template  opencode設定テンプレート
│   └── python_sample.py      PythonからLLM APIを呼ぶ最小サンプル
├── plugins/
│   ├── opencode-link.js      Discord連携プラグイン
│   ├── opencode-link-chunk.js  （pluginsフォルダの「外」に置く。詳細はSETUP.md）
│   └── package.json
├── skills/                   AIの振る舞いを定義するスキル集
│   ├── study-support/        学習支援（答えを教えず考え方を導く）
│   ├── llm-practice/         LLM・APIの仕組みを体験的に学ぶ
│   ├── linux-basics/         Linux基本操作の支援
│   ├── image-receive/        受信画像の読み取り
│   ├── image-send/           成果物の画像送信
│   ├── learning-diary/       学習ログの記録
│   └── data-viz/             データ可視化（2D・3D・MATLAB/Octave/matplotlib・資料の逸脱禁止ルール付き）
├── AGENTS.example.md         AIの行動ルールのテンプレート
└── LICENSE                   MIT License
```

## クイックスタート（概要）

詳細は `docs/SETUP.md` を参照してください。

1. Raspberry Pi OS (64-bit) をmicroSDに書き込み起動
2. opencodeをインストール
3. Zhipu GLMのAPIキーを取得（無料枠あり）して `~/.bashrc` に登録
4. `opencode.json` を設定（テンプレートをコピー）
5. Discordボットを作成しプラグインを設置
6. `~/AGENTS.example.md` を `~/AGENTS.md` として配置し、AIのルールを定める
7. ホーム(~)から `opencode` を起動

## モデル構成（デフォルト）

- **GLM-4.7-Flash**（テキスト・無料）— デフォルト
- **GLM-4.6V-Flash**（マルチモーダル・無料）— 画像用。TUIの `/models` で切替
- **GLM-5.3-Flash**（有料）— 高性能用。課金登録後に1行変更で切替

他社API（OpenAI互換）にも `opencode.json.template` の `baseURL` と `models` を書き換えるだけで対応できます。

## 実運用で学んだ設計上のポイント

- **プラグインはフラットに**: `opencode-link.js` は `plugins/` 直下、chunkは**pluginsの外**（起動しなくなる事故の実績あり）
- **question禁止設定必須**: `permission: {question: deny}`（Discord運用ではセッション停止の原因になる）
- **成果物はWebhook送信**: テキスト出力は画面に見えないため、ファイル化してチャンネルへ添付
- **日本語フォルダ名対応**: 日本語設定のOSでは `~/ダウンロード` になる点を手順書に明記

## ライセンス

MIT License
