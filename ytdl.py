import pafy


class Downloader:

    def __init__(self):
        print("YouTube Downloader 0.1.1")
        print("========================")
        print()
        print("1. Single FIle Download", "\t", "2. Batch Files Download\n")
        while True:
            self.choice = input()
            if self.choice not in ('1', '2'):
                print("Invalid input. Choose again:\n")
            else:
                break
        eval({"1": "self.download_single()", "2": "self.download_multiple()"}[self.choice])

    def download_single(self):
        pass

    def donwload_multiple(self):
        pass

app = Downloader()
