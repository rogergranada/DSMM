#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, codecs, os, re
from collections import defaultdict
from Mongo import Mongo
from Parameters import Parameters

def main(argv):
	parameters = Parameters(argv)
	hostname = parameters.getHostname()
	port = parameters.getPort()
	dbname = parameters.getDBName()
	language_1, language_2 = parameters.getLanguage()
	collection = parameters.getCollection()
	fileinput_1 = parameters.getInputFile_1()
	fileinput_2 = parameters.getInputFile_2()
	type_corpus = parameters.getType()

	print 'Using parameters of configuration: '
	print '- Host : ',hostname
	print '- Port : ',port
	print '- Coll : ',collection
	print '- DBase: ',dbname
	print '- File1: ',fileinput_1
	print '- File2: ',fileinput_2

	database = Mongo(hostname, dbname, collection)	

	id_file_1 = (fileinput_1.split('/'))[-1]
	id_file_2 = (fileinput_2.split('/'))[-1]

	try:
		file_1 = codecs.open(fileinput_1, 'r', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the '+fileinput_1+' file'
		sys.exit(2)
	try:
		file_2 = codecs.open(fileinput_2, 'r', 'utf-8')
	except IOError:
		print 'ERROR: System cannot open the '+fileinput_2+' file'
		sys.exit(2)
	
	line_number = 1

	#Sentences indexed by the number of the line : number_line = _id (sentence)
	lines_2 = file_2.readlines()
	for counter, content_1 in enumerate(file_1):
		content_2 = lines_2[counter]

		if not database.exists(language_1, id_file_1) and not database.exists(language_2, id_file_2):
			database.insertNewData(language_1, id_file_1, content_1, language_2, id_file_2, content_2, type_corpus, line_number)
		else:
			if database.existsSentence(language_1, id_file_1, line_number):
				if not database.existsSentence(language_2, id_file_2, line_number):
					database.insertInExistingSentence(language_1, id_file_1, language_2, id_file_2, content_2, line_number)
			else:
				if database.existsSentence(language_2, id_file_2, line_number):
					database.insertInExistingSentence(language_2, id_file_2, language_1, id_file_1, content_1, line_number)
				else:
					database.insertNewSentence(language_1, id_file_1, content_1, language_2, id_file_2, content_2, line_number)
				
		line_number += 1
	
if __name__ == "__main__":
	main(sys.argv[1:])
	#python indexTed.py -l en-fr -t sen dsm_corpora ted /home/granada/temp/train.fr-en.en /home/granada/temp/train.fr-en.fr		
