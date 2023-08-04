import re
import shutil
import sys
from pathlib import Path
from threading import Thread

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "y",
    "",
    "e",
    "yu",
    "u",
    "ja",
    "je",
    "i",
    "ji",
    "g",
)


JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
MP4_VIDEOS = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
OTHERS = []
ARCHIVES = {"ZIP": []}


REGISTER_EXTENSION = {
    "images": {
        "JPEG": JPEG_IMAGES,
        "JPG": JPG_IMAGES,
        "PNG": PNG_IMAGES,
        "SVG": SVG_IMAGES,
    },
    "audio": {"MP3": MP3_AUDIO},
    "video": {"MP4": MP4_VIDEOS},
    "documents": {
        "DOC": DOC_DOCUMENTS,
        "DOCS": DOCX_DOCUMENTS,
        "TXT": TXT_DOCUMENTS,
        "PDF": PDF_DOCUMENTS,
    },
}

FOLDERS = []
TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name):
    t_name = re.sub(r"\W", "_", name.stem)
    t_name = name.name.translate(TRANS)
    return t_name


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename))


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename))


def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.with_suffix(""))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f"Its not archive {filename}!")
        folder_for_file.rmdir()
        return
    filename.unlink()


def handle_folder(folder: Path) -> None:
    try:
        folder.rmdir()
    except OSError:
        print(f"Sorry, we can not delete the folder: {folder}")


def start_threaded(folder: Path) -> None:
    media_threads = []
    for fldr in REGISTER_EXTENSION:
        for ext, file_list in REGISTER_EXTENSION[fldr].items():
            for file in file_list:
                target_folder = folder / fldr / ext
                thread = Thread(target=handle_media, args=(file, target_folder))
                media_threads.append(thread)
                print(f"Starting thread for file: {file}")
                thread.start()

    other_threads = []
    for file in OTHERS:
        target_folder = folder / "OTHER"
        thread = Thread(target=handle_other, args=(file, target_folder))
        other_threads.append(thread)
        print(f"Starting thread for file: {file}")
        thread.start()

    archive_threads = []
    for file_ext in ARCHIVES:
        for file in ARCHIVES[file_ext]:
            target_folder = folder / "archives" / file_ext
            thread = Thread(target=handle_archive, args=(file, target_folder))
            archive_threads.append(thread)
            print(f"Starting thread for archive: {file}")
            thread.start()

    folder_threads = []
    for folder in FOLDERS:
        thread = Thread(target=handle_folder, args=(folder,))
        folder_threads.append(thread)
        print(f"Starting thread for folder: {folder}")
        thread.start()

    for thread in media_threads + other_threads + archive_threads + folder_threads:
        thread.join()

    print("All threads have finished.")


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_file():
            file_ext = get_extension(item.name)
            if file_ext in REGISTER_EXTENSION["images"]:
                REGISTER_EXTENSION["images"][file_ext].append(item)
            elif file_ext in REGISTER_EXTENSION["audio"]:
                REGISTER_EXTENSION["audio"][file_ext].append(item)
            elif file_ext in REGISTER_EXTENSION["video"]:
                REGISTER_EXTENSION["video"][file_ext].append(item)
            elif file_ext in REGISTER_EXTENSION["documents"]:
                REGISTER_EXTENSION["documents"][file_ext].append(item)
            elif file_ext in ARCHIVES:
                ARCHIVES[file_ext].append(item)
            else:
                OTHERS.append(item)
        elif item.is_dir():
            FOLDERS.append(item)
            scan(item)


def main_with_threads(folder: Path) -> None:
    scan(folder)
    start_threaded(folder)


def start():
    try:
        folder_for_scan = Path(sys.argv[1])
        print(f"Start in folder {folder_for_scan.resolve()}")
        main_with_threads(folder_for_scan.resolve())
    except IndexError:
        print("Please provide the folder you need to sort/clean")


if __name__ == "__main__":
    start()
