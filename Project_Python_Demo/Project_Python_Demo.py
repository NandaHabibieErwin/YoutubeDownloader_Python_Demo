import tkinter as tk
from tkinter import ttk
from pytube import YouTube
import pytube
import threading
import os
import webbrowser
import pathlib

home_directory = pathlib.Path.home()
download_dir = os.path.join(home_directory, "Downloads", "Python Video")

def clear_progress():
    progress_text.config(state=tk.NORMAL)
    progress_text.delete(1.0, tk.END)
    progress_text.config(state=tk.DISABLED)

def download_progress(stream, chunk, remaining):
    total_size = stream.filesize
    downloaded_size = total_size - remaining
    progress_percentage = int((downloaded_size / total_size) * 100)
    progress_text.config(state=tk.NORMAL)
    progress_text.delete(1.0, tk.END)
    progress_text.insert(tk.END, f"Retrieving video...\n")
    progress_text.insert(tk.END, f"File size: {total_size / (1024 * 1024):.2f} MB\n")
    progress_text.insert(tk.END, f"Downloaded: {downloaded_size / (1024 * 1024):.2f} MB\n")
    progress_text.insert(tk.END, f"Progress: {progress_percentage}%\n")
    progress_text.insert(tk.END, f"Saved to {download_dir}%\n")
    progress_text.config(state=tk.DISABLED)
    root.update()

def download_video():
    clear_progress()
    video_url = link.get()
    try:
        yt = YouTube(video_url, on_progress_callback=download_progress)
        stream = yt.streams.get_highest_resolution()
        os.makedirs(download_dir, exist_ok=True)
        stream.download(download_dir)
    except pytube.exceptions.RegexMatchError:
        progress_text.config(state=tk.NORMAL)
        progress_text.insert(tk.END, "Invalid YouTube link.\n")
        progress_text.config(state=tk.DISABLED)
    except pytube.exceptions.VideoUnavailable:
        progress_text.config(state=tk.NORMAL)
        progress_text.insert(tk.END, "Video is unavailable.\n")
        progress_text.config(state=tk.DISABLED)
    except pytube.exceptions.VideoPrivate:
        progress_text.config(state=tk.NORMAL)
        progress_text.insert(tk.END, "Video is private.\n")
        progress_text.config(state=tk.DISABLED)
    except pytube.exceptions.ExtractError:
        progress_text.config(state=tk.NORMAL)
        progress_text.insert(tk.END, "Unable to extract video information.\n")
        progress_text.config(state=tk.DISABLED)
    except pytube.exceptions.RequestError:
        progress_text.config(state=tk.NORMAL)
        progress_text.insert(tk.END, "Unable to establish connection. Please check your internet connection.\n")
        progress_text.config(state=tk.DISABLED)
    except Exception as e:
        progress_text.config(state=tk.NORMAL)
        progress_text.insert(tk.END, f"{str(e)}\n")
        progress_text.config(state=tk.DISABLED)

        
def open_download_directory():
    webbrowser.open(download_dir)
    print(download_dir)

def button_clicked():
    threading.Thread(target=download_video).start()

root = tk.Tk()
root.title("Youtube Downloader")

window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

title_label = tk.Label(root, text="Youtube Video Downloader", font=("Verdana", 16))
title_label.grid(row=0, column=0, columnspan=2, sticky="ew")

subtitle_label = tk.Label(root, text="By Nanda Habibie Erwin", font=("Garamond", 8))
subtitle_label.grid(row=1, column=0, columnspan=2, sticky="ew")

link_placeholder = "Paste YouTube video link here"
link = tk.Entry(root, width=30, fg="gray")
link.insert(0, link_placeholder)
link.bind("<FocusIn>", lambda event: link_on_focus_in(event, link_placeholder))
link.bind("<FocusOut>", lambda event: link_on_focus_out(event, link_placeholder))
link.grid(row=2, column=0, padx=(20, 10), pady=5, sticky="ew")

def link_on_focus_in(event, placeholder):
    if link.get() == placeholder:
        link.delete(0, tk.END)
        link.config(fg="black")

def link_on_focus_out(event, placeholder):
    if not link.get():
        link.insert(0, placeholder)
        link.config(fg="gray")

button = tk.Button(root, text="Download", command=button_clicked)
button.grid(row=2, column=1, padx=(10, 20), sticky="ew")

status = tk.Label(root, text="", font=("Helvetica", 12))
status.grid(row=3, column=0, columnspan=2, )

progress_text = tk.Text(root, height=4, width=50, state=tk.DISABLED)
progress_text.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

open_dir_button = tk.Button(root, text="Open Download Directory", command=open_download_directory)
open_dir_button.grid(row=6, column=0, columnspan=2, pady=3)

root.mainloop()
