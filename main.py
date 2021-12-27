import sys
import requests
import zipfile
import os
import shutil
import json

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
    os.remove(file_name)
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

def get_location():
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
    return location

def append_json(file, append_to, data_name, data_to_write):
    try:
        with open(file) as json_file:
            data = json.load(json_file)
            if data_name not in data[append_to].keys():
                data[append_to][data_name] = data_to_write
    except FileNotFoundError:
        data = {
            "settings" : {
                "crashAssistance" : True,
                "enableAdvanced" : False,
                "enableAnalytics" : True,
                "enableHistorical" : False,
                "enableReleases" : True,
                "enableSnapshots" : False,
                "keepLauncherOpen" : False,
                "profileSorting" : "ByLastPlayed",
                "showGameLog" : False,
                "showMenu" : False,
                "soundOn" : False
            },
            "version" : 3
        }
        data[append_to] = {data_name : data_to_write}
    except json.decoder.JSONDecodeError:
        print("Couldn't add a profile")
        return
    with open(file, 'w') as outfile:
        json.dump(data, outfile)
    print("Profile added")


location = get_location()
link_mods = "https://codeload.github.com/Khudyakov1/mods_installer/zip/refs/heads/mods"
link_versions = "https://codeload.github.com/Khudyakov1/mods_installer/zip/refs/heads/versions"
print("Downloading forge")
donwload_and_extract(link_versions, location + "\\versions\\")
print("Forge downloaded")
print("Downloading mods")
donwload_and_extract(link_mods, location + "\\mods\\")
print("Mods downloaded")
profile_data = {
      "icon" : "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAC4jAAAuIwF4pT92AAAGdWlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNi4wLWMwMDYgNzkuMTY0NzUzLCAyMDIxLzAyLzE1LTExOjUyOjEzICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjIuMyAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIxLTEyLTI3VDE3OjM2OjA4KzAzOjAwIiB4bXA6TWV0YWRhdGFEYXRlPSIyMDIxLTEyLTI3VDE3OjM2OjA4KzAzOjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMS0xMi0yN1QxNzozNjowOCswMzowMCIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDoxMTdjOGZjMC1kYjUyLWU5NGMtODZiNC1jN2VmOGE3YTJmMDQiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDoxNjg1NjE5NC01NDI4LTkyNDktOTFlNy1lY2ViZTM2YjE2NDEiIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDpkNTlkZjFhNS01NDM2LTcyNDYtYjI1OS05ZDAwNTVmZDI3ZmYiIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJzUkdCIElFQzYxOTY2LTIuMSIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOmQ1OWRmMWE1LTU0MzYtNzI0Ni1iMjU5LTlkMDA1NWZkMjdmZiIgc3RFdnQ6d2hlbj0iMjAyMS0xMi0yN1QxNzozNjowOCswMzowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDIyLjMgKFdpbmRvd3MpIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDoxMTdjOGZjMC1kYjUyLWU5NGMtODZiNC1jN2VmOGE3YTJmMDQiIHN0RXZ0OndoZW49IjIwMjEtMTItMjdUMTc6MzY6MDgrMDM6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyMi4zIChXaW5kb3dzKSIgc3RFdnQ6Y2hhbmdlZD0iLyIvPiA8L3JkZjpTZXE+IDwveG1wTU06SGlzdG9yeT4gPHBob3Rvc2hvcDpEb2N1bWVudEFuY2VzdG9ycz4gPHJkZjpCYWc+IDxyZGY6bGk+MEMxOTExQkE3QzM4RUZCNTBBMzIzQkM1NjEyQzhFRUY8L3JkZjpsaT4gPC9yZGY6QmFnPiA8L3Bob3Rvc2hvcDpEb2N1bWVudEFuY2VzdG9ycz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7WeWw3AAAC3ElEQVR4nO1bv4sTQRSeyWaTnNcYTa5XOOUg/0M6rYQUV9ikvCogKFxjd8jdFYJgIRY2lhcQbD0rwdY6cIqlFpdIxBSSTbJzVd68GTK52Z29m+LNV71s5u28fHzvx+4QLoRglFHyHYBvkCeg7HqDe/e3ryuH+NL4fvajsJuSV0AgwHcAvhEI8B2Ab5AnQGmDza2GbUuDllSv1wsNyAV6/MPzETetXYK8AsgTkHcSBKmNx2O46CMdMqTtSpBXAHkCnB+GMN49f2i1bnf/5NI1H14+1i+B1JtbDbg4Gv4Bu9G8fWnV10FeAeQJ0FMAS8iquq6QKmOMsb2j08w+efx3908yyx6DvALIE5CrC/wdT1ZeXydbG7j6D89HmX3IKyAQ4DsA31BqgJZDSnvhnENbNLGGJ8E8+ZzHP0/eY5BXAHkCeJ7DUZwO2J9zmTVf3veM/tHXN2BP/svrNx6YfTD2jk4LOyUirwDyBFxZCrxtqz537yB/w33/RVWwN8VU+W74S9rdT8LpAQiDvALIE1BoCqhr1OesJxsLsCfoq5u3pF1Fwp7+Vu/3aqrsE1KgKJAnwPmtMK78OB2EmBt9EpGC/WynBvbHsxnY30bqjL9YyBSKq2XYKJ27dQTyCggE+A7AN6zbIG59NsA5yxhjcRyDHUUR2KZJUo9rPjfXFLhvRe6RauVNJPKpSwhZN8grgDwBhR6OYtRqNeUzlj0Glv1sNlu5xhYRGhBLWhtOUXpgkFcAeQKMKZC16jPGWLnsllG4U+jA6SFSGdrTwwOwX784lrFoZ7slw68hrwDyBBgHIc510ciPuKIPBgOwW62WcSM8GOlDkhvQILXzCOz452ejR5IkYRBagjwBXJvFrSq/aX5fV8XbbfmauNPpgN3r2R2G2KDf74Pd7XaN60IKIAQCfAfgG9Y1wNQuK5WK1UZJkmQMLTts61GoAQjkCbiy9wE+/pRteuewDuQVQJ6AC+N924pkiOuvAAAAAElFTkSuQmCC",
      "lastUsed" : "2021-12-27T14:47:28.627Z",
      "lastVersionId" : "1.18.1-forge-39.0.8",
      "name" : "Zoomer Kingdoms",
      "type" : "custom"
    }
print("Adding a profile")
append_json(location + '\\launcher_profiles.json', 'profiles', "Zoomer Kingdoms", profile_data)