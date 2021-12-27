import sys
import requests
import zipfile
import os
import shutil

def donwload_and_extract(url, folder):
    file_name = "tmp.zip"
    with open(file_name, "wb") as f:
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                print("\r[%s%s]" % ('=' * done, ' ' * (50-done)), end="")

    tmp_dir = ".\\tmp\\"
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(tmp_dir)
    all_subdirs = [d for d in os.listdir(tmp_dir) if os.path.isdir(tmp_dir + d)]
    for dirs in all_subdirs:
        root_src_dir = tmp_dir + dirs
        root_dst_dir = folder
        for src_dir, dirs, files in os.walk(root_src_dir):
            dst_dir = src_dir.replace(root_src_dir, folder, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    if os.path.samefile(src_file, dst_file):
                        continue
                    os.remove(dst_file)
                shutil.move(src_file, dst_dir)
    shutil.rmtree(".\\tmp")

print("Input the \".minecraft\" folder location, leave blank to use default: ", end="")
location = input()
location.strip()
if not len(location):
    location = os.getenv('APPDATA') + "\\.minecraft"
if location.find(".minecraft") == -1:
    location = location + "\\.minecraft"
if not os.path.isdir(location):
    print("Folder not found")
    exit()

link = "https://codeload.github.com/Khudyakov1/mods_installer/zip/refs/heads/mods"
file_name = "mods.zip"
# with open(file_name, "wb") as f:
#     print("Downloading mods")
#     response = requests.get(link, stream=True)
#     total_length = response.headers.get('content-length')

#     if total_length is None: # no content length header
#         f.write(response.content)
#     else:
#         dl = 0
#         total_length = int(total_length)
#         for data in response.iter_content(chunk_size=4096):
#             dl += len(data)
#             f.write(data)
#             done = int(50 * dl / total_length)
#             print("\r[%s%s]" % ('=' * done, ' ' * (50-done)), end="")

# print("\nUnpacking mods")
# with zipfile.ZipFile(file_name, 'r') as zip_ref:
#     zip_ref.extractall(location)

# shutil.rmtree(location + "\\mods")
# os.rename(location + "\\mods_installer-mods", location + "\\mods")

print("Donwloading mods")
donwload_and_extract(link, location + "\\mods\\")
print("Mods downloaded")
