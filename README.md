# YouTube Downloader

_-Yet another tool to download youtube videos (and more, coming soon).-_
 
## Description

Download videos from Youtube using this simple tool, right from the command line. Supports downloading multiple videos.

Contributions are welcome :)


## Installation

```
cd folder_name
git clone https://github.com/amalrajan/youtube-downloader.git
cd youtube-downloader
pip install -U -r requirements.txt
py -3.6 main.py             # or python3 main.py, depeding on how you have Python installed.
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
Example usage:
```
py -3.6 main.py single "https://www.youtube.com/watch?v=aIPqt-OdmS0&list=PLQVvvaa0QuDfV1MIRBOcqClP6VZXsvyZS" -m
```
**Note**: 
* The url and the output directory must be passed within double quotes. 
* While using the 'playlist' mode, it **IS** necessary to give the URL of the first video.


## Requirements
* ~~Python 3x~~
* pafy
* youtube-dl

## Version and Status

`Version 0.4.0`

**Status**: Released the Beta version.


## License
`MIT License`

