# Kinetics Dataset Downloader

Kinetics-600 is a large-scale high-quality dataset of YouTube video URLs which include a diverse range of human focused actions.

## Warning! This scrip is not without bugs!

This script downloads the Kinetics-600 dataset according to author guidelines (https://arxiv.org/pdf/1705.06950.pdf). This script downloads only a 10 second clip using the provided youtube video ID.

# Pre-requisites ( dependencies )

- [X] Environment: Ubuntu 16.04 (This is some-what irrelevant but worth mentioning)

- [X]  Python 3

- [X]  tqdm
```
pip3 install tqdm
```

- [X] youtube-dl
```
sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl
```

- [X] ffmpeg
```
sudo add-apt-repository ppa:jonathonf/ffmpeg-4
sudo apt-get update
sudo apt-get install ffmpeg
```

# Usage
```
python kinetics_dataset.py -t [data_set_categoty] -d [destination_to_where_videos_should_be_downloaded_to]
```
eg. python kinetics_dataset.py -t train -d ~/Documents/Kinetics_dataset

Command Line Parameters
* `-t`: Type of dataset category to be downloaded, such as train, validate, test and holdout
* `-d`: Final destintion where all videos should be dwonloaded to saved. A directory is automatically created in this destination folder according to the parameter of `-t`

From the above exampple, the final destination folder may look like
```
 |~/Documents/Kinetics_dataset
   |-- train
   |-- validate
   |-- test
   |-- holdout
```
 
