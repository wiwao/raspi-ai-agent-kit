# セットアップ手順書

```
# ============================================================
#  ⚠️ 重要な注意 ⚠️
#  1. 機密性の高い書類はこのシステムで扱わないでください
#  2. ラズパイに入れる資料は「コピー」にすること。
#     オリジナルは必ず別途保存すること
# ============================================================
```

対象: Raspberry Pi 4B（4GB推奨・2GBでも可）/ すべてのコマンドはコピペで動きます

## 用意するもの
- Raspberry Pi 4B（4GB推奨）+ 電源(USB-C 5V/3A)
- microSD 32GB以上
- ディスプレイ・キーボード（初回のみ。HDMI microはPi4用）
- Wi-Fi環境
- Discordアカウント（ボット連携する場合）

## ステップ1: OSインストール（30分）
1. 別PCで Raspberry Pi Imager を入手: https://www.raspberrypi.com/software/
2. OS「Raspberry Pi OS (64-bit)」/ ストレージにmicroSDを選択
3. 設定編集: ユーザー名・Wi-Fi・タイムゾーンAsia/Tokyo・SSH有効化
4. 書き込み→SDをラズパイへ→起動

## ステップ2: 更新とキットの展開（20分）【全部コピペでOK】
```bash
sudo apt update && sudo apt upgrade -y
```
このキットを展開します。ブラウザでダウンロードした場合は日本語フォルダ環境では ~/ダウンロード に入ります（両方の例を載せます）:
```bash
cd ~
tar -xzf ~/raspi-ai-agent-kit.tar.gz
```
または:
```bash
tar -xzf ~/ダウンロード/raspi-ai-agent-kit.tar.gz -C ~
```
確認（`ls` でREADME.mdなどが出れば成功）:
```bash
ls ~/raspi-ai-agent-kit
```

## ステップ3: opencodeのインストール
公式の手順に従って導入してください: https://opencode.ai

## ステップ3.5（任意）: 可視化ツールのインストール
データのグラフ化（skills/data-viz）を使う場合のみ:
```bash
pip3 install matplotlib
sudo apt install octave -y   # MATLAB互換の3Dプロットも使う場合
```
※ MATLAB本体は有償ライセンス製品でラズパイでは動作しません。ラズパイ上ではOctave（MATLAB互換・無料）かmatplotlibを使います

## ステップ4: APIキーの登録
1. LLMプロバイダのアカウントを作成し、APIキーをコピー
   （この手順書のデフォルトは Zhipu GLM: https://open.bigmodel.cn）
2. キーを環境変数に登録（ファイルへの直書きはしない）:
```bash
echo 'export ZHIPU_API_KEY="★APIキー★"' >> ~/.bashrc
source ~/.bashrc
```

## ステップ5: opencode.json（モデル設定）
テンプレートをコピーして使います（無料モデルで即動作・question禁止込み）:
```bash
mkdir -p ~/.config/opencode
cp ~/raspi-ai-agent-kit/docs/opencode.json.template ~/.config/opencode/opencode.json
```
内容（参考・テンプレートと同じ）:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "zhipu/glm-4.7-flash",
  "provider": {
    "zhipu": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Zhipu GLM",
      "options": {
        "baseURL": "https://open.bigmodel.cn/api/paas/v4",
        "apiKey": "{env:ZHIPU_API_KEY}"
      },
      "models": {
        "glm-4.7-flash": {"name": "GLM-4.7-Flash (Free Text)"},
        "glm-4.6v-flash": {"name": "GLM-4.6V-Flash (Free Multimodal)"},
        "glm-5.3-flash": {"name": "GLM-5.3-Flash (Paid)"}
      }
    }
  },
  "permission": {"question": "deny"}
}
```
※ `permission: {question: deny}` は必ず残す（Discord運用でセッション停止を防ぐ）
※ 有料モデルへの切替: `"model"` の行を `"zhipu/glm-5.3-flash"` に変更（課金登録後）
※ 画像用への切替: TUIで `/models` → `glm-4.6v-flash`

## ステップ6: プラグイン設置（★失敗しない配置）
```bash
mkdir -p ~/.config/opencode/plugins
cp ~/raspi-ai-agent-kit/plugins/opencode-link.js ~/.config/opencode/plugins/opencode-link.js
cp ~/raspi-ai-agent-kit/plugins/opencode-link-chunk.js ~/.config/opencode/
sed -i 's|./opencode-link-chunk.js|../opencode-link-chunk.js|' ~/.config/opencode/plugins/opencode-link.js
```
※ chunkはpluginsフォルダの【外】に置く（中に入れると全システムが起動しなくなる＝実機で確認済みの事故）

## ステップ7: ボット接続設定（Discord連携する場合）
1. https://discord.com/developers/applications でボットを新規作成
2. Bot設定で「MESSAGE CONTENT INTENT」をON → Save Changes（必須）
3. 招待URLをブラウザで開いてサーバーに認可:
   `https://discord.com/oauth2/authorize?client_id=★ApplicationID★&scope=bot&permissions=68608`
4. チャンネルID・ユーザーIDを開発者モードでコピー
5. 設定ファイル:
```bash
mkdir -p ~/.opencode
nano ~/.opencode/opencode-link.json
```
```json
{
  "provider": "discord",
  "botToken": "★ボットのトークン★",
  "channelId": "★チャンネルID★",
  "allowedUserIds": ["★管理者のユーザーID★"]
}
```
※ opencodeは必ずホーム(~)から起動（設定の場所がここで固定される）

## ステップ8: 成果物送信用Webhook
1. チャンネル設定→連携サービス→ウェブフック→新規作成→URLコピー
```bash
nano ~/.discord-webhook-url
```
（URLを1行だけ保存。AIが成果物をチャンネルへ添付送信するときに使う）

## ステップ9: AGENTS.mdの配置（最重要）
```bash
cp ~/raspi-ai-agent-kit/AGENTS.md ~/AGENTS.md
```
※ opencodeは起動フォルダ直下のAGENTS.mdを毎回自動読込する。ホームから起動するため ~/AGENTS.md が効く
※ 内容を編集して、あなたの用途に合わせたルールにしてください

## ステップ10: 起動とテスト
```bash
pkill -f opencode
cd ~
opencode >/tmp/oc-tui.log 2>&1 &
```
→ チャンネルのメンバーリストでボットが緑になる → 「テスト」と送る → 返信で完成

## トラブル対処（実機で確認済みの事象）
| 症状 | 対処 |
|---|---|
| Unexpected server errorで起動しない | plugins内に.jsが2つ以上ないか確認。chunkはpluginsの外へ |
| ボットがオフライン | MESSAGE CONTENT INTENT未ON/未Save。Token無効なら再発行 |
| Used disallowed intents | 同上。PortalでINTENTをON |
| 緑だが返信しない | 無料APIのレート制限。待つか有料化 |
| 設定が効かない | opencode-link.jsonは「起動したフォルダの.opencode/」を読む。ホームから起動しているか確認 |
| 401エラー | APIキー貼付ミス。`source ~/.bashrc` を忘れずに |

> ★日本語設定のOSの注意: 日本語でセットアップするとフォルダ名が日本語になります
> （ダウンロード/ドキュメント/画像 等）。ブラウザでダウンロードしたファイルは ~/ダウンロード に入ります。
> （英語名に統一したい場合は: `LANG=C xdg-user-dirs-update --force` を実行→再ログイン）

## 安全運用の心得（再掲）
- **機密性の高い書類を扱わない**: 契約書・個人情報・社外秘資料は入れない
- **コピーだけを置く**: ラズパイに置く資料はコピーにし、オリジナルは別途保存する
- 秘密情報は環境変数で管理し、設定ファイルに直書きしない
