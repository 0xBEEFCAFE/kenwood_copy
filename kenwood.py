#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import itertools
import os
import re
import shutil
import sys
import time

source_dir = "/home/user/Music"
target_dir = "/media/user/WD500GB"
music_extensions = [".flac"] # List of allowed extensions
del_exclude_dirs = ["Video"] # List of directories in the TARGET folder to exclude from deletion

# Leave empty to copy everything from the source_dir, otherwise, specify a list of artists sub-folders to copy
# Note: Larger libraries will choke the Kenwood scan process and may take a long time to resume playback.
artists = []


# Reference specifications for Kenwood DNX691HD
# http://www.kenwood.com/cs/ce/audiofile/index.php?model=DNX691HD&lang=english

maximum_folders = 255 # Per specification
maximum_files_per_folder = 255 # Per specification
maximum_files = maximum_folders * maximum_files_per_folder

# specification is 128, but we want to have some extra chars for handling duplicate
# file names so we can add a " (n)" to the file name, ex: "01 - Some Song.flac" and "01 - Some Song (1).flac"
max_file_name_chars = 120

def DeleteAllSubfolders(path):
	for f in os.listdir(path):
		target = os.path.join(path, f)
		if f not in del_exclude_dirs:
			if os.path.isdir(target):
				shutil.rmtree(target)
			else:
				os.remove(target)
			
def BuildFileList(filenames): # Recursively scan all files/folders in a given directory
	file_list = []
	
	for path in filenames:
		if os.path.isdir(path):
			file_list.extend(BuildFileList([os.path.join(path, f) for f in os.listdir(path)]))
		elif os.path.isfile(path):
			_, ext = os.path.splitext(path)
			if ext.lower() in music_extensions:
				file_list.append(path)
				
	return file_list

start = time.time()

print "\n------------- Kenwood Music File Copy Script -------------\n"

print "Source Directory is: %s" % source_dir
print "Target Directory is: %s" % target_dir

sys.stdout.write("\nPlease wait while the source directory is scanned for files...")

artist_folders = ["%s/%s" % (source_dir, artist) for artist in artists]
if artist_folders:
	file_list = BuildFileList(artist_folders)
else:
	file_list = BuildFileList([source_dir])
total_files = len(file_list)
print "Done (%i found)" % total_files

valid_chars = []
valid_chars.append(r"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789")
valid_chars.append(r"- _ ' , . ( ) ! @ # $ % & [ ] = +".replace(" ", "")) # Putting spaces here for easy reading
valid_chars = "".join(valid_chars)

proceed = True
if total_files > maximum_files:
	print "\nWarning: You have %i total files which is greater than the maximum" % total_files
	print "amount of files that Kenwood supports (Max: %i)." % maximum_files
	print "Extra files will not be processed."
	response = raw_input("\nDo you wish to continue? (Y/N) ")
	if response.upper() != "Y":
		proceed = False
	total_files = maximum_files # To allow accurate progress reporting
	
if proceed:
	file_list.sort()

	print "\nThis will delete all data from the target directory (except excluded folders)."
	response = raw_input("Are you sure you want to proceed? (Y/N): ")
	if response.upper() == "Y":
		sys.stdout.write("Deleting all data from the target directory...")
		DeleteAllSubfolders(target_dir)
		print "Done"
		
		dest_dir_count = 0
		overall_progress = 0.0
		
		regex = re.compile(r" \(\d{1,99}\)$", flags=re.IGNORECASE)
		
		groups = itertools.izip_longest(*(iter(file_list),) * maximum_files_per_folder)
		for group in groups:
			dest_dir_count += 1
			if dest_dir_count > maximum_folders:
				break
			
			current_dir = os.path.join(target_dir, str(dest_dir_count))
			os.mkdir(current_dir)
			
			for f in group:
				if f:
					basename = os.path.basename(f)
					old_base = basename
					
					# Replace non-ascii and invalid (for filenames on Windows) characters
					a = []
					replaced = False
					for c in basename:
						if c in valid_chars:
							a.append(c)
						else:
							replaced = True
					basename = "".join(a)
					
					name, ext = os.path.splitext(basename)
					dest_name = os.path.join(current_dir, basename)
					
					# Uncomment to print before/after filesnames
					# if replaced:
						# print "%s -> %s" % (old_base, basename)
					
					
					
					# The full path from the root of the destination drive, ex: /1/01 - Song.flac
					# Need to make sure the full path of the file on the destination drive
					# is not more than the character limit
					dest_dir = os.path.split(current_dir)[1]
					resulting_name = os.path.join(dest_dir, basename)
					length = len(resulting_name)
					if length > max_file_name_chars:
						name = name[0:max_file_name_chars-length]
						dest_name = os.path.join(current_dir, "%s%s" % (name, ext))
					
					
					while os.path.exists(dest_name):
						if not regex.search(name):
							basename = "%s (1)%s" % (name, ext)
						else:
							first = name.split("(")
							number = int(first[1].split(")")[0])
							number += 1
							basename = "%s(%i)%s" % (first[0], number, ext)
							
						dest_name = os.path.join(current_dir, basename)
					
					overall_progress += 1
					percent_progress = overall_progress / total_files * 100
					shutil.copy2(f, dest_name)
					print "Copied %i/%i %.2f%%" % (overall_progress, total_files, percent_progress)
					print "\tfrom: %s" % f
					print "\tto:   %s" % dest_name
					
				
		print "Done! Total time elapsed: %s" % str(datetime.timedelta(seconds=(time.time() - start)))