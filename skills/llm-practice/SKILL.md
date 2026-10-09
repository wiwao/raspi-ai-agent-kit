---
name: llm-practice
description: ユーザーにLLMやAPIの仕組みを教えるときに使う。AIとは何か・APIとは何かを体験的に学ばせる
---

# LLM・API学習の教え方

## 学習ステップ（ステップ1から順に）
1. **AIに話しかけてみる**: Discordでボットに質問する（これが一番かんたんなAPI利用）
2. **仕組みを絵で理解する**: 質問がインターネット越しにGLM APIへ行き、答えが返る流れを説明
3. **curlで直接叩く**: ターミナルで以下を実行させる（APIキーは先生が設定済み）
   curl -s https://open.bigmodel.cn/api/paas/v4/chat/completions -H "Authorization: Bearer $ZHIPU_API_KEY" -H "Content-Type: application/json" -d '{"model":"glm-4.6v-flash","messages":[{"role":"user","content":"こんにちは"}]}'
4. **JSONを読む**: 返ってきた答えがJSON形式であること、choices[0].message.content に答えがあることを教える
5. **Pythonで動かす**: 3行のPythonスクリプトで同じことをさせる（docs/python_sample.py 参照）
6. **AGENTS.mdを編集する**: AIの性格やルールを自分で変えさせて「AIを育てる」体験をする

## 教えるときのポイント
- 「AIは魔法ではなく、インターネット越しの計算サービス」と伝える
- LLMは時々間違える（もっともらしい嘘）ので、大事なことは必ず確認する習慣を教える
- 個人情報をAIに送らない理由（どこに届くか）もセットで教える

## よくある質問
- Q: AIは本当に入力を覚えているの? → A: このシステムでは会話は基本覚えない。覚えさせるにはファイルに書く（それがRAG）
- Q: 無料でずっと使える? → A: GLM-4.6V-Flashは無料。混雑時は待つことがある
