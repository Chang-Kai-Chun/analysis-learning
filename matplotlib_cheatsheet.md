# Matplotlib 圖片調整指令速查

`df.plot()` 會回傳一個 `ax`（座標軸物件），之後所有調整都對它操作。建議用 `fig, ax = plt.subplots()` 先建好畫布，控制最完整。

## 基本架構

```python
fig, ax = plt.subplots(figsize=(8, 5))          # 建立畫布，尺寸單位為英吋
ax.plot(df["Time (s)"], df["Voltage (V)"])      # 畫線
plt.show()
```

用 pandas 的 `df.plot` 也可以接到同一個 ax：

```python
ax = df.plot(x="Time (s)", y="Voltage (V)", figsize=(8, 5))
```

## 1. 標題與軸標籤

```python
ax.set_title("Photovoltage vs Time", fontsize=14)
ax.set_xlabel("Time (s)", fontsize=12)
ax.set_ylabel("Voltage (V)", fontsize=12)
```

## 2. 線條樣式（寫在 `ax.plot()` 內）

```python
ax.plot(x, y,
        color="tab:blue",       # 顏色：名稱、"#1f77b4"、(r,g,b)
        linewidth=1.5,          # 線寬（可縮寫 lw）
        linestyle="--",         # "-" 實線 / "--" 虛線 / ":" 點線 / "-." 點虛線
        marker="o",             # 資料點形狀："o" "s" "^" "x" "."
        markersize=4,           # 點的大小
        alpha=0.8,              # 透明度 0~1
        label="Sample A")       # 圖例用的名稱
```

## 3. 座標軸範圍與刻度

```python
ax.set_xlim(0, 10)              # x 軸範圍
ax.set_ylim(0.2, 0.3)           # y 軸範圍
ax.invert_yaxis()               # 反轉 y 軸

ax.set_xscale("log")            # 對數座標（也可 "linear"）
ax.set_yscale("log")            # 暗電流常用 y 軸取對數

ax.set_xticks([0, 2, 4, 6, 8, 10])             # 指定刻度位置
ax.tick_params(labelsize=10, direction="in")   # 刻度字體大小、刻度朝內
ax.minorticks_on()                             # 開啟次刻度
```

## 4. 格線與圖例

```python
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend(loc="upper right", fontsize=10, frameon=False)
# loc 可用："best" "upper left" "lower right" "center" 等
```

## 5. 文字、標註、輔助線

```python
ax.text(2, 0.27, "peak", fontsize=10)                  # 在座標位置加文字
ax.annotate("max", xy=(3, 0.28), xytext=(5, 0.29),
            arrowprops=dict(arrowstyle="->"))           # 帶箭頭的標註
ax.axhline(0.265, color="gray", linestyle=":")          # 水平參考線
ax.axvline(5, color="gray", linestyle=":")              # 垂直參考線
ax.axvspan(2, 4, color="yellow", alpha=0.2)             # 標示某一區間
```

## 6. 同圖多條線與雙 y 軸

```python
ax.plot(x, y1, label="A")
ax.plot(x, y2, label="B")

ax2 = ax.twinx()                  # 共用 x 軸、另一個 y 軸
ax2.plot(x, y3, color="tab:red")
ax2.set_ylabel("Current (A)")
```

## 7. 使用 cmcrameri 色盤

```python
import cmcrameri.cm as cmc

# 多條線依序取色
colors = cmc.batlow(np.linspace(0, 1, 5))     # 從色盤取 5 個顏色
for i, c in enumerate(colors):
    ax.plot(x, y[i], color=c)

# 熱圖或散點用 cmap
sc = ax.scatter(x, y, c=z, cmap=cmc.batlow)
fig.colorbar(sc, ax=ax, label="Z value")      # 色條
```

## 8. 多張子圖

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))   # 1 列 2 欄
axes[0].plot(x, y1)
axes[1].plot(x, y2)
fig.tight_layout()                                # 自動調整間距
```

## 9. 全域樣式與中文字型

```python
plt.rcParams["font.size"] = 12
plt.rcParams["axes.unicode_minus"] = False        # 避免負號顯示成方塊
plt.rcParams["font.family"] = "Microsoft JhengHei"   # 圖中要顯示中文時
plt.style.use("seaborn-v0_8-whitegrid")           # 套用內建風格
```

## 10. 存檔

```python
fig.savefig("plot.png", dpi=300, bbox_inches="tight")   # 高解析度，裁掉多餘白邊
fig.savefig("plot.pdf")                                  # 向量圖，論文常用
```

`savefig` 要放在 `plt.show()` **之前**，否則可能存到空白圖。

## 完整範例（套用 pv_triggered.csv）

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(df["Time (s)"], df["Voltage (V)"], color=cmc.batlow(0.3), lw=1.2, label="PV triggered")

ax.set_title("Photovoltage vs Time", fontsize=14)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage (V)")
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend(frameon=False)

fig.tight_layout()
fig.savefig("pv_triggered.png", dpi=300)
plt.show()
```

## 速查：最常改的幾項

| 想做的事 | 指令 |
|---|---|
| 改標題、軸名稱 | `set_title` / `set_xlabel` / `set_ylabel` |
| 改範圍 | `set_xlim` / `set_ylim` |
| 對數座標 | `set_yscale("log")` |
| 改顏色、線寬 | `plot()` 內的 `color` / `linewidth` |
| 加圖例 | `label=` 加 `ax.legend()` |
| 存檔 | `fig.savefig(..., dpi=300)` |
