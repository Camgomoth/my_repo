import re
import shutil
import sys
from pathlib import Path
from file_generator import file_generator

TRANS = {ord("а"):"a",ord('б'): "b", ord('в'):"v", ord('г'):"g", ord('д'):"d", ord('е'):"e", ord('є'):"je",ord('ж'): "zh",
               ord('з'):"z", ord('и'):"y", ord('і'):"i", ord('ї'): "ji", ord('й'): "j", ord('к'): "k",  ord('л'):"l",  ord('м'):"m",  
               ord('н'):"n", ord('о'): "o",  ord('п'):"p",  ord('р'):"r",  ord('с'):"s", ord('т'): "t",  ord('у'):"u",
               ord('ф'):"f",  ord('х'):"h",  ord('ц'):"ts",  ord('ч'):"ch",  ord('ш'):"sh",  ord('щ'):"sch", ord('ь'): "", 
               ord('ю'): "ju", ord('я'): "ja",ord("A"):"A",ord('Б'): "B", ord('В'):"V", ord('Г'):"G", ord('Д'):"D", ord('Е'):"E",
               ord('Є'):"Je",ord('Ж'): "Zh",ord('З'):"Z", ord('И'):"Y", ord('І'):"I", ord('Ї'): "Ji", ord('Й'): "J", ord('К'): "K", 
               ord('Л'):"L",  ord('М'):"M", ord('Н'):"N", ord('О'): "O",  ord('П'):"P",  ord('Р'):"R",  ord('С'):"S", 
               ord('Т'): "T",  ord('У'):"U",ord('Ф'):"F",  ord('Х'):"H",  ord('Ц'):"Ts",  ord('Ч'):"Ch",  ord('Ш'):"S", 
               ord('Щ'):"Sch", ord('Ь'): "", ord('Ю'): "Ju", ord('Я'): "Ja"}




def normalize(name):
    name_search = name.rfind('.')
    if name_search == -1:
        return f'Name of the file is incorrect: {name}'
    position = name[(name_search):]
   
    new_name = name.replace(position,'')
    
    new_name = new_name.translate(TRANS)
    
    new_name = re.sub(r'\W', "_", new_name)
    
    return f"{new_name}{position}"


images = []
videos = []
documents = []
music = []
folders = []
archives = []
other = []
unknown = []
extensions = []

registered_extensions = {
    "JPEG": images,
    "PNG": images,
    "JPG": images,
    "SVG": images,
    "AVI": videos,
    "MP4": videos,
    "MOV": videos,
    "MKV": videos,
    "TXT": documents,
    "DOCX": documents,
    "DOC": documents,
    "PDF": documents,
    "XLSX": documents,
    "PPTX": documents,
    "MP3": music,
    "OGG": music,
    "WAV": music,
    "AMR": music,
    "ZIP": archives,
    "GZ": archives,
    "TAR": archives,
}

reserved_folders = ("IMAGES", "VIDEOS", "DOCUMENTS", "MUSIC", "OTHER", "ARCHIVES")

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in reserved_folders:
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            other.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                other.append(new_name)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan(arg)

    print(f"Found images: {images}\n")
    print(f"Found videos: {videos}\n")
    print(f"Found documents: {documents}\n")
    print(f"Found music: {music}\n")
    print(f"Found archives: {archives}\n")
    print(f"Unknowns: {other}\n")
    print(f"All extensions: {extensions}\n")
    print(f"Unknown extensions: {unknown}\n")
    



def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    
    path_search = path.name.rfind('.')
    
    position = path.name[(path_search):]
   
    new_name = normalize(path.name.replace(position,''))
    
    archive_folder = target_folder/ new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(path.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass

def main(folder_path):
    scan.scan(folder_path)

    for file in images:
        hande_file(file, folder_path, "IMAGES")

    for file in videos:
        hande_file(file, folder_path, "VIDEOS")

    for file in documents:
        hande_file(file, folder_path, "DOCUMENTS")

    for file in music:
        hande_file(file, folder_path, "MUSIC")

    for file in other:
        hande_file(file, folder_path, "OTHER")

    for file in archives:
        handle_archive(file, folder_path, "ARCHIVES")

    get_folder_objects(folder_path)
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    file_generator(arg)
  


   

if __name__ == '__main__':
   main(arg.resolve())



