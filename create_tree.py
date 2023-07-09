import os
import pathlib
from datetime import date
from data import cards_infos

def create(dirname):
    try:
        pathlib.Path(dirname).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print(os.path.basename(dirname), "Folder Already exists!")
    else:
        print(os.path.basename(dirname), " Folder was created successfully")

def create_forlders():
    curr_date = date.today()
    dir_name = str(curr_date.day) + '_' + str(curr_date.month) + '_' + str(curr_date.year)
    root_path = pathlib.Path().resolve()
    create(dir_name)
    os.chdir(dir_name)
    create("pre-livraison")
    create("livraison")

    os.chdir("pre-livraison")
    create("ZIP")
    create("ibis_to_rename")
    os.chdir("ibis_to_rename")

    for info in cards_infos:
        create(info['name'])
        os.chdir(info['name'])
        for internal in info['internals']:
            create(internal)
            os.chdir(internal)
            create('old_files')
            create('new_files')
            os.chdir("..")
        os.chdir("..")
    os.chdir("../..")

    return dir_name


def list_files(startpath,dir_name):
    for root, dirs, files in os.walk(startpath):

        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 7 * (level)
        if os.path.basename(root) == dir_name:
            print('{}{}/'.format(indent, os.path.basename(root)))
        else:
            print('{}|__{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 7 * (level + 1)
        for f in files:
            print('{}|_{}'.format(subindent, f))


