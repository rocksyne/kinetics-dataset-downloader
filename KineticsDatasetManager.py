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
Version:	1.2.0 (Current)
Purpose:	Manage daownload of kinetics dataset according to author guidelines

* Download dataset from https://deepmind.com/research/open-source/open-source-datasets/kinetics/


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


REFS:
https://www.ostechnix.com/20-ffmpeg-commands-beginners/
https://stackoverflow.com/q/22766111/3901871
https://ffmpeg.org/ffmpeg-utils.html#toc-Examples
"""


# import the libraries we need
import os, sys
from natsort import natsorted
from tqdm import tqdm as tqdm
import shutil


# Class begins
class KineticsDatasetManager(object):

	# constructor
	def __init__(self,destination_path=None,dataset_type=None):
		
		self.destination_path = destination_path
		self.dataset_type = str(dataset_type).lower()

		# the dataset type can never be empty
		if self.dataset_type is None:
			sys.exit("Please provide the category of dataset [train,validate,test] ")


		# we need to make sure that the destination path really exists
		# if it doesnt, we will need to create a temp one in this current working dir
		if self.destination_path is None:
			self.destination_path = os.path.join(os.getcwd(),"Kinetics_dataset",str(dataset_type))
			print("")
			print("Destination directory defaulted to '",self.destination_path,"'")
			print("")

		else: self.destination_path = os.path.join(self.destination_path,str(dataset_type))


		# chek if destination exists. if it does, delete and create new one
		if os.path.exists(self.destination_path):
			user_input = input("Destination path '{}' already exists. Do you want to delete and recreate it? y or n: ".format(self.destination_path))
			print("")

			if str(user_input).lower() == 'y':
				print("Deleting and re-creating {}...".format(self.destination_path))
				print("")
				shutil.rmtree(self.destination_path)
				os.makedirs(self.destination_path)

			elif str(user_input).lower() == 'n':
				print("Keeping '{}' as the default...".format(self.destination_path))
				print("")

			else:
				print("Invalid {} option. Program exiting!".format(user_input))
				sys.exit()

		else:
			os.makedirs(self.destination_path)
			print("")
			print("Destination path '{}' created successfully!".format(self.destination_path))
			print("")
	



	# return the list of all split files in the dir that
	# that matches the split version number
	"""
		This code will need some working on. For now we are not able to download only a component the youtube datase
		So what we shall do is, download each video and use post processing to crop out the part of the video we need
		Thats just the hard way out for now

		-- To do --
		[ref: https://github.com/ytdl-org/youtube-dl/issues/622#issuecomment-162337869]
	"""
	# provide range of downloads. Default is everything
	def download_video(self,start_from=1,end_at=-1):

		# lets make sure that the range we are providin
		# this code needs cleaning. kindly make a pull request if you can help
		def download_data_range(csv_location: str, dataset_type: str) -> dict:
			with open(csv_location,"r") as opened_csv:
				lines = opened_csv.readlines()
				lines = [line.rstrip('\n') for line in lines]
				lines = lines[1:] # trim out the label


				# hold out dataset does not have labelling
				# so we need to be careful about
				if dataset_type!="holdout":
					lines = [line.split(",")[0] for line in lines] # get all the labels

					print("List of data set classes available for download")
					print("-----------------------------------------------")
					print("")
					# now create a dictionary of the
					# first element
					indexing_holder = {}
					start_point = end_point =  0
					unique_element_counter = 1
					for index_,element_ in enumerate(lines[:]):
						
						# variable to hold the last previous element
						previous_element = lines[index_-1]

						# however, if this is the first element, then previous = first
						if index_ == 0:
							previous_element = lines[0]

						# if this curent element is the same as the previous one
						# extend the end point
						if lines[index_] == previous_element:
							end_point = index_

							# if we have reached the last element in the the array, 
							# then set the stop point at this index
							if index_ == (len(lines)-1): 
								end_point = index_
								print(unique_element_counter,". ",lines[index_])

								# dictionary format: [id] ---> saves [class_name,index_start_point,index_end_point]
								indexing_holder[unique_element_counter] = [lines[index_],start_point,end_point] # store the values in a dictionary
								unique_element_counter +=1

						# else if the curent element is different from the previous
						# then let this index be the starting point of the new bath and
						# let the prevoius index be the stop point of the previous batch 
						else:
							#print(lines[index_-1]," {} - {}".format(start_point,end_point ))
							element_ = lines[index_-1]
							end_point = index_-1
							print(unique_element_counter,". ",element_)

							# dictionary format: [id] ---> saves [class_name,index_start_point,index_end_point]
							indexing_holder[unique_element_counter] = [element_,start_point,end_point]
							unique_element_counter +=1
							start_point = index_

					# pretty printing
					print("")

					# return the dictionary
					return indexing_holder

				# -- to do: implement for when downloading holdout dataset
				else:
					sys.exit("holdout data set has not been implemented yet")
							
			# -- END --



		if self.dataset_type == "train":
			csv_location = "./dataset_splits/kinetics_600/kinetics_train.csv"

		elif self.dataset_type == "validate":
			csv_location = "./dataset_splits/kinetics_600/kinetics_val.csv"

		elif self.dataset_type == "test":
			csv_location = "./dataset_splits/kinetics_600/kinetics_600_test.csv"

		elif self.dataset_type == "holdout":
			csv_location = "./dataset_splits/kinetics_600/kinetics_600_holdout_test.csv"

		else:
			sys.exit("Invalid dataset category type. Please enter [train,validate,test]")


		download_data_range = download_data_range(csv_location,self.dataset_type)



		"""
		***********************************************************************************************
		*************************** EVERY BIT OF CODE BELOW NEEDS SOME CLEANING UP ********************
		************************ FOR NOW JUST MAKE SURE YOU ENTER THE RIGHT COMMANDS ******************
		***********************************************************************************************
		"""

		# ask user to enter the range of the dataset they want to download
		user_input = str(input("Please choose a range of the dataset classes you want to download, eg. 1 or 1-100: "))
		print()

		# now some validation
		# trim out all spaces
		user_input = user_input.replace(" ","")

		# now check to see if a single number is given or a range is provided
		user_input = user_input.split("-")

		#print(user_input)

		if len(user_input)>2:
			sys.exit("Sorry. Please provide the correct range such as eg. 1 or 1-100. Program will exit now")


		elif len(user_input)==1:
			if isinstance(int(user_input[0]), (int)) is False or user_input[0]=='':
				sys.exit("Sorry. Please provide the correct range such as eg. 1 or 1-100. Program exiting now")

			user_input = int(user_input[0])

			# ensure the right range
			if user_input<=0 or user_input>len(download_data_range):
				sys.exit("Sorry. Please provide the correct range such as eg. 1 or 1-100. Program exiting now")


			start_from = download_data_range[user_input][1]
			end_at = download_data_range[user_input][2]+1
			print("Downloading videos of '{}' only.".format(download_data_range[user_input][0]))
			#print(start_from, " --> ",end_at  )
			print("")


		elif len(user_input)==2:
			if isinstance(int(user_input[0]), (int)) is False or isinstance(int(user_input[1]), (int)) is False or user_input[0]=='' or user_input[1]=='':
				sys.exit("Sorry. Please provide the correct range such as eg. 1 or 1-100. Program exiting now")

			from_class = int(user_input[0])
			to_class = int(user_input[1])

			# ensure the right range
			if from_class>=to_class or from_class<=0 or to_class<=0 or from_class>len(download_data_range) or to_class>len(download_data_range):
				sys.exit("Sorry. Please provide the correct range such as eg. 1 or 1-100. Program exiting now")


			start_from = download_data_range[from_class][1]
			end_at = download_data_range[to_class][2]+1
			print("Downloading videos from class '{}' to '{}'".format(download_data_range[from_class][0],download_data_range[to_class][0]))
			#print(start_from, " --> ",end_at  )
			print("")


		#number may not be right but just give us a rough estimate	
		video_counter = 0

		# open the file
		with open(csv_location,"r") as opened_csv:
			lines = opened_csv.readlines()
			lines = [line.rstrip('\n') for line in lines]

			# since the first line is just headings,
			# we will chop that part off
			lines = lines[1:]
			sp = "./"

			# loop through the lines to downlad the videos
			for line in tqdm(lines[start_from:end_at]):
				coumn = str(line).split(",")

				# there is no label for holdout data
				if self.dataset_type == "holdout":
					data_lable = "all_data"
					youtube_id = coumn[0]
					start_time = coumn[1]

				else:
					data_lable = coumn[0]
					youtube_id = coumn[1]
					start_time = coumn[2]
				
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
					os.system("ffmpeg -hide_banner -ss "+start_time+" -i $(youtube-dl -f 18 --get-url "+youtube_link+") -t 10 -c:v copy -c:a copy '"+vid_path+"'")
					video_counter +=1
					print(video_counter, " videos downloaded")
					
				else:
					print("Skipped: ",vid_path)		

