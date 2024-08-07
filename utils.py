import subprocess
import re
from datetime import date
from sys import platform


def exchange():
    if platform == "linux" or platform == "linux2":
        subprocess.run("./start")
    elif platform == "win32":
        subprocess.run("./START.exe")


def getResult():
    with open("Results.txt", "r", errors="replace", encoding="cp950") as f:
        return f.read()


def getUsers():
    with open("_User data.txt", "r", errors="replace", encoding="cp950") as f:
        text = f.read()
        return "\n".join(text.split("\n")[2:])


def getClues():
    with open("Input.txt", "r") as f:
        return f.read()


def getDetail():
    with open("detail.txt", "r") as f:
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

    with open("Input.txt", "w") as f:
        f.write(new_clues)

    # record details
    detail = getDetail()

    with open("detail.txt", "w") as f:
        detail_list = detail.split("\n")
        detail_list[idx] = f"{date.today()} {user_list[idx]:<7} {new_clue}"
        new_detail = "\n".join(detail_list)
        f.write(new_detail)


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


def formatClues(text: str):
    text = text.strip()

    # check if only contains 0-7
    if not re.match("/[^0-7]/", text):
        print("only 0-7")
    else:
        return ""

    result = re.split("\s+", text)
    if len(result) == 1:
        return f"{text} 0"
    elif len(result) == 2:
        return f"{result[0]} {result[1]}"
    else:
        return ""
