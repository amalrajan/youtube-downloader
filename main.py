import pafy
import sys
import os
import re


class Main:

    def __init__(self):
        self.silent = False
        self.audio_only = False
        self.video_only = False
        self.best_quality = False
        self.data = sys.argv
        self.regular_url = "https?://www.youtube.com/"

        self.analyze_input()

    def analyze_input(self):
        if "--audio" in self.data:
            self.audio_only = True
        elif "--video" in self.data:
            self.video_only = True

        if "single" in self.data:
            self.download_single()
        elif "multiple" in self.data:
            self.download_multiple()
        else:
            self.download_comments()

    def video_description(self, url):
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

    def list_streams(self):
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
        if not re.match(self.regular_url, self.data[2]):
            print("Invalid URL. Execution terminated.")
            sys.exit(1)

        self.video_description(self.data[2])
        self.list_streams()


app = Main()
