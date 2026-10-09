---
name: data-viz
description: データの可視化（2D・3D）をするときに使う。MATLAB/Octave/matplotlibの3種の実装を提供。資料に書いてある数値・内容から逸脱しないことを最優先する
---

# データ可視化（2D・3D）スキル

## 最重要ルール: 資料の逸脱禁止（データサイエンスの基本）
1. **グラフにする数値は、必ずユーザー提供の資料内の値を使う**。資料に書いてあることから逸脱しない
2. **資料にないデータは、勝手に作らない・補間しない・「それっぽい値」を入れない**。
   資料にないものは「探索」する: 資料の別ページ・別資料・ローカル記録を検索して探す
3. それでも見つからない場合は、グラフ化せず「資料に該当データなし」と報告し、
   ユーザーに補完データの出所を確認する。推定値を入れる場合は軸ラベルに
   「推定値（出所: ○○）」と明記する
4. 出所の明記: 各グラフに「出典: ○○資料 p.X」等を必ず添える
5. 単位・軸の範囲・凡例は資料の数値と一致させる（目盛りを加工して見せかけを変えない）

## 使うツールの選び方
| 環境 | ツール | 備考 |
|---|---|---|
| MATLABライセンス保有 | MATLAB | 最も高機能。ラズパイ本体では動かない |
| ラズパイ上・無料 | **Octave** | MATLAB互換文法。`sudo apt install octave -y` |
| ラズパイ上・無料（Python） | matplotlib | `pip3 install matplotlib`。図をWebhook送信するときはこれ |

## 3Dプロットの基本形（同じ図を3つのツールで）

### MATLAB / Octave（共通文法）
```matlab
% 資料の数値をそのまま入れる（例: 3機器の消費電力と発熱量）
x = [2000 1400 132];      % 資料の値そのもの
y = [1800 1300 120];      % 資料の値そのもの
z = x + y;                 % 計算は根拠をコメントで残す
labels = {"TR", "UPS", "負荷A"};
scatter3(x, y, z, 100, 'filled'); hold on
for i = 1:3
    text(x(i)+20, y(i), z(i), labels{i});
end
xlabel('給電容量 [kW]'); ylabel('消費電力 [kW]'); zlabel('発熱量 [kW]');
grid on; title('出典: 負荷発熱量計算表 p.1');
print -dpng chart3d.png    % OctaveでのPNG出力
```

### matplotlib（Python・Webhook送信はこれで作る）
```python
# ★日本語ラベルには必ず日本語フォント設定（未設定だと文字が□になる・実機で確認済み）
# フォント無い場合の導入: sudo apt install fonts-noto-cjk -y
import matplotlib
matplotlib.use("Agg")          # 画面なし環境で必須
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Noto Serif CJK JP"   # 日本語フォント指定

x = [2000, 1400, 132]   # 資料の値そのもの
y = [1800, 1300, 120]   # 資料の値そのもの
labels = ["TR", "UPS", "負荷A"]

fig = plt.figure(figsize=(8, 6))   # 3D用に大きめ・文字は読みやすく
ax = fig.add_subplot(projection="3d")
ax.scatter(x, y, [a+b for a, b in zip(x, y)], s=100)
for xi, yi, li in zip(x, y, labels):
    ax.text(xi+20, yi, xi+yi, li)
ax.set_xlabel("給電容量 [kW]"); ax.set_ylabel("消費電力 [kW]")
ax.set_zlabel("発熱量 [kW]")
ax.set_title("出典: 負荷発熱量計算表 p.1")
plt.tight_layout()
plt.savefig("chart3d.png", dpi=150)
```

## 送信前チェック（skills/image-send と共通）
- ①軸ラベル・単位・凡例があるか ②文字が大きすぎず小さすぎないか（3Dは回転で隠れやすいのでfontsize大きめ）
- ③表示角度を調整（matplotlibは `ax.view_init(elev=20, azim=35)` など）して要素の重なりを避ける
- ④数値が資料と一致しているか最終確認してからWebhook送信する
