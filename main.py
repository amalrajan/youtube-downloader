import pafy
import sys
import os
import re

import argparse


class Main:

    def __init__(self):
        self.silent = False
        self.multiple = False
        self.audio_only = False
        self.video_only = False
        self.maxquality = False
        self.filepath = None
        self.best_quality = False
        self.data = sys.argv
        self.regular_url = "https?://www.youtube.com/"

        self.analyze_input()

    def analyze_input(self):
        if "--audio" in self.data:
            self.audio_only = True
        elif "--video" in self.data:
            self.video_only = True

        if "--maxquality" in self.data:
            self.maxquality = True

        if "multiple" in self.data and self.data[2][-3:] != 'txt':
            print("File should have the extension 'txt'. Program terminated.")
            sys.exit(1)

        if "single" in self.data:
            self.download_single()
        elif "multiple" in self.data:
            self.multiple = True
            self.download_multiple()
        else:
            self.download_comments()

    def video_description(self, url):
        if not re.match(self.regular_url, url):
            print("Invalid URL. Execution terminated.")
            sys.exit(1)
        self.video = pafy.new(url.strip())

        self.views = self.video.viewcount
        if self.views >= 1000:
            self.views = "{}k".format(round(self.views/1000, 2))
        elif self.views >= 100000:
            self.views = "{}m".format(round(self.views/100000), 2)

        print("""
        Video Description: 
        ------------------
        Title        : {}
        Author       : {}
        Duration     : {}
        Rating       : {}
        Views        : {} \n""".format(self.video.title, self.video.author,
                                        self.video.duration, round(self.video.rating, 2),
                                        self.views))

        self.list_streams()

    def list_streams(self):
        if self.maxquality:
            self.stream = self.video.getbest()
        else:
            print("\n\tAvailable streams:\n")
            if self.audio_only:
                self.streams = self.video.audiostreams
            elif self.video_only:
                self.streams = self.video.videostreams
            else:
                self.streams = self.video.streams

            print("\t    %5s | %10s" % ("stream", "resolution"))
            print("\t-- + ----- + ----------")

            for index, stream in enumerate(self.streams):
                print("\t%2s    %5s  %10s" % (index, str(stream).split(':')[-1].split('@')[0], 
                    str(stream).split(':')[-1].split('@')[1]))
            print()

            while True:
                try:
                    choice = int(input("Choice? "))
                except KeyboardInterrupt:
                    print("Program terminated.")
                    sys.exit(0)
                except ValueError:
                    print("Invalid input. Trye again.")
                else:
                    if not choice in range(len(self.streams)):
                        print("Invalid input. Try again.")
                    else:
                        self.stream = self.streams[choice]
                        break

        self.ask_file_path()


    def ask_file_path(self):
        while True:
            self.file_path = input("Directory to be saved to: ")
            if os.path.exists(self.file_path):
                break
            else:
                print("The path doesn't exist. Create a new one? (y/n)")
                create_new = input()
                if create_new.lower() == 'y':
                    try:
                        os.makedirs(self.file_path)
                    except:
                        print("Failed to create a new directory.")
                    else:
                        print("Created a new diretory: ", self.file_path)

        self.start_download()

    def start_download(self):
        print("\nFile size: {} MB\n".format(round(self.stream.get_filesize()/1024), 2))

        try:
            self.proceed_request = input("Start download? (Return/Ctrl-C) ")
        except KeyboardInterrupt:
            sys.exit(0)
        else:
            try:
                self.downloaded_file = self.stream.download(filepath=self.file_path)
            except:
                print("Couldn't download the requested file. Program terminated.")
                sys.exit(1)


    def download_single(self):
        self.video_description(self.data[2])

    def download_multiple(self):
        with open(self.data[2]) as self.textfile:
            self.urls = self.textfile.read().split('\n')

        for url in self.urls:
            self.video_description(url)
            print()


app = Main()
