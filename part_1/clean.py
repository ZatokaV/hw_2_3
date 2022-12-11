import os
from pathlib import Path
import shutil
import constants as CON
from threading import Thread


def find_images() -> list:
    files = os.listdir(address)
    type_img = (list(
        filter(lambda x: any(
            filter(lambda y: x.lower().endswith(y.lower()),
                   CON.IMAGES)
        ), files)
    ))
    return type_img


def find_video() -> list:
    files = os.listdir(address)
    type_video = (list(
        filter(lambda x: any(
            filter(lambda y: x.lower().endswith(y.lower()),
                   CON.VIDEO)
        ), files)
    ))
    return type_video


def find_docs() -> list:
    files = os.listdir(address)
    type_docs = (list(
        filter(lambda x: any(
            filter(lambda y: x.lower().endswith(y.lower()),
                   CON.DOCS)
        ), files)
    ))
    return type_docs


def find_music() -> list:
    files = os.listdir(address)
    type_mus = (list(
        filter(lambda x: any(
            filter(lambda y: x.lower().endswith(y.lower()),
                   CON.MUSIC)
        ), files)
    ))
    return type_mus


def find_archives() -> list:
    files = os.listdir(address)
    type_arch = (list(
        filter(lambda x: any(
            filter(lambda y: x.lower().endswith(y.lower()),
                   CON.ARCHIVES)
        ), files)
    ))
    return type_arch


def dont_know_files() -> list:
    all_in = find_images()
    all_in.extend(find_video())
    all_in.extend(find_docs())
    all_in.extend(find_music())
    all_in.extend(find_archives())
    files = os.listdir(address)
    type_any = [i for i in files if i not in all_in]
    return type_any


def del_empty_dirs(address: str) -> None:
    for dirs in os.listdir(address):
        new_directory = os.path.join(address, dirs)
        if os.path.isdir(new_directory):
            del_empty_dirs(new_directory)
            if not os.listdir(new_directory):
                os.rmdir(new_directory)


def deep_folders() -> None:
    for el in os.listdir(address):
        way = os.path.join(address, el)
        if os.path.isdir(way):
            files_in_way = os.listdir(way)
            for i in files_in_way:
                shutil.move(os.path.join(way, i), address)
                del_empty_dirs(address)
            if not os.path.isdir(address):
                break
            else:
                deep_folders()


def normalize(filename: str) -> None:
    find_kyrill = [x for x in CON.CYRILLIC_SYMBOLS if x in filename.lower()]
    name_cln = ''
    if len(find_kyrill) > 0:
        result = filename.translate(CON.TRANS)
        for el in result:
            if el.isalpha() or el.isalnum() or el == '.':
                name_cln += el
            if el in CON.SUMB:
                name_cln += el.replace(el, '_')
        old_name = os.path.join(address, filename)
        newname = os.path.join(address, name_cln)
        os.rename(old_name, newname)


def transfer_files(folder_name: str, files: list) -> None:
    if folder_name not in address:
        os.chdir(address)
        os.mkdir(folder_name)
    if folder_name == 'archives':
        to_unpack_folder = os.path.join(address, folder_name)
        os.chdir(to_unpack_folder)
        for arch_name in files:
            named = arch_name.split('.')
            name = named[0]
            os.mkdir(name)
            path_to_unpack = os.path.join(to_unpack_folder, name)
            file_for_unpack = os.path.join(address, arch_name)
            try:
                shutil.unpack_archive(file_for_unpack, path_to_unpack)
                os.remove(file_for_unpack)
            except shutil.ReadError:
                error_name = os.path.split(file_for_unpack)
                del_empty_dirs(os.path.join(address, 'archives'))
                print(f'Файл {error_name[-1]} має розширення архіву, проте не є ним.')
    if folder_name != 'archives':
        file_destination = os.path.join(address, folder_name)
        get_files = files
        for files in get_files:
            shutil.move(os.path.join(address, files), file_destination)


def rename_files() -> None:
    no_type = dont_know_files()

    files = os.listdir(address)
    for file in files:
        if file not in no_type:
            normalize(file)
    print(f'Файли, які через невідоме розширення, залишилися там, де й були: {no_type}')


def relocation_files() -> None:

    t1 = Thread(target=transfer_files, args=('images', find_images()))
    t2 = Thread(target=transfer_files, args=('music', find_music()))
    t3 = Thread(target=transfer_files, args=('video', find_video()))
    t4 = Thread(target=transfer_files, args=('documents', find_docs()))
    t5 = Thread(target=transfer_files, args=('archives', find_archives()))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()


def resume(*args) -> None:
    for name_fold in args:
        way_for_resume = os.path.join(address, name_fold)
        files = os.listdir(way_for_resume)
        count_images = (len(files))
        line_of_ras = []
        for el in files:
            formatting = el.split('.')
            line_of_ras.append(formatting[-1].lower())
        line_of_ras = set(line_of_ras)
        print(
            f'''До папки {name_fold} було відсортовано файли у кількості {count_images} шт.'''
            f'''Їх формати: {line_of_ras}'''
        )
    dop_way = os.path.join(address, 'archives')
    files = os.listdir(dop_way)
    count_ar = (len(files))
    print(
        f'''Також я розпакував архіви, у кількості {count_ar} шт. '''
        f'''Вони тепер у папці 'archives'. '''
    )


def run() -> None:
    deep_folders()
    rename_files()
    relocation_files()
    resume('images', 'video', 'documents', 'music')


if __name__ == '__main__':
    address = input("Введіть шлях до папки...")
    if os.path.exists(address) and Path(address).is_dir():
        run()
    else:
        print('Введено невірний шлях')
