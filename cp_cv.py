import os
import sys
import csv
from optparse import OptionParser
import fnmatch
import platform

## please edit this id you are using and IDE and have not way to pass command line arguments!!
COLLUMNS = "1,2,3"

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def get_coll(row_num,ifile):
	with open(ifile, 'rU') as csvfile:
		spamreader = csv.reader(csvfile, dialect=csv.excel_tab)
		colls = []
		for idx,row in enumerate(spamreader):
			colls.append(row[0].split(',')[row_num - 1])
		return colls

def created_output_files(file_name,input_cols):
	to_read = map(int,input_cols.split(','))

	coll_counter = 0

	n = 48
	final_table = [[0] * n for i in range(n)]

	for (index,x) in enumerate(to_read):
		coll_read = get_coll(x,file_name)
		# print coll_read
		for idx,item in enumerate(coll_read):
			if(idx < 8):
				final_table[idx][coll_counter]= item
				# print item
			else:
				final_table[idx-8][coll_counter+1]= item

		coll_counter = coll_counter + 2

	# print final_table
	output_file_name = file_name.split('.')[0] + "output.csv"

	if os.path.exists(output_file_name):
		os.remove(output_file_name)

	ofile  = open(output_file_name, "wb")
	writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	 
	for row in range(0,8):
		writer.writerow(final_table[row])

	ofile.close()





parser = OptionParser()
parser.add_option("-c", "--colls",
                  dest="cols", default='',help="number of colls to extract!!")


(options, args) = parser.parse_args()

if (options.cols==''):
	print "You did not tell me the collumn numbers to extract, e.g -c 1,3,4"
	options.cols = COLLUMNS;
	print "using collumns from the script :)"

files_to_use = find ("NS*.csv",".")
print files_to_use

if(len(files_to_use) == 0):
	print "no NS files found!! Make sure you have NSXXXXXXXX.csv files in the directory before running :("
	sys.exit(0);

for x in files_to_use:
	if(platform.system() != 'Windows'):
		created_output_files(x.split('/')[1],options.cols)
	else:
		created_output_files(x.split('\\')[1],options.cols)

print "script run!!"
