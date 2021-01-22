"""
MIT License

Copyright (c) 2019 Rockson Agyeman

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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% SOME MORE INFO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Author:		Rockson Agyeman and Gyu Sang Choi
Date: 		2019.05.27 (First Authored)
Email:		rocksyne@gmail.com, castchoi@ynu.ac.kr
Version:	1.4.0 (Current)
Purpose:	Manage daownload of kinetics dataset according to author guidelines

* Download dataset annotations from 
	https://deepmind.com/research/open-source/kinetics
	Link updated on 2021.01.21

						

Version Changes:
----------------
				V 1.0.0 - Beta application
				V 1.0.1 - Stable release
				V 1.1.0 - Added: ability to download videos from a range of classes or from one class
				V 1.2.0 - Added: Check if video already exist. If it does, skip
				V 1.3.0 - Debuged: Provided quotatio marks to cater for file or folder names with special characters such
								   as white space and (). Without this quotation mark, folders had to be created with all 
								   white spaces replaced with _ before ffmpeg considered it to be a valid string 
								   Another flaw was that folder names with () in them were considered invalid strings,
								   thus, were not download. 
				V 1.4.0 (2021.01.21) - Download capability for Kinetics 400 and 700 also
									 - Disable logs from ffmpeg operations
									 - House cleaning on the annotations according to https://deepmind.com/research/open-source/kinetics


References:
	https://www.ostechnix.com/20-ffmpeg-commands-beginners/
	https://stackoverflow.com/q/22766111/3901871
	https://ffmpeg.org/ffmpeg-utils.html#toc-Examples
"""


# import needed libraries
import os, sys
from natsort import natsorted
from tqdm import tqdm as tqdm
import shutil
from collections import Counter


# Download manager class
class KineticsDatasetManager(object):

	# constructor
	def __init__(self,version=None,split_type=None,destination_path=None,show_log=False):
		
		self.destination_path = str(destination_path).strip()
		self.split_type = str(split_type).lower().strip()
		self.version = str(version).strip()
		self.allowed_split_type = ["train","test","validate"]
		self.allowed_version_number = ["400","600","700"]
		self.show_log = show_log
		self.show_log_cmd = "-loglevel quiet"

		if self.show_log is True:
			self.show_log_cmd = ""

		# check the version of the Kinetics to be downloaded. only 3 versions allowed ()
		if (self.version is None) or (self.version not in self.allowed_version_number):
			sys.exit("Please select your kinetics version. Eg, 400, 600 or 700")

		# check the split verions of the Kinetics to be downloaded. only 3 versions allowed
		if (self.split_type is None) or (self.split_type not in self.allowed_split_type):
			sys.exit("Please provide the split category of the dataset [train,validate,test] ")

		# Making sure the destination path has been provided
		# If not, create a temporary one in this current working directory
		if self.destination_path is None:
			self.destination_path = os.path.join(os.getcwd(),"Kinetics_dataset",str(self.split_type))
			print("")
			print("Destination directory defaulted to '",self.destination_path,"'")
			print("")

		else: self.destination_path = os.path.join(self.destination_path,str(self.split_type))


		# Some house cleaning
		# check if destination dir exists. 
		# if it does, prompt user to delete and create new one
		if os.path.exists(self.destination_path):
			print("")
			user_input = input("Destination path '{}' already exists. Do you want to delete and re-create it? y or n: ".format(self.destination_path))
			print("")

			if str(user_input).lower() == 'y':
				print("")
				print("Deleting and re-creating {}...".format(self.destination_path))
				print("")
				shutil.rmtree(self.destination_path)
				os.makedirs(self.destination_path)

			elif str(user_input).lower() == 'n':
				print("")
				print("Keeping '{}' as the default...".format(self.destination_path))
				print("")

			else:
				print("")
				print("Invalid {} option. Program exiting!".format(user_input))
				print("")
				sys.exit()

		else:
			os.makedirs(self.destination_path)
			print("")
			print("Destination path '<{}>' was created successfully!".format(self.destination_path))
			print("")
	



	# provide range of downloads. Default is everything
	def download_video(self,start_from=1,end_at=-1):

		# fetch the list of of videos from the list of csv files
		def fetch_video_list(csv_location: str) -> list:
			with open(csv_location,"r") as opened_csv:
				lines = opened_csv.readlines()
				lines = [line.rstrip('\n') for line in lines]
				lines = lines[1:] # trim out the label
				all_data = lines

				lines = [line.split(",")[0] for line in lines] # get all the labels

				print("")
				print("List of classes available in Kinetics{} {} split dataset".format(self.version,self.split_type))
				print("------------------------------------------------------------------")


				lines = Counter(lines)
				labels = natsorted(lines)

				for count,label in enumerate(labels,start=1):
					print("{}. {} ({:,d} videos)".format(count,str(label).upper(),lines[label]))

				# return the unique labels 
				# and all the data fetched as well
				return labels,all_data

		# -- function ends here
		

		# get the annotation file
		csv_location = "./dataset_splits/kinetics"+str(self.version)+"/"+str(self.split_type)+".csv"

		# get the unique labels as well as all the data
		labels, all_data = fetch_video_list(csv_location)
		classes_to_be_downloaded = []


		"""
		***********************************************************************************************
		*************************** EVERY BIT OF CODE BELOW NEEDS SOME CLEANING UP ********************
		************************ FOR NOW JUST MAKE SURE YOU ENTER THE RIGHT COMMANDS ******************
		***********************************************************************************************
		"""

		# ask user to enter the range of the dataset they want to download
		print("")
		user_input = str(input("Please choose a range of the dataset classes you want to download, eg. 1 or 1-{}: ".format(str(len(labels)))))
		print("")

		# now some validation
		# trim out all spaces
		user_input = user_input.replace(" ","")

		# now check to see if a single number is given or a range is provided
		user_input = user_input.split("-")

		if len(user_input)>2:
			sys.exit("Sorry. Please provide the correct range such as eg. 1 or 1-"+str(len(labels))+". Program will exit now")


		elif len(user_input)==1:
			if isinstance(int(user_input[0]), (int)) is False or user_input[0]=='':
				sys.exit("Sorry. Please provide the correct range such as eg. 1 or 1-"+str(len(labels))+". Program exiting now")

			else:
				val = int(user_input[0])

				# ensure the right range
				if val<=0 or val>len(labels):
					sys.exit("Sorry. Please provide the correct range such as eg. 1 or 1-"+str(len(labels))+". Program exiting now")

				classes_to_be_downloaded = labels[val-1:val]
				print("Downloading videos from the '{}' class only.".format(str(classes_to_be_downloaded[0]).upper()))
				print("")


		elif len(user_input)==2:
			if isinstance(int(user_input[0]), (int)) is False or isinstance(int(user_input[1]), (int)) is False or user_input[0]=='' or user_input[1]=='':
				sys.exit("Sorry. Please provide the correct range such as eg. 1 or 1-"+str(len(labels))+". Program exiting now")

			else:
				from_class = int(user_input[0])
				to_class = int(user_input[1])

				# ensure the right range
				if from_class>=to_class or from_class<=0 or to_class<=0 or from_class>len(labels) or to_class>len(labels):
					sys.exit("Sorry. Please provide the correct range such as eg. 1 or 1-"+str(len(labels))+". Program exiting now")


				classes_to_be_downloaded = labels[from_class-1:to_class]
				print("Downloading videos from class '{}' to '{}'".format(classes_to_be_downloaded[0],classes_to_be_downloaded[-1]))
			
				


		#number may not be right but just give us a rough estimate	
		video_counter = 0

		# this needs cleaning
		# select the candidates for downloading
		candidates = []
		for data in all_data:
			data_lable = str(data).strip().split(',')[0]

			if data_lable in classes_to_be_downloaded:
				candidates.append(data)

				

		# # download the candidate videos
		for candidate in tqdm(candidates):

			data_lable = str(candidate).strip().split(',')[0]
			youtube_id = str(candidate).strip().split(',')[1]
			start_time = str(candidate).strip().split(',')[2]

			# create the directory according to the label name
			dir_name = os.path.join(self.destination_path,str(data_lable)) # make it an absolute path

			# if the directory does not already exist
			# then create a new one
			if os.path.exists(dir_name) is False:
				os.makedirs(dir_name)

			# sample video name
			vid_name = "vid_"+youtube_id+".avi"
			vid_path = os.path.join(dir_name,vid_name)

			# if the video does not exist, then download it
			if os.path.exists(vid_path) is False:

				# create the youtube link
				youtube_link = "https://www.youtube.com/watch?v="+youtube_id
			
				# use youtube-dl and ffmpeg to download videos
				# use quotation to cater for special charaters such as whitesspace and () in file or folder name
				# REF: https://stackoverflow.com/q/22766111/3901871
				# REF: zsnhttps://ffmpeg.org/ffmpeg-utils.html#toc-Examples
				os.system("ffmpeg "+self.show_log_cmd+" -ss "+start_time+" -i $(youtube-dl -f 18 --get-url "+youtube_link+") -t 10 -c:v copy -c:a copy '"+vid_path+"'")
				video_counter +=1
				
			else:
				print("Skipped: ",vid_path)		

