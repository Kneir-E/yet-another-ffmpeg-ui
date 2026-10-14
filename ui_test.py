from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
from conf_driver import config as Config
from datetime import datetime
import subprocess
import os

# FFMPEG Location
def set_lib_dir():
    choice = filedialog.askdirectory()
    if choice:
        Config.ffmpeg_dir = choice
        lbl_ffmpeg_dir.config(text=choice)
    elif Config.ffmpeg_dir == '':
        lbl_ffmpeg_dir.config(text="No folder selected")

# Output Location
def set_out_dir():
    choice = filedialog.askdirectory()
    if choice:
        Config.output_dir = choice
        lbl_out_dir.config(text=f"Output Location: {choice}")
    elif Config.output_dir == '':
        lbl_out_dir.config(text="No folder selected")

# Select Inputs
def set_inputs():
    choices = filedialog.askopenfilenames()

    for file in lst_queue.get_children():
        lst_queue.delete(file)

    global var_queue
    if choices:
        var_queue = choices
        for i, file in enumerate(var_queue):
            file_size = os.path.getsize(file)

            if file_size >= 1024**3:
                size = f"{file_size / 1024**3:.2f} GB"
            elif file_size >= 1024**2:
                size = f"{file_size / 1024**2:.2f} MB"
            elif file_size >= 1024:
                size = f"{file_size / 1024:.2f} KB"
            else:
                size = f"{file_size} bytes"

            lst_queue.insert(
                "",
                "end",
                iid=f"file_{i}",
                values=(
                    file,
                    "ready",
                    size
                )
            )

def start_conv():

    btn_convert.config(state="disabled")

    items = var_queue
    if len(items) < 1:
        return

    for i, input_file in enumerate(var_queue): 

        item_no = f"[{i+1}/{len(items)}]"
        filename = input_file.rsplit('/', 1)[-1][:-4]
        output_file = f"{Config.output_dir}/{filename}_1080p.mp4"
        
        start_time = datetime.now()
        print(f"{start_time} --- {item_no} Converting file: {input_file}")

        lst_queue.set(f"file_{i}", column="status", value="Converting")

        command = [
            f"{Config.ffmpeg_dir}/ffmpeg.exe",
            # "-hwaccel", "amf",    #idk why this did not work
            "-i", input_file,
            "-vf", "scale=1920:1080",
            "-c:v", "h264_amf",
            "-rc", "vbr_peak",
            "-b:v", "6M",
            "-maxrate", "10M",
            "-quality", "quality",
            "-c:a", "copy",
            "-y",  # Overwrite file
            output_file
        ]

        try:
            # Run the command and check for errors
            print(command)
            result = subprocess.run(command, check=True, capture_output=True, text=True)

            end_time = datetime.now()
            time_elapsed = end_time - start_time

            print(f"{end_time} --- {item_no} Converted successfully: {input_file}_1080p.mp4 --- Time Elapsed: {time_elapsed}")

            lst_queue.set(f"file_{i}", column="status", value="Finished")
        except subprocess.CalledProcessError as e:
            print(f"Unsuccessful conversion: {input_file}.mp4")
            print(f"Error during conversion:\n{e.stderr}")
        except FileNotFoundError:
            print("FFmpeg is not installed or not added to your system PATH.")

    btn_convert.config(state="enabled")


# -- root --
root = tk.Tk(baseName="batch Conversion GUI via FFMPEG",className="batch Conversion GUI via FFMPEG")
# root.geometry("500x400")
# style = ttk.Style()
# style.theme_use("vista")

frm_main = ttk.Frame(root, padding=15)
frm_main.pack(fill="both", expand=True)

# -- setup --
frm_setup = ttk.LabelFrame(frm_main, text="Step 1 - ffmpeg Setup", padding=15)
frm_setup.pack(fill="x", expand=True)

lbl_ffmpeg_dir = ttk.Label(frm_setup, text=Config.ffmpeg_dir)
lbl_ffmpeg_dir.pack(side="left")

button = ttk.Button(frm_setup, text="Browse", command=set_lib_dir)
button.pack(side="right")

# -- settings --
frm_settings = ttk.LabelFrame(frm_main, text="Step 2 - Video Conversion Settings", padding=15)
frm_settings.pack(fill="x", expand=True)

lbl_out_dir = ttk.Label(frm_settings, text=f"Output Location: {Config.output_dir}")
lbl_out_dir.pack(side="left")
btn_out_dir = ttk.Button(frm_settings, text="Choose Folder", command=set_out_dir)
btn_out_dir.pack(side="right")

# lbl_setting = ttk.Label(frm_settings, text=f"Current Settings: 1080p h264 (can't change for now)")
# lbl_setting.pack(side="left")

# -- conversion --
frm_convert = ttk.LabelFrame(frm_main, text="Step 3 - Convert", padding=15)
frm_convert.pack(fill="x", expand=True)

frm_queue = ttk.Frame(frm_convert, padding=10)
frm_queue.pack(fill="x")

columns = ("file", "status", "size")
var_queue = []
lst_queue = ttk.Treeview(frm_queue, columns=columns, show="headings", selectmode="extended", height=10)
lst_queue.heading("file", text="File")
lst_queue.heading("status", text="Status")
lst_queue.heading("size", text="Size")
lst_queue.column("file", width=200)
lst_queue.column("status", width=75, anchor="center")
lst_queue.column("size", width=75)

scroll = ttk.Scrollbar(frm_queue, orient="vertical", command=lst_queue.yview)
lst_queue.configure(yscrollcommand=scroll.set)
lst_queue.pack(side="left", fill="both",expand=True)
scroll.pack(side="right", fill="y")

btn_add_fil = ttk.Button(frm_convert, text="Add File", command=set_inputs)
btn_add_fil.pack(side="left")
btn_convert = ttk.Button(frm_convert, text="Convert", command=start_conv)
btn_convert.pack(side="right")

root.mainloop()