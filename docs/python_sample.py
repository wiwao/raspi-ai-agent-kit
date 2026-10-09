# 生徒用: PythonからGLM APIを呼ぶ最小サンプル
# 実行: python3 python_sample.py
import os, json, urllib.request

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
KEY = os.environ.get("ZHIPU_API_KEY", "")

def ask(question):
    body = json.dumps({
        "model": "glm-4.6v-flash",
        "messages": [{"role": "user", "content": question}],
    }).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    return data["choices"][0]["message"]["content"]

if __name__ == "__main__":
    while True:
        q = input("\n質問（終了は quit）: ")
        if q.strip() == "quit":
            break
        try:
            print("AI:", ask(q))
        except Exception as e:
            print("エラー:", e)
