import sys
import requests
import zipfile
import os

link = "https://codeload.github.com/Khudyakov1/mods_installer/zip/refs/heads/mods"
file_name = "mods.zip"
with open(file_name, "wb") as f:
    print("Downloading mods")
    response = requests.get(link, stream=True)
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

print("\nUnpacking mods")
with zipfile.ZipFile(file_name, 'r') as zip_ref:
    zip_ref.extractall("./")

os.rename("mods_installer-mods", "mods")

