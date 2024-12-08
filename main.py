from yt_dlp import YoutubeDL
from pathlib import Path
from pywebio.input import input
from pywebio.output import put_html, clear, put_processbar, set_processbar, scroll_to
import validators
import time
import tkinter as tk
from tkinter import filedialog

def progress_hook(d):
    """Callback to update the progress bar."""
    if d['status'] == 'downloading':
        # Calculate the progress bar
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', d.get('total_bytes_estimate', 1))
        if total > 0:  # Don't give permission to divide by zero
            progress = downloaded / total
            set_processbar('progress', progress)  # Update bar
    elif d['status'] == 'finished':
        set_processbar('progress', 1)  # Complete bar

def get_download_path():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    folder_selected = filedialog.askdirectory(title="Select Folder")
    return folder_selected

def video_download():
    path_to_download = get_download_path()

    while True:
        # Shows title
        clear()  # Clear main page
        put_html('<h1 style="color: black; font-size: 30px">Video Downloader</h1>')
        
        # Insert link
        video_link = input("Insert the video link (or type 'exit' to quit): ")
        if video_link.lower() == "exit":
            break
        
        # URL validate
        if validators.url(video_link):
            put_html('<p style="color: green; font-size: 25px">Downloading content...</p>')
            
            # Running processbar
            put_processbar('progress') 
            scroll_to('progress')  
            try:
                # Configurações do yt-dlp com hook de progresso
                ydl_opts = {
                    'outtmpl': f'{path_to_download}/%(title)s.%(ext)s',
                    'format': 'best',
                    'progress_hooks': [progress_hook],  # Adiciona o hook
                }
                
                # Baixar vídeo usando yt-dlp
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_link])
                
                # Mensagem de sucesso
                put_html('<h2 style="color: black; font-size: 20px">Video downloaded successfully!</h2>')
                
                # Aguarda 3 segundos antes de limpar a mensagem de sucesso
                time.sleep(3)
                clear()  # Limpa mensagens de sucesso e barra, mantendo a entrada
            except Exception as e:
                put_html(f'<p style="color: red; font-size: 25px">Error: {e}</p>')
        else:
            # URL inválida
            put_html('<p style="color: red; font-size: 25px">Invalid URL!</p>')
            time.sleep(3)
            clear()

if __name__ == "__main__":
    video_download()