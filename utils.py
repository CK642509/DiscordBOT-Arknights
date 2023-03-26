import subprocess
import re

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

def setClues(clues: str):
    # get previous clues
    text = getClues()
    clue_list = text.split("\n")[:8]

    # get user list (lowercase)
    user_list = getUsers().split("\n")
    user_list = list(map(lambda x: x.lower(), user_list))

    # get the row number that needs to be updated
    idx = user_list.index(clues.split(",")[0].strip().lower())

    # set new clues
    new_clue = clues.split(",")[1].strip()
    # TODO: re
    # print(re.match("", new_clue))

    clue_list[idx] = new_clue
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
    - 參數範例: JABO, 112356 56
    - 成功後會回傳當前所有線索
2. 計算
    - 使用 `exchange` (注意: 沒有斜線)
    - 等待其回傳「計算完畢」
3. 取得計算結果
    - 使用 `/result` 取得結果
Github: https://github.com/CK642509/DiscordBOT-Arknights
"""

def formatClues(text:str):
    text = text.strip()

    # check if only contains 0-7
    if not re.match("/[^0-7]/", text):
        print("only 0-7")
    else:
        return ""
    
    if len(text.split(" ")) == 1:
        return f"{text} 0"
    elif len(text.split(" ")) == 2:
        return text
    else:
        return ""


