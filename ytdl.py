import pafy
import os


class Downloader:
    default_config = None
    first_time = True
    flag = True

    def __init__(self):
        print("YouTube Downloader 0.1.1")
        print("========================")
        print()
        print("1. Single File Download", "\t", "2. Batch Files Download\n")
        while True:
            self.choice = input()
            if self.choice not in ('1', '2'):
                print("Invalid input. Choose again:\n")
            else:
                break
        eval({"1": "self.download_single()", "2": "self.download_multiple()"}[self.choice])

        self.url = None
        self.file = None
        self.video = None
        self.choice = None
        self.streams = None
        self.file_path = None
        self.batch_file = None
        self.stream_choice = None
        self.batch_file_path = None
        self.default_configuration = None

    def download_single(self, url=None, default_configuration=None, batch=None):
        if not url:
            self.url = input("\nEnter the URL of the video:\n")
        else:
            self.url = url

        print()
        if not Downloader.first_time or batch:
            self.video_description_mini(self.url, default_configuration)
        else:
            self.video_description(self.url)

    def video_description(self, url):
        self.video = pafy.new(url.strip())
        print("VIDEO DESCRIPTION")
        print("-----------------")
        print("Title    :", self.video.title)
        print("Duration :", self.video.duration)
        print("Rating   :", round(self.video.rating, 2))
        print("Author   :", self.video.author)
        print("Views    :", self.video.viewcount)
        self.stream_lists(self.video)

    def video_description_mini(self, url, default_configuration):
        self.video = pafy.new(url.strip())
        print("[", self.video.title, "]")
        self.stream_lists(self.video, default_configuration)

    def stream_lists(self, video, default_configuration=None):
        self.default_configuration = default_configuration
        if Downloader.first_time:
            print()
            print("Select the stream: ")
            print("-----------------")
            print("1. Regular Streams (choose this if you're not sure)",
                  "2. Audio Streams",
                  "3. Video Streams",
                  "4. OGG Streams",
                  "5. M4 Streams",
                  "10. List all the streams", sep='\n')
            while True:
                self.choice = input("\nEnter your choice:\n")
                if self.choice not in ('1', '2', '3', '4', '5', '10'):
                    print("Invalid input. Choose again.\n")
                else:
                    break
            Downloader.default_config['stream_type'] = self.choice

        else:
            self.choice = Downloader.default_config['stream_type']
            Downloader.flag = False

        eval({"1": "self.stream_regular", "2": "self.stream_audio", "3": "self.stream_video",
              "4": "self.stream_ogg", "5": "self.stream_m4", "10": "self.stream_listall"}[
                 self.choice] + "(video, Downloader.default_config)")

    def stream_regular(self, video, default_configuration=None):
        if Downloader.first_time:
            print("\nAvailable Streams:\n")
            self.streams = video.streams
            for stream in range(len(self.streams)):
                print(stream + 1, ". ", self.streams[stream])
            while True:
                self.stream_choice = input("Enter your choice: ")
                if self.stream_choice not in ('1', '2', '3', '4', '5'):
                    print("Invalid input. Choose again:\n")
                else:
                    break
            self.choice = input("View additional information about the stream? (y/n)\n").lower()
            if self.choice == "y":
                self.stream_view_additional()
            print()
            print("File size: ", round(self.streams[int(self.stream_choice) - 1].get_filesize() / (1024 * 1024), 2),
                  "MB")

            '''
            Asking for location of the video to be saved into.
            '''

            while True:
                self.file_path = input("Enter the file path:\n")
                if os.path.exists(self.file_path):
                    break
                else:
                    self.choice = input("The path doesn't exist. Create a new one? (y/n)")
                    if self.choice:
                        try:
                            os.makedirs(self.file_path)
                        except:
                            print("Operation failed. Couldn't create a new directory. Try again.\n")
                        else:
                            print("Path created successfully.\n")
                    else:
                        continue

                print("File size: ", self.streams[self.stream_choice - 1].get_filesize())
            print()
            self.choice = input("Start download? (y/n)\n").lower()
            if self.choice == 'y':
                self.start_download(self.streams[int(self.stream_choice) - 1], self.file_path, video)
            Downloader.default_config['stream'] = self.stream_choice
            Downloader.default_config['path'] = self.file_path
        else:
            self.streams = video.streams
            self.start_download(self.streams[int(Downloader.default_config['stream']) - 1],
                                Downloader.default_config['path'], video)
            Downloader.first_time = False

    def start_download(self, stream, path, video):
        try:
            self.file = stream.download(filepath=path)
        except:
            print("Couldn't download the requested file: [", video.title, "]\n")

    def stream_view_additional(self):
        pass

    def download_multiple(self):
        while True:
            self.batch_file_path = input("Enter the complete location of the text file: ")
            if self.batch_file_path[-3:] != 'txt':
                print("Invalid input. Make sure you've added the file extension along with it. Try again.\n")
            else:
                break

        with open(self.batch_file_path) as self.batch_file:
            self.url_data = self.batch_file.read().split('\n')

        print()
        print("URL(s) Listed: ")
        print("---------------")
        [print(url) for url in self.url_data]
        print()

        self.choice = input("Use different configurations for each video? (y/n, default:n)").lower()

        if self.choice == 'y':
            for url in self.url_data:
                self.download_single(url)
        else:
            print("Choose the configuration for the first video, "
                  "else all will be downloaded to at least the best quality possible, if not the preferred one.")
            Downloader.default_config =  {"stream_type": None, "stream": None, "path": None}
            self.download_single(self.url_data[0], batch=True)
            if len(self.url_data) > 1:
                Downloader.first_time = False
                for url in range(1, len(self.url_data)):
                    self.download_single(self.url_data[url])


app = Downloader()
