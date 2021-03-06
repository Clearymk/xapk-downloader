import zipfile
import os


def read_file_in_xapk(file_path):
    target_file = []
    if not zipfile.is_zipfile(file_path):
        return False
    with zipfile.ZipFile(file_path, 'r') as xapk_file:
        for apk_file in xapk_file.namelist():
            if apk_file.endswith(".apk") and "config" not in apk_file:
                target_file.append(apk_file)
    if len(target_file) > 1:
        print(target_file)
        stored_path = "G:/apk_pure/xapk/%s" % file_path.split("\\")[-1].split(".")[0]
        if not os.path.exists(stored_path):
            zipfile.ZipFile(file_path, "r").extractall(stored_path)
        return True
    return False


def extract_apks(file_path):
    if not zipfile.is_zipfile(file_path):
        return
    stored_path = "D:/apk_pure/decompress/%s" % file_path.split("\\")[-1].split(".")[0]
    if not os.path.exists(stored_path):
        zipfile.ZipFile(file_path, "r").extractall(stored_path)


if __name__ == "__main__":
    download_path = "D:\\apk_pure\\download"
    count = 0
    for xapk_file in os.listdir(download_path):
        if not xapk_file.endswith(".xapk"):
            continue
        xapk_file_path = os.path.join(download_path, xapk_file)
        extract_apks(xapk_file_path)
        # if read_file_in_xapk(xapk_file_path):
        #     count = count + 1
        #     print(xapk_file_path)
        #     print("------------------------")
        #     print(count)
