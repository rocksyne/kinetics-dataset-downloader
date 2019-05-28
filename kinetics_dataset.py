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
Date: 		2019.05.23
Email:		rocksyne@gmail.com, castchoi@ynu.ac.kr
Version:	1.0.0
Purpose:	Download Kinetics-600 dataset according to the author guidelines
"""

import argparse
from KineticsDatasetManager import KineticsDatasetManager


# start the application
if __name__ == "__main__":
	
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--destination", type=str, default=None, help="Enter destination of where files should be extracted to")
	ap.add_argument("-t", "--type", type=str, required=True, default=None, help="Enter train, validation or test")
	args = vars(ap.parse_args())

	# instantiate the manager class
	kinetics_manager = KineticsDatasetManager(args["destination"],args["type"])

	kinetics_manager.download_video()






