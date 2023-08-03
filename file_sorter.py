from pathlib import Path
import re


REGISTER_EXTENSION = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "audio": [".mp3"],
    "video": [".mp4"],
    "documents": [".txt", ".docx", ".doc", ".pdf",".xls",".xlsx"],
    "archives": [".tar", ".gz", ".7z", ".zip"],
    "Python": [".py"],
}

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", 'i', "ji", "g")

