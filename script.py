import os
import pathlib
import shutil
import zipfile
from data import data
import create_tree


def prepare_paths():
    work_path = pathlib.Path().resolve()
    delivery_path = str(work_path) + '\livraison'
    ibis_to_rename_dir = str(work_path) + '\pre-livraison\ibis_to_rename'
    zip_path = str(work_path) + str('\pre-livraison\ZIP')
    latest_zip_version = str(work_path.parent.absolute()) + str('\LATEST_ZIP_VERSION')
    return work_path, delivery_path, ibis_to_rename_dir, zip_path, latest_zip_version

def edit_file(file):
    with open(file, "r") as f:
        file_data = f.read()
    file_data = file_data.replace('Copyright', 'Ilyess')
    with open(file, "w") as f:
        f.write(file_data)
    f.close()

def rename_files(ibis_to_rename_dir):
    for dir in os.listdir(ibis_to_rename_dir):
        dir_path = str(ibis_to_rename_dir) + str('\\') + str(dir)
        for sub_dir in os.listdir(dir_path):
            old_file_path = str(dir_path) + str('\\') + str(sub_dir) + str("\old_files")
            new_file_path = str(dir_path) + str('\\') + str(sub_dir) + str("\\new_files")
            for file in os.listdir(old_file_path):
                for item in data:
                    for p in item["package"]:
                        if p in file and file.index(p) + len(p) == file.index('.') and sub_dir == item[
                            "internal_name"] and dir.upper() == item['family']:
                            new_file_name = file.replace(item["old_name"], item["new_name"])
                            rename = False
                            if new_file_name != file:
                                try:
                                    os.rename(old_file_path + str('\\') + file,
                                              old_file_path + str('\\') + new_file_name)
                                    rename = True
                                except:
                                    rename = False
                                    print("Error RENAME or MOVE FILE ==> ", file, '!!!  :(')
                                if rename == True:
                                    edit_file(old_file_path + str('\\') + new_file_name)
                                    try:
                                        shutil.move(old_file_path + str('\\') + new_file_name, new_file_path)
                                    except:
                                        print("Error MOVE FILE ==> ", file, ' TO new_files!!!  :(')



def get_latest_zip_files_version(zip_path, latest_zip_version):
    for zip_file in os.listdir(latest_zip_version):
        if (".zip" in zip_file):
            try:
                shutil.copy2(latest_zip_version + str('\\') + zip_file, zip_path)
            except:
                print("ERROR GET THE LATEST ZIP VERISON!!!  :(")


def extract_latest_zip_files_version(zip_path):
    for dir in os.listdir(zip_path):
        if (".zip" in dir):
            try:
                zip_file_path = zip_path + str("\\") + dir
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(zip_path)
                os.remove(zip_file_path)
            except:
                print(" ERROR EXTRACT ZIP FILE !!!    :(")


def move_new_files(ibis_to_rename_dir, zip_path):
    for dir in os.listdir(ibis_to_rename_dir):
        dir_path = str(ibis_to_rename_dir) + str('\\') + str(dir)
        for sub_dir in os.listdir(dir_path):
            new_file_path = str(dir_path) + str('\\') + str(sub_dir) + str("\\new_files")
            for file in os.listdir(new_file_path):
                moved = False
                for zip_dir in os.listdir(zip_path):
                    if dir.upper() in zip_dir.upper():
                        same = False
                        for f in os.listdir(zip_path+"\\"+str(zip_dir)):
                            if f == file:
                                same = True
                                rep = input(file+" is already exist. Are you sure to save new version?(yes/no):")
                                while rep.upper() != "YES" and rep.upper() != "NO":
                                    rep = input(file+" is already exist. Are you sure to save new version?(yes/no):")
                                if rep.upper() == "YES":
                                    try:
                                        os.remove(zip_path + "\\" + str(zip_dir) + "\\" + file)
                                        moved = True
                                        shutil.move(new_file_path + str('\\') + file, zip_path + str('\\') + zip_dir)

                                    except:
                                        print("ERROR REMOVE OR MOVE " + file + " FROM/TO ZIP FOLDER !!!    :(")
                                else:
                                    try:
                                        os.remove(new_file_path + str('\\') + file)
                                    except:
                                        print("ERROR REMOVE " + file + " FROM NEW NAME !!!    :(")
                        if same == False:
                            try:
                                shutil.move(new_file_path + str('\\') + file, str(zip_path) + str('\\') + str(dir))
                                moved = True
                            except:
                                print("ERROR MOVE NEW " + file + " TO ZIP FOLDER !!!    :(")

                if moved == False:
                    create_tree.create(str(zip_path) + str('\\') + str(dir))
                    try:
                        shutil.move(new_file_path + str('\\') + file, str(zip_path) + str('\\') + str(dir))
                        moved = True
                    except:
                        print("ERROR MOVE NEW " + file + " TO ZIP FOLDER !!!    :(")


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def compress_dirs(zip_path, delivery_path):
    for zip_dir in os.listdir(zip_path):
        if (".zip" not in zip_dir):
            with zipfile.ZipFile(delivery_path + str('\\') + zip_dir + '.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipdir(zip_path + str('\\') + zip_dir, zipf)


def latest_zip_version_delivery(delivery_path, latest_zip_version):
    for file in os.listdir(delivery_path):
        shutil.copy2(delivery_path + "\\" + file, latest_zip_version)


def remove_extra_dirs(dir_path):
    for dir in os.listdir(dir_path):
        shutil.rmtree(dir_path + str('\\') + dir)


def remove_old_running_dirs(dir_path, dir_name):
    for dir in os.listdir(dir_path):
        if dir.count('_') == 2 and dir != dir_name:
            d = dir.split('_')
            if d[0].isdigit() and len(d[0]) <= 2 and d[1].isdigit() and len(d[1]) <= 2 and d[2].isdigit() and len(
                    d[2]) >= 4:
                shutil.rmtree(str(dir_path) + str('\\') + str(dir))

def move_directories(source_dir, destination_dir):
    for root, dirs, files in os.walk(source_dir):
        for directory in dirs:
            source_directory_path = os.path.join(root, directory)
            destination_directory_path = source_directory_path.replace(source_dir, destination_dir)
            shutil.move(source_directory_path, destination_directory_path)

        for file in files:
            source_file_path = os.path.join(root, file)
            destination_file_path = source_file_path.replace(source_dir, destination_dir)
            shutil.move(source_file_path, destination_file_path)


if __name__ == '__main__':
    print("SCRIPT STARTED ...")
    print("CREATED FOLDERS TREE ...")
    dir_name = create_tree.create_forlders()
    print("RENAME PROCESS STARTED ...")
    work_path, delivery_path, ibis_to_rename_dir, zip_path, latest_zip_version = prepare_paths()
    rename_files(ibis_to_rename_dir)
    print("ZIP PROCESS STARTED ...")
    get_latest_zip_files_version(zip_path, latest_zip_version)
    extract_latest_zip_files_version(zip_path)
    move_new_files(ibis_to_rename_dir, zip_path)
    move_directories(zip_path, delivery_path)
    # move_new_files(ibis_to_rename_dir, delivery_path)
    #compress_dirs(zip_path, delivery_path)
    # latest_zip_version_delivery(delivery_path, latest_zip_version)
    #remove_extra_dirs(zip_path)
    #remove_old_running_dirs(work_path.parent, dir_name)
    print("******** ZIP finished **********")
    print("******** SCRIPT FINISHED **********")
# DEFAULT ZIP NAME: en.stm32g0_ibis REPLACE g0 , c0 , etc
