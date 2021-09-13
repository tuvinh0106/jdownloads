import json
import re  # nosec
import ipywidgets as widgets  # pylint: disable=import-error
from IPython.display import HTML, clear_output, display  # pylint: disable=import-error
from google.colab import files  # pylint: disable=import-error
from glob import glob
from sys import exit as exx

# Ultilities Methods ==========================================================


def createButton(name, *, func=None, style="", icon="check"):
    import ipywidgets as widgets  # pylint: disable=import-error

    button = widgets.Button(
        description=name, button_style=style, icon=icon, disabled=not bool(func)
    )
    button.style.font_weight = "900"
    button.on_click(func)
    output = widgets.Output()
    display(button, output)


def generateRandomStr():
    from uuid import uuid4

    return str(uuid4()).split("-")[0]


def checkAvailable(path_="", userPath=False):
    from os import path as _p

    if path_ == "":
        return False
    else:
        return (
            _p.exists(path_)
            if not userPath
            else _p.exists(f"/usr/local/sessionSettings/{path_}")
        )


def findProcess(process, command="", isPid=False):
    from psutil import pids, Process  # pylint: disable=import-error

    if isinstance(process, int):
        if process in pids():
            return True
    else:
        for pid in pids():
            try:
                p = Process(pid)
                if process in p.name():
                    for arg in p.cmdline():
                        if command in str(arg):
                            return True if not isPid else str(pid)
                        else:
                            pass
                else:
                    pass
            except:  # nosec
                continue


def runSh(args, *, output=False, shell=False):
    import subprocess
    import shlex  # nosec

    if not shell:
        if output:
            proc = subprocess.Popen(  # nosec
                shlex.split(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            while True:
                output = proc.stdout.readline()
                if output == b"" and proc.poll() is not None:
                    return
                if output:
                    print(output.decode("utf-8").strip())
        return subprocess.run(shlex.split(args)).returncode  # nosec
    else:
        if output:
            return (
                subprocess.run(
                    args,
                    shell=True,  # nosec
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                .stdout.decode("utf-8")
                .strip()
            )
        return subprocess.run(args, shell=True).returncode  # nosec


def accessSettingFile(file="", setting={}):
    from json import load, dump

    if not isinstance(setting, dict):
        print("Only accept Dictionary object.")
        exx()
    fullPath = f"/usr/local/sessionSettings/{file}"
    try:
        if not len(setting):
            if not checkAvailable(fullPath):
                print(f"File unavailable: {fullPath}.")
                exx()
            with open(fullPath) as jsonObj:
                return load(jsonObj)
        else:
            with open(fullPath, "w+") as outfile:
                dump(setting, outfile)
    except:
        print(f"Error accessing the file: {fullPath}.")


def memGiB():
    from os import sysconf as _sc  # pylint: disable=no-name-in-module

    return _sc("SC_PAGE_SIZE") * _sc("SC_PHYS_PAGES") / (1024.0 ** 3)


# Prepare prerequisites =======================================================
def installJDownloader():
    if checkAvailable("/root/.JDownloader/JDownloader.jar"):
        return
    else:
        runSh("mkdir -p -m 666 /root/.JDownloader/libs")
        runSh("apt-get install openjdk-8-jre-headless -qq -y")
        runSh(
            "wget -q http://installer.jdownloader.org/JDownloader.jar -O /root/.JDownloader/JDownloader.jar"
        )
        runSh("java -jar /root/.JDownloader/JDownloader.jar -norestart -h")
        runSh(
            "wget -q https://biplobsd.github.io/RLabClone/res/jdownloader/sevenzipjbinding1509.jar -O /root/.JDownloader/libs/sevenzipjbinding1509.jar"
        )
        runSh(
            "wget -q https://biplobsd.github.io/RLabClone/res/jdownloader/sevenzipjbinding1509Linux.jar -O /root/.JDownloader/libs/sevenzipjbinding1509Linux.jar"
        )

def configTimezone(auto=True):
    if checkAvailable("timezone.txt", userPath=True):
        return
    if not auto:
        runSh("sudo dpkg-reconfigure tzdata")
    else:
        runSh("sudo ln -fs /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime")
        runSh("sudo dpkg-reconfigure -f noninteractive tzdata")
    data = {"timezone": "Asia/Ho_Chi_Minh"}
    accessSettingFile("timezone.txt", data)


# JDownloader =================================================================

Email = widgets.Text(placeholder="*Required", description="Email:")
Password = widgets.Text(placeholder="*Required", description="Password:")
Device = widgets.Text(placeholder="Optional", description="Name:")
SavePath = widgets.Dropdown(
    value="/content/Downloads",
    options=["/content", "/content/Downloads"],
    description="Save Path:",
)


def refreshJDPath(a=1):
    if checkAvailable("/content/drive/"):
        if checkAvailable("/content/drive/Shared drives/"):
            SavePath.options = (
                ["/content", "/content/Downloads", "/content/drive/My Drive"]
                + glob("/content/drive/My Drive/*/")
                + glob("/content/drive/Shared drives/*/")
            )
        else:
            SavePath.options = [
                "/content",
                "/content/Downloads",
                "/content/drive/My Drive",
            ] + glob("/content/drive/My Drive/*/")
    else:
        SavePath.options = ["/content", "/content/Downloads"]


def exitJDWeb():
    runSh("pkill -9 -e -f java")
    clear_output(wait=True)
    createButton("Start", func=startJDService, style="info")


def confirmJDForm(a):
    clear_output(wait=True)
    action = a.description
    createButton(f"{action} Confirm?")
    if action == "Restart":
        createButton("Confirm", func=startJDService, style="danger")
    else:
        createButton("Confirm", func=exitJDWeb, style="danger")
    createButton("Cancel", func=displayJDControl, style="warning")


def displayJDControl(a=1):
    clear_output(wait=True)
    createButton("Control Panel")
    display(
        HTML(
            """
            <h3 style="font-family:Trebuchet MS;color:#4f8bd6;">
                You can login to the WebUI by clicking
                    <a href="https://my.jdownloader.org/" target="_blank">
                        here
                    </a>.
            </h3>
            """
        ),
        HTML(
            """
            <h4 style="font-family:Trebuchet MS;color:#4f8bd6;">
                If the server didn't showup in 30 sec. please re-login.
            </h4>
            """
        ),
    )
    createButton("Re-Login", func=displayJDLoginForm, style="info")
    createButton("Restart", func=confirmJDForm, style="warning")
    createButton("Exit", func=confirmJDForm, style="danger")


def startJDService(a=1):
    runSh("pkill -9 -e -f java")
    runSh(
        "java -jar /root/.JDownloader/JDownloader.jar -norestart -noerr -r &",
        shell=True,  # nosec
    )
    displayJDControl()


def displayJDLoginForm(a=1):
    clear_output(wait=True)
    Email.value = ""
    Password.value = ""
    Device.value = ""
    refreshJDPath()
    display(
        HTML(
            """
            <h3 style="font-family:Trebuchet MS;color:#4f8bd6;">
                If you don't have an account yet, please register
                    <a href="https://my.jdownloader.org/login.html#register" target="_blank">
                        here
                    </a>.
            </h3>
            """
        ),
        HTML("<br>"),
        Email,
        Password,
        Device,
        SavePath,
    )
    createButton("Refresh", func=refreshJDPath)
    createButton("Login", func=startJDFormLogin, style="info")
    if checkAvailable(
        "/root/.JDownloader/cfg/org.jdownloader.api.myjdownloader.MyJDownloaderSettings.json"
    ):
        createButton("Cancel", func=displayJDControl, style="danger")


def startJDFormLogin(a=1):
    try:
        if not Email.value.strip():
            ERROR = "Email field is empty."
            THROW_ERROR
        if not "@" in Email.value and not "." in Email.value:
            ERROR = "Email is an incorrect format."
            THROW_ERROR
        if not Password.value.strip():
            ERROR = "Password field is empty."
            THROW_ERROR
        if not bool(re.match("^[a-zA-Z0-9]+$", Device.value)) and Device.value.strip():
            ERROR = "Only alphanumeric are allowed for the device name."
            THROW_ERROR
        clear_output(wait=True)
        if SavePath.value == "/content":
            savePath = {"defaultdownloadfolder": "/content/Downloads","maxchunksperfile" : 20,"maxsimultanedownloads" : 3,"maxforceddownloads" : 3}
        elif SavePath.value == "/content/Downloads":
            runSh("mkdir -p -m 666 /content/Downloads")
            savePath = {"defaultdownloadfolder": "/content/Downloads","maxchunksperfile" : 20,"maxsimultanedownloads" : 3,"maxforceddownloads" : 3}
        else:
            savePath = {"defaultdownloadfolder": SavePath.value,"maxchunksperfile" : 20,"maxsimultanedownloads" : 3,"maxforceddownloads" : 3}
            
        with open(
            "/root/.JDownloader/cfg/org.jdownloader.settings.GeneralSettings.json", "w+"
        ) as outPath:
            json.dump(savePath, outPath)
        if Device.value.strip() == "":
            Device.value = Email.value
        runSh("pkill -9 -e -f java")
        data = {
            "email": Email.value,
            "password": Password.value,
            "devicename": Device.value,
            "directconnectmode": "LAN",
        }
        with open(
            "/root/.JDownloader/cfg/org.jdownloader.api.myjdownloader.MyJDownloaderSettings.json",
            "w+",
        ) as outData:
            json.dump(data, outData)
        startJDService()
    except:
        print(ERROR)


def handleJDLogin(newAccount):
    installJDownloader()
    if newAccount:
        displayJDLoginForm()
    else:
        data = {
            "email": "thinhplust@gmail.com",
            "password": "1234567890",
            "devicename": "THINHPLUST",
            "directconnectmode": "LAN",
        }
        with open(
            "/root/.JDownloader/cfg/org.jdownloader.api.myjdownloader.MyJDownloaderSettings.json",
            "w+",
        ) as outData:
            json.dump(data, outData)
        startJDService()
# TO DO ===
# Update MAKE BUTTON FUNCTIONS
# FINISH MAKING ICONS
#