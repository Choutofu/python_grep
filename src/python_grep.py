import sys, os
from multiprocessing import Pool
import codecs
from itertools import *
import time
import argparse

# Set save result file path and name
SAVE_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/' + time.strftime('%Y_%m_%d') + '.txt'

# List file  from Database Folder
def FolderList(database_folder):
	
	dblist = []
	'''
	dir_path = os.path.dirname(os.path.realpath(__file__))
	allPath = dir_path + r"/2014up"
	'''
	for dirPath, dirNames, fileNames in os.walk(database_folder):
		#print dirPath
		#print dirNames
		#print fileNames
		for f in fileNames:
			#print os.path.join(dirPath, f)
			dblist.append(os.path.join(dirPath, f))

	return dblist

# Comparison the string
def search_action(str_and_path):
	key = str_and_path[0]
	file_path = str_and_path[1]
	#search_result = ''

	# Get the file_path content
	with codecs.open(file_path, 'rb') as f:
		data_list = f.read().splitlines()
	for data in data_list:
		if key in data:
			print('[*] {0} in {2} - {1}'.format(key, data, file_path))
			# Save result to file
			with codecs.open(SAVE_FILE_PATH, 'a', 'utf-8') as f:
				f.write(str(data) + '\n')

# Use multiprocessing function
def search_string(database_folder, search_string_file):
	# Get the SheGongKu file paths
	database_file_paths = FolderList(database_folder)
	# Get the search string content
	with codecs.open(search_string_file, 'rb') as f:
		key_list = f.read().splitlines()
	for key in key_list:
		str_and_path = list(zip(repeat(key), database_file_paths))
		with Pool(5) as p:
			p.map(search_action, str_and_path)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="python grep")
	parser.add_argument('-p', '--path', help="database_absolute_folder_path", required=True)
	parser.add_argument('-i', '--input',help="search_string_file", required=True)
	
	args = parser.parse_args()
	'''
	if len(sys.argv) != 3:
		print('Usage:python3 {0} [database_absolute_folder_path] [search_string_file]'.format(sys.argv[0]))
		sys.exit(0)
	'''
	database_folder = args.path
	search_string_file = args.input
	sTime = time.time()
	search_string(database_folder, search_string_file)
	eTime = time.time()
	print('\nIt cost {0} sec'.format((eTime - sTime)))