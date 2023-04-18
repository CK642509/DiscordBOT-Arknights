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
```
python main.py
```

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

### TODO
- [ ] 更彈性的線索格式規定
  - [x] 沒有打 0，就補 0
  - [x] 名字大小寫通用
  - [x] 沒有打名字就視為是幫自己設定
  - [ ] 名字與線索中間的分隔符號有更多選擇 (目前只有逗號)
  - [ ] 一次輸入多個帳號 + 線索也可以 (目前只有特定玩家有)
  - [x] 線索與指定線索之間有大於一個空格也可以
  - [ ] 線索防呆，若不符合格式就跳出錯誤處理
  - [ ] 更新 `/help` 的說明
- [ ] 環境變數整理
- [ ] 部屬在其他平台
- [ ] 將 `.exe` 以 python 重寫，方便部屬
- [ ] 部屬的替代方案：
  - [ ] 將原始碼 (C++) 編譯成 linux 可執行的執行檔
  - [ ] 找一個可以部屬 docker 的平台
        > 說不定 pywine 這個 docker image 可以