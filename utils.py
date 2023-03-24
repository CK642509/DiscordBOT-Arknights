import subprocess

def exchange():
    subprocess.run("./START.exe")

def getResult():
    with open("Results.txt", "r") as f:
        return f.read()

def getUsers():
    with open("_User data.txt", "r") as f:
        text = f.read()
        return "\n".join(text.split("\n")[2:])

def getClues():
    with open("input.txt", "r") as f:
        return f.read()

def setClues(clues):
    # get previous clues
    text = getClues()
    clue_list = text.split("\n")[:8]

    # get user list (lowercase)
    user_list = getUsers().split("\n")
    user_list = list(map(lambda x: x.lower(), user_list))
    idx = user_list.index(clues.split(",")[0].lower())

    # set new clues
    clue_list[idx] = clues.split(",")[1].strip()
    new_clues = "\n".join(clue_list)

    with open("input.txt", "w") as f:
        f.write(new_clues)

def getHelp():
    return """
**__使用方法說明__**
1. 設定線索:
    - 使用 `/clue` 設定線索
    - 一次只能設定一個玩家
    - 後面的參數格式為: 玩家名稱, 線索
    - 參數範例: JABO, 1123 56
    - 成功後會回傳當前所有線索
2. 計算
    - 使用 `exchange` (注意: 沒有斜線)
    - 等待其回傳「計算完畢」
3. 取得計算結果
    - 使用 `/result` 取得結果
"""
