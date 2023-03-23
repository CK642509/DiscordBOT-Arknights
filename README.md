# Discord BOT + Python + Render

## Start up
### 0. 建立虛擬環境
```
pip install virtualenv
virtualenv .venv
```

### 1. 安裝套件
```
pip install -r requirements.txt
```

### 2. 啟動機器人
執行 `main.py`

## 機器人使用方法
### 說明
- `exchange` 計算
- `/result` 取得結果
- `/clue` 設定線索
- `/clues` 顯示當前線索
- `/users` 顯示玩家清單
- `/help` 顯示說明


## 筆記
### 用 python 呼叫 .exe 檔
- 使用 `subprocess` 可以做到
- 交換線索的檔案們(包含 `.exe` 和 `.txt`)必須放在和 `main.py` 同一資料夾
- 原因是這支程式在讀取和寫入檔案時，所使用的路徑是「工作資料夾」，移到其他路徑會因為找不到檔案而出事

### timeout 
- 若把執行 exe 放在 slash command 中，會因為 timeout 而出錯
- 目前只能把執行 exe 的功能，由一般對話進行觸發