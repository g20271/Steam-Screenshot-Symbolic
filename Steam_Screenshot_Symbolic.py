#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

if os.name == 'nt':
    import win32com.client
    
    # ショートカットを作る
    def win32_create_shortcut(target_path, shortcut_path):
        shell = win32com.client.Dispatch("WScript.shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = target_path
        shortcut.Save()


appids=[]
names=[]
users=[]


try:
    with open('config.txt', mode='x') as f:
        if os.name == 'posix':
            steaminstdir = os.getenv('HOME')+'/.steam/steam'
            shortcutmode = 0
        elif os.name == 'nt':
            steaminstdir = os.getenv('HOMEDRIVE')+'/Program Files (x86)/Steam'
            shortcutmode = 1
        
        text = ('#ショートカットで作成する場合は1にしてください(Windowsのみの設定)\n'
                +str(shortcutmode)+'\n'
                '#以下にSteamがインストールされたディレクトリを入力してください(一行のみ)\n'
                +steaminstdir+'\n'
                '#以下にsteamappsを別の場所に置いている場合は追加で入力してください(複数行可)\n'
                '#例:/home/akatorih0913/.steam/steam/steamapps\n')
        
        f.write(text)
except FileExistsError:
    pass


shortcutmode = -1
steaminstdir=''
steamappsdirs=[]

f = open('config.txt', 'r')
line = f.readline()

while line:
    if not line[0:1] == '#':
        if shortcutmode == -1:
            shortcutmode = int(line.strip())
        elif steaminstdir == '':
            steaminstdir = line.strip()
            steamappsdirs.append(line.strip()+'/steamapps/')
        else:
            steamappsdirs.append(line.strip()+'/')
    line = f.readline()
f.close()



for steamappsdir in steamappsdirs:
    for file in os.listdir(steamappsdir):
        if not (os.path.splitext(file)[1]) == '.acf':continue
        cnt=0
        f = open(steamappsdir+file, 'r')
        line = f.readline()
        
        while line:
            ext = (line.strip()).split('\"')
            if len(ext)<=3:
                line = f.readline()
                continue
            obj = ext[1]
            data = ext[3]
            
            if obj == 'appid':
                appids.append(data)
                cnt+=1
            elif obj == 'name':
                names.append(data)
                cnt+=1
            if cnt == 2:break
            line = f.readline()
        f.close()

for user in os.listdir(): #再構成のための削除
    if (os.path.splitext(user)[1]) == '.lnk':
                os.remove(user)
    if os.path.isdir(user):
        for file in os.listdir(user):
            if os.path.islink(user+'/'+file):
                os.remove(user+'/'+file)
            if (os.path.splitext(user+'/'+file)[1]) == '.lnk':
                os.remove(user+'/'+file)



for user in os.listdir(steaminstdir+'/userdata/'):
    if user == 'ac':continue
    users.append(user)


for user in users:
    if len(users) >= 2:
        os.makedirs(user, exist_ok=True)
    
    for folder in os.listdir(steaminstdir+'/userdata/'+user+'/760/remote/'):
        for appid, name in zip(appids, names):
            if folder == appid:
                if shortcutmode == 0:
                    if len(users) >= 2:
                        os.symlink(steaminstdir+'/userdata/'+user+'/760/remote/'+appid+'/screenshots/', user+'/'+name)
                    else:
                        os.symlink(steaminstdir+'/userdata/'+user+'/760/remote/'+appid+'/screenshots/', name)
                elif shortcutmode == 1:
                    if len(users) >= 2:
                        win32_create_shortcut((steaminstdir+'/userdata/'+user+'/760/remote/'+appid+'/screenshots/').replace('/', os.path.sep), user+'/'+name+'.lnk')
                    else:
                        win32_create_shortcut((steaminstdir+'/userdata/'+user+'/760/remote/'+appid+'/screenshots/').replace('/', os.path.sep), name+'.lnk')
                break
                
