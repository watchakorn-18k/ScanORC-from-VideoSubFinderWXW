#! orc_sub\Scripts\activate.bat

import sys


import tkinter as tk
from tkinter import ttk

import httplib2
import os
import io
import sys
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from pathlib import Path
import threading

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
# Code is based on https://tanaikech.github.io/2017/05/02/ocr-using-google-drive-api/
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_path = os.path.join("./", 'token.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

root = tk.Tk()
big_frame = ttk.Frame(root)
root.title('Scaner-OCR')
root.iconbitmap('scaner-orc.ico')
big_frame.pack(fill="both", expand=True)
root.resizable(width=False, height=False)

#--setting size window--
w = 310
h = 200
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
#--end setting size window--



# Set the initial theme
root.tk.call("source", "sun-valley.tcl")
root.tk.call("set_theme", "dark")


def change_theme():
    # NOTE: The theme's real name is sun-valley-<mode>
    if root.tk.call("ttk::style", "theme", "use") == "sun-valley-dark":
        # Set light theme
        root.tk.call("set_theme", "light")
    else:
        # Set dark theme
        root.tk.call("set_theme", "dark")

# Remember, you have to use ttk widgets
Input1 = ttk.Entry(big_frame)
Input1.insert(0, "Judul episode")
Input1.grid(row=0, column=0, padx=80, pady=(30, 0), sticky="ew")

def orc_word():
    label['text'] = "Membaca..."
    progress.start(1)
    title = Input1.get()
    file_sub = title
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    current_directory = Path(Path.cwd())
    images_dir = Path(f'{current_directory}/RGBImages')
    raw_texts_dir = Path(f'{current_directory}/raw_texts')
    texts_dir = Path(f'{current_directory}/texts')
    srt_file = open(Path(f'{current_directory}/File_srt/{file_sub}.srt'), 'a', encoding='utf-8')
    
# check directory if exists
    if not images_dir.exists():
        images_dir.mkdir()
        print('Images folder is empty.')
        exit()

    if not raw_texts_dir.exists():
        raw_texts_dir.mkdir()
    if not texts_dir.exists():
        texts_dir.mkdir()

    images = Path(f'{current_directory}/RGBImages').rglob('*.jpeg')
    count_round = 0
    count_file_img = len(list(Path(f'{current_directory}/RGBImages').rglob('*.jpeg')))
    for image in images:
        # Get data
        imgfile = str(image.absolute())
        imgname = str(image.name)
        raw_txtfile = f'{current_directory}/raw_texts/{imgname[:-5]}.txt'
        txtfile = f'{current_directory}/texts/{imgname[:-5]}.txt'

        mime = 'application/vnd.google-apps.document'
        res = service.files().create(
            body={
                'name': imgname,
                'mimeType': mime
            },
            media_body=MediaFileUpload(imgfile, mimetype=mime, resumable=True)
        ).execute()


        downloader = MediaIoBaseDownload(
            io.FileIO(raw_txtfile, 'wb'),
            service.files().export_media(fileId=res['id'], mimeType="text/plain")
        )
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        service.files().delete(fileId=res['id']).execute()

        # Create clean text file
        raw_text_file = open(raw_txtfile, 'r', encoding='utf-8')
        text_content = raw_text_file.read()
        raw_text_file.close()
        text_content = text_content.split('\n')
        text_content = ''.join(text_content[2:])
        text_file = open(txtfile, 'w', encoding='utf-8')
        text_file.write(text_content)
        text_file.close()

        start_hour = imgname.split('_')[0][:2]
        start_min = imgname.split('_')[1][:2]
        start_sec = imgname.split('_')[2][:2]
        start_micro = imgname.split('_')[3][:3]

        end_hour = imgname.split('__')[1].split('_')[0][:2]
        end_min = imgname.split('__')[1].split('_')[1][:2]
        end_sec = imgname.split('__')[1].split('_')[2][:2]
        end_micro = imgname.split('__')[1].split('_')[3][:3]

        # Format start time
        start_time = f'{start_hour}:{start_min}:{start_sec},{start_micro}'
        line = 1
        # Format end time
        end_time = f'{end_hour}:{end_min}:{end_sec},{end_micro}'
        # Append the line to srt file
        srt_file.writelines([
            f'{line}\n',
            f'{start_time} --> {end_time}\n',
            f'{text_content}\n\n',
            ''
        ])

        line += 1
        count_round += 1
        count_file_img_left = count_file_img - 1
        print(f"{imgname} pass Line : {count_round} , left {count_file_img_left} lines")
        label['font'] = ("-size", 6, "-weight", "normal")
        progress.stop()
        Allimgdata_percent = (count_round / count_file_img) * 100
        progress['value'] = Allimgdata_percent
        label['text'] = f"{imgname} selesai Baris : {count_round}, tersisa {count_file_img_left} baris   {Allimgdata_percent:.2f} %"

    label['text'] = "Menyelesaikan"
    print("\nFinish Scan File!")
    srt_file.close()
    raise SystemExit

def start_sub():
    return threading.Thread(target=orc_word).start()

accentbutton = ttk.Button(big_frame, text="Konversi Teks", style="Accent.TButton",command=start_sub)
accentbutton.grid(row=5, column=0, padx=80, pady=10, sticky="nsew")

button = ttk.Button(big_frame, text="Penyimpanan",command=lambda: os.startfile('File_srt'))
button.grid(row=6, column=0, padx=(80,80), pady=(0,5), sticky="nsew")

label = ttk.Label(
    big_frame,
    text="Dev-wk18k",
    justify="center",
    font=("-size", 8, "-weight", "bold"),
)
label.grid(row=7, column=0, pady=(5,0), columnspan=1)

progress = ttk.Progressbar(big_frame, mode="determinate")
progress.grid(row=8, column=0, padx=(10, 20), pady=(12, 0), sticky="ew")






root.mainloop()