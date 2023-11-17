#!/usr/bin/env python3

import shutil
from os import scandir, rename
import sys
from os.path import splitext, exists, join
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler



source_dir = "" # Add path to downloads folder or whichever folder you would liek to organize
destinationDir_music = "" # Add destination folder for music
destinationDir_sfx = "" # Add destination folder for sound effects
destinationDir_video = "" # Add destination folder for videos
destinationDir_image = "" # Add destination folder for images
destinationDir_document = "" # Add destination folder for# Add destination folder for documents

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg",".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]  


def make_unique(dest,name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name


def move_file(dest,entry,name):
    source_path = entry.path
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest,name)
        oldName = join(dest,name)
        newName = join(dest,unique_name)
        rename(oldName, newName)
    shutil.move(source_path, dest)    



#This code snippet prints all directories within the given source directory
# with os.scandir(source_dir) as entries:
#     for entry in entries:
#         print(entry)


class Organizer(FileSystemEventHandler):

    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry,name)
                self.check_video_files(entry,name)
                self.check_image_files(entry,name)
                self.check_document_files(entry,name)

    def check_audio_files(self,entry,name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10000000 or "SFX" in name:
                    dest = destinationDir_sfx
                else:
                    dest = destinationDir_music
                move_file(dest,entry,name)
                logging.info(f"Moved audio file: {name}")

    def check_image_files(self,entry,name):
        for image_extension in image_extensions:
            if name.endswith(image_extension):
                move_file(destinationDir_image,entry,name)
                logging.info(f"Moved image file: {name}")

    def check_video_files(self,entry,name):
        for video_extension in video_extensions:
            if name.endswith(video_extension):
                move_file(destinationDir_video,entry,name)
                logging.info(f"Moved video file : {name}")

    def check_document_files(self,entry,name):
        for document_extension in document_extensions:
            if name.endswith(document_extension):
                move_file(destinationDir_document,entry,name)
                logging.info(f"Moved document file : {name}")                                        
                                





if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir 
    # if len(sys.argv) > 1 else '.'
    event_handler = Organizer()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()