import os, sys, requests, shutil, json, pandas as pd
from colorama import Fore; from zipfile import ZipFile; from collections import namedtuple;

hbaRepo = 'https://wiiu.cdn.fortheusers.org/repo.json'
hbaCDN = 'https://wiiu.cdn.fortheusers.org/zips/'
hbaDL = 'https://wiiu.cdn.fortheusers.org/zips/appstore.zip'
aromaUpdater = 'https://github.com/thegamershollow/hbl-apps/releases/download/aromaUPD/AromaUpdater.wuhb'
aromaPackages = 'https://aroma.foryour.cafe/api/download?packages=bloopair,wiiload,ftpiiu,sdcafiine,screenshotplugin,swipswapme,environmentloader,wiiu-nanddumper-payload'
nuspliPKG = 'https://github.com/V10lator/NUSspli/releases/download/v1.131/NUSspli-1.131-Aroma.zip'
aromaBase = 'https://github.com/wiiu-env/Aroma/releases/download/beta-14/aroma-beta-14.zip'
oscURL = 'https://api.oscwii.org/v2/primary/packages'
oscCDN = 'https://hbb1.oscwii.org/hbb/'
compaturl = 'https://github.com/thegamershollow/vwii-compat-installer/releases/download/v1.0/vwii-compat-installer.wuhb'
d2x = 'https://hbb1.oscwii.org/hbb/d2x-cios-installer/d2x-cios-installer.zip'
ios80 = 'https://hbb1.oscwii.org/hbb/Patched_IOS80_Installer_for_vWii/Patched_IOS80_Installer_for_vWii.zip'

# download function with status        
def download(url: str, fileName: str):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    length = response.headers.get('content-length')
    block_size = 1000000  # default value
    if length:
        length = int(length)
        block_size = max(4096, length // 20)
    filesize = length*10**-6
    filesize = round(filesize, 2)
    print(Fore.BLUE+f"{fileName}"+Fore.RESET+' size: '+Fore.CYAN+f"{filesize} MB"+Fore.RESET)
    with open(fileName, 'wb') as f:
        size = 0
        for buffer in response.iter_content(block_size):
            if not buffer:
                break
            f.write(buffer)
            size += len(buffer)
            if length:
                percent = int((size / length) * 100)
                print(Fore.RESET+"Downloading "+Fore.BLUE+f"{fileName}"+': '+Fore.CYAN+f"{percent}%", end='\r')
    print(Fore.GREEN+"\n\nDone Downloading: "+Fore.CYAN+f"{fileName}"+Fore.RESET+'\n')

# json decoder function
def jsonDecoder(jsonDict):
    return namedtuple('x', jsonDict.keys())(*jsonDict.values())

# base homebrew check function
def nohb():
    noWIIU = os.path.isdir(sd+'/wiiu')
    if noWIIU != True:
        print(Fore.RED+'please download the base homebrew apps before downloading anything else')
        sys.exit(5)

#*main function
os.system('clear')
sdPath = ''
sdVerify = os.path.isfile('.sdpath')
if sdVerify != True:
    giveSdPath = input('Please specify the path of your '+Fore.CYAN+'Wii U'+Fore.RESET+' SD Card: ')
    f = open('.sdpath','w')
    giveSdPath = giveSdPath.replace("'","")
    f.write(giveSdPath)
    f.close
    sdPath = giveSdPath
f = open('.sdpath','r')
sd = f.read()
f.close
sdPath = os.path.isdir(sd)
if sdPath != True:
    print(Fore.RED+'Please reinsert the SD Card and try again')
    sys.exit(1)

# prompt for the whole program
prompt = input('\033[1;37mWii U SD Card Setup Tool\n\033[0;0mType the number of the corrasponding option that you want to select.\n\n\033[1;37m1. '+Fore.CYAN+'Download/Update'+Fore.RESET+' base SD Card files\n2. '+Fore.CYAN+'Download/Update'+Fore.RESET+' Wii U Homebrew Apps\n3. '+Fore.CYAN+'Download/Update'+Fore.RESET+' files needed for vWii mod\n4. '+Fore.CYAN+'Download/Update'+Fore.RESET+' Wii Homebrew\n5. '+Fore.BLUE+'Remove all files'+Fore.RESET+' from Wii U SD Card\n6. Use a diffrent SD card\n7. '+Fore.RED+'Exit'+Fore.RESET+'\n\n\033[0;0mOption: ')

#*Download/Update Base Homebrew Files
if prompt == '1':
    os.system('clear')
    # changes directory to cache
    os.chdir(sd)
    # downloads the Homebrew appstore and extracts the zip file
    if os.path.isdir(sd+'/wiiu/apps/appstore') != True:
        hba = download(hbaDL,'appstore.zip')
        hba = ZipFile('appstore.zip','r')
        hba.extractall()
        hba.close
    pkgs = os.path.isdir(sd+'/wiiu/apps/appstore/.get/packages')
    if pkgs != True:
        os.mkdir(sd+'/wiiu/apps/appstore/.get/packages')
    hba = os.path.isdir(sd+'/wiiu/apps/appstore/.get/packages/appstore')
    if hba != True:
        os.mkdir(sd+'/wiiu/apps/appstore/.get/packages/appstore')
        shutil.move(sd+'/manifest.install',sd+'/wiiu/apps/appstore/.get/packages/appstore')
        shutil.move(sd+'/info.json',sd+'/wiiu/apps/appstore/.get/packages/appstore')
    os.remove(sd+'/appstore.zip')
    # downloads the aroma packages and extracts the zip file
    if os.path.isdir(sd+'/wiiu/environments') != True:
        aPKG = download(aromaPackages, 'aromapkgs.zip')
        aPKG = ZipFile('aromapkgs.zip','r')
        aPKG.extractall()
        aPKG.close
        os.remove(sd+'/aromapkgs.zip')
    # downloads the base files for aroma and extracts the zip file
        aroma = download(aromaBase, 'aroma.zip')
        aroma = ZipFile('aroma.zip','r')
        aroma.extractall()
        aroma.close
        os.remove(sd+'/aroma.zip')
    # downloads nuspli wuhb and extracts the zip file
    if os.path.isdir(sd+'/wiiu/apps/nuspli') !=True:
        os.mkdir(sd+'/wiiu/apps/nuspli')
        os.chdir(sd+'/wiiu/apps/nuspli')
        nuspli = download(nuspliPKG, 'nuspliPKG.zip')
        nuspli = ZipFile('nuspliPKG.zip')
        nuspli.extractall()
        nuspli.close
        os.remove(sd+'/wiiu/apps/nuspli/nuspliPKG.zip')
    if os.path.isdir(sd+'/wiiu') != False:
        print(Fore.GREEN+'\nFinished downloading the '+Fore.CYAN+'base SD Card Files.'+Fore.RESET+'\n')
    else:
        print(Fore.RED+'\nThe '+Fore.CYAN+'base SD Card Files'+Fore.RED+' are already installed, please choose a diffrent option.\n'+Fore.RESET)
        sys.exit(1)

#*Download/Update Wii U Homebrew Apps
if prompt == '2':
    os.system('clear')
    nohb
    # opens the repo.json file located at: https://wiiu.cdn.fortheusers.org/repo.json
    repo = requests.get(hbaRepo)
    jsonSrc = repo.text
    pkg = json.loads(jsonSrc, object_hook=jsonDecoder)
    count = 0
    pkgTotal = pkg.packages.__len__()
    # create an empty list
    allPkg = []
    # iterate through items in json file
    for items in pkg.packages.__iter__():
        allPkg.append(pkg.packages[count])
        count = count+1
    allPkg = sorted(allPkg)
    # converts list into a printable pkgTable
    pkgTable = pd.DataFrame(allPkg)
    pkgTable.drop(columns=["binary", "title", "license", "url", "changelog", "screens", "extracted", "details", "md5", "description"],inplace=True,)
    pkgTable = pkgTable.reindex(columns=["name", "author", "category", "version", "filesize"])
    pkgTable.rename(columns={"category": "Category", "version" : "Version", "filesize" : "Download Size(KB)", "app_dls" : "App Downloads", "author" : "Author", "updated" : "Update Date","name" : "App Name"},inplace=True,)
    print(pkgTable.to_string())
    # asks for input of what app/s you want to download
    hbSelect = input('Type the app/s name/ to download it '+Fore.LIGHTCYAN_EX+'**if multiple are selected this process will take a lot longer**'+Fore.RESET+'\n\nSeperate the app names with commas if you want to download multiple apps at once.\n\nSelection: '); hbSelect = hbSelect.split(',')
    apps = pkgTable['App Name'].values.tolist()
    os.chdir(sd)
    pkgPath = os.path.isdir(sd+'/wiiu/apps/appstore/.get/packages')
    if pkgPath != True:
        os.mkdir(sd+'/wiiu/apps/appstore/.get/packages')
    # downloads the homebrew apps specified in hbSelect
    for item in hbSelect:
        if item in apps:
            if os.path.isdir(sd+'/wiiu/apps/'+item) != True:
                dlURL = hbaCDN+item+'.zip'
                dl = download(dlURL,item+'.zip')
                dl = ZipFile(item+'.zip')
                dl.extractall()
                dl.close
                print('Copied '+Fore.CYAN+item+Fore.RESET+' to the SD card\n')
                dlPath = os.path.isdir(sd+'/wiiu/apps/appstore/.get/packages/'+item)
                if dlPath != False:
                    os.remove(sd+'/manifest.install')
                    os.remove(sd+'/info.json')
                if dlPath != True:
                    os.mkdir(sd+'/wiiu/apps/appstore/.get/packages/'+item)
                    shutil.move(sd+'/manifest.install',sd+'/wiiu/apps/appstore/.get/packages/'+item)
                    shutil.move(sd+'/info.json',sd+'/wiiu/apps/appstore/.get/packages/'+item)
                os.remove(sd+'/'+item+'.zip')
            else:
                print(Fore.YELLOW+'SKIPPING '+item+' Because it is already installed on the SD Card!'+Fore.RESET)
    print(Fore.GREEN+'Finished downloading app/s')

#*Download/Update vWii mod files
if prompt == '3':
    os.system('clear')
    nohb
    if os.path.isfile(sd+'/wiiu/apps/vwii-compat-installer.wuhb') != True:
        os.chdir(sd)
        os.chdir(sd+'/wiiu/apps/')
        compat = download(compaturl, 'vwii-compat-installer.wuhb')
        os.chdir(sd)
        d2xdl = download(d2x, 'd2x.zip')
        d2xdl = ZipFile('d2x.zip')
        d2xdl.extractall()
        ios80dl = download(ios80, 'ios80.zip')
        ios80dl = ZipFile('ios80.zip')
        ios80dl.extractall()
        os.remove(sd+'/ios80.zip')
        os.remove(sd+'/d2x.zip')
        print(Fore.GREEN+'Finished downloading the '+Fore.CYAN+'vWii Mod Files'+Fore.RESET)
    else:
        print(Fore.RED+'\nThe'+Fore.CYAN+'vWii Mod Files'+Fore.RESET+' are already installed, please choose a diffrent option.\n')

#*Download/Update VWii Homebrew Apps
if prompt == '4':
    os.system('clear')
    nohb
    oscApi = requests.get(oscURL)
    jsonFRMT = '{\n     "packages":'
    after = '}'
    jsonSrc = f'{jsonFRMT}{oscApi.text}'
    jsonSrc = jsonSrc.replace(']',' ]')
    jsonSrc += after
    osc = json.loads(jsonSrc, object_hook=jsonDecoder)
    count = 0
    oscTotal = osc.packages.__len__()
    allOSC = []
    for items in osc.packages.__iter__():
        allOSC.append(osc.packages[count])
        count = count+1
    allOSC = sorted(allOSC)
    oscTable = pd.DataFrame(allOSC)
    apps = oscTable['internal_name'].values.tolist()
    oscTable.drop(columns=["downloads", "extra_directories", "icon_url", "rating", "release_date", "shop_title_id", "shop_title_version", "long_description", "updated", "zip_size", "display_name", "package_type"],inplace=True,)
    oscTable = oscTable.reindex(columns=["internal_name", "category", "version", "short_description", "coder"])
    oscTable.rename(columns={"internal_name":"App Name","category":"Catergory","version":"Version","short_description":"Decription","coder":"Author"},inplace=True,)
    f = open('text.txt','w')
    f.write(oscTable.to_string())
    print(oscTable.to_string())
    oscSelect = input('Type the app/s name/ to download it '+Fore.LIGHTCYAN_EX+'**if multiple are selected this process will take a lot longer**'+Fore.RESET+'\n\nSeperate the app names with commas if you want to download multiple apps at once.\n\nSelection: '); oscSelect = oscSelect.split(',')
    os.chdir(sd)
    oscPath = os.path.isdir(sd+'/apps')
    if oscPath != True:
        os.mkdir(sd+'/apps')
    for item in oscSelect:
        if item in apps:
            if os.path.isdir(sd+'/apps/'+item) != True:
                dlURL = oscCDN+item+'/'+item+'.zip'
                dl = download(dlURL,item+'.zip')
                dl = ZipFile(item+'.zip')
                dl.extractall()
                dl.close
                print('Copied '+Fore.CYAN+item+Fore.RESET+' to the SD card\n')
                #dlPath = os.path(sd+'/wiiu/apps/appstore/.get/packages/'+item)
                os.remove(sd+'/'+item+'.zip')
            else:
                print(Fore.YELLOW+'SKIPPING '+item+' Because it is already installed on the SD Card!'+Fore.RESET)
    print('\n'+Fore.GREEN+'Finished downloading app/s')
    

#*Delete all files from SD card
if prompt == '5':
    os.system('clear')
    warn=input(Fore.RED+'*⚠️WARNING⚠️* '+Fore.RESET+'This will delete/remove all files from the SD card\nContinue (Y/N):\n')
    if warn == 'Y' or warn == 'y' or warn == 'yes' or warn == 'Yes':
        shutil.rmtree(sd, ignore_errors=True)
        os.system('exit')
        sys.exit()
    sys.exit()

#*Use a different sd card
if prompt == '6':
    os.system('clear')
    os.remove('.sdpath')
    print('Please restart the app for changes to take effect.')

#*Exit program
if prompt == '7':
    os.system('exit')
    sys.exit()