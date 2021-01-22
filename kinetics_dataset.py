"""
MIT License

Copyright (c) 2019 Rockson Agyeman & Gyu Sang Choi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Authors:	Rockson Agyeman and Gyu Sang Choi
Date: 		2019.05.23 (first authored)
Email:		rocksyne@gmail.com, castchoi@ynu.ac.kr
Version:	1.2.0
Purpose:	Download Kinetics dataset (400,600 or 700) according to specifications from
		https://deepmind.com/research/open-source/kinetics

Usage: python kinetics_dataset.py -v [400 / 600 / 700] -t [train / validate / test] -d ~/Documents/datasets/kinetics_dataset/

"""

import argparse
from KineticsDatasetManager import KineticsDatasetManager


# start the application
if __name__ == "__main__":
	
	# construct the parse arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--version", type=str, required=True, default=None, help="Enter the version to download, eg. 400, 600 or 700")
	ap.add_argument("-t", "--type", type=str, required=True, default=None, help="Enter the split type, eg. train, validation or test")
	ap.add_argument("-d", "--destination", type=str, default=None, help="Enter destination for download videos")
	
	args = vars(ap.parse_args())

	# instantiate the download manager class
	kinetics_manager = KineticsDatasetManager(args["version"],args["type"],args["destination"],False)

	kinetics_manager.download_video()



