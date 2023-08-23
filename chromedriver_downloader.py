
import zipfile
from os import remove, getcwd, path, popen
from shutil import move, rmtree
import urllib.request


def extract_version(output):
    try:
        google_version = ''
        for letter in output[output.rindex('DisplayVersion    REG_SZ') + 24:]:
            if letter != '\n':
                google_version += letter
            else:
                break
        return(google_version.strip())
    except TypeError:
        return


def download(google_version):
    try:
        session = requests.Session()
        workdir = getcwd()

        url = f'https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{google_version}'
        version_response = session.get(url).text
        download_url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{version_response}/win32/chromedriver-win32.zip"
        urllib.request.urlretrieve(download_url, "chromedriver.zip")

        ## if you want to use rquests instead of using urllib.request use following code
        ## import requests
        # download_file = session.get(download_url)
        # with open(f"{workdir}/chromedriver.zip", "wb") as f:
        #     f.write(download_file.content)

        with zipfile.ZipFile("chromedriver.zip") as zip_file:
            zipname = zip_file.namelist()[0].split('/')[0]
            zip_file.extractall(".")

        remove("chromedriver.zip")
        ## try to remove old chromedriver.exe file from the directory
        try:
            remove('chromedriver.exe')
        except:
            pass
        # Get the path to the chromedriver-win32 folder
        chrome_folder = path.join(workdir, zipname)
        # Get the path to the chromedriver.exe file
        chromedriver_path = path.join(chrome_folder, "chromedriver.exe")
        # Copy the chromedriver.exe file to the current working directory
        move(chromedriver_path, workdir)
        try:
        ## clean the directory
        # Delete the chromedriver-win32 folder
            rmtree(f"{workdir}/{zipname}")
        except OSError as e:
            print(e)

        return True
    except Exception as e:
        print('download_chromedriver failed', e)
        return False
    

def chromedriver_downloader():
    try:
        stream = popen('reg query "HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome"')
        output = stream.read()
        google_version = extract_version(output).split('.')[0]
        download(google_version)
    except Exception as e:
        print('chromedriver_downloader failed', e)
        return False


if __name__ == '__main__':
    try:
        chromedriver_downloader()
    except Exception as e:
        print('main error', e)
        input('')
