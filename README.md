# youtube-downloader
Command line utility to download content from www.youtube.com
 
## Description
Download videos from Youtube using this simple tool, right from the command line. Supports downloading multiple videos.

## Installation
```
git clone https://github.com/amalrajan/youtube-downloader.git
cd youtube-downloader
pip install -r requirements.txt
python main.py
```

## Usage
```
usage: main.py [-h] [-m] [-o OUTPUT] type url

positional arguments:
  type                   single/multiple/playlist
  url                    link to the original video on YouTube, or 
                         complete path to the text file

optional arguments:
  -h, --help             show this message and exit
  -m, --maxquality       download video(s) in the best quality available
  -a, --audio            audio only mode
  -o OUTPUT, --output OUTPUT
                         download location
```

## Requirements
* pafy
* youtube-dl

## Version and Status
`Version 0.4.0`

## License
`MIT License`

