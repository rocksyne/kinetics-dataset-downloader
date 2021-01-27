# Kinetics Dataset Downloader

Kinetics-400/600/700 is a large-scale high-quality dataset of YouTube video URLs which includes a diverse range of human focused actions.


# Warn·ing! This work comes with no warranty!

This script downloads the Kinetics-400, 600 or 700 dataset according to author guidelines at https://deepmind.com/research/open-source/kinetics. The original paper can be found at https://arxiv.org/pdf/1705.06950.pdf. This script downloads only ~10 second long clips using the provided youtube video ID. Some videos may be absent because they may have been taken off YouTube or be restricted because of copyright issues.


# Pre·req·ui·sites ( dependencies )

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


# Us·age
```
python kinetics_dataset.py -v [400 / 600 / 700] -t [train / validate / test] -d ~/Documents/datasets/kinetics_dataset/
```
eg. python kinetics_dataset.py -v 400 -t train -d ~/Documents/Kinetics_dataset

Command Line Parameters
* `-v`: The version of the Kinetics dataset to be downloaded, Kinetics400,Kinetics600 or Kinetics700
* `-t`: The split category to be downloaded, such as train, validate or test 
* `-d`: Final destintion where all videos should be dwonloaded and saved to. A directory is automatically created in this destination folder according to the parameter of `-t`

From the above exampple, the final destination folder may look like
```
 |~/Documents/Kinetics_dataset
   |-- train
   |-- validate
   |-- test
```
 
