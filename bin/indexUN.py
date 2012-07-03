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
	input_folder = parameters.getInputFolder()
	type_corpus = parameters.getType()

	print 'Using parameters of configuration: '
	print '- Host : ',hostname
	print '- Port : ',port
	print '- Coll : ',collection
	print '- DBase: ',dbname
	print '- Input: ',input_folder

	database = Mongo(hostname, dbname, collection)	
	
	try:
		root, dirs, files = os.walk(input_folder).next()[:3]
	except IOError:
		print 'ERROR: It was not possible to open the '+input_folder+' folder'
		sys.exit(2)
		
	name_folder = (input_folder.split('/'))[-2]
	dic_files = {}
	for corpus_file in files:
		print 'Working on file: '+corpus_file
		if not re.match('~$', corpus_file):
			id_file = corpus_file[0:-7]
			language = corpus_file[-6:-4]
			if not dic_files.has_key(id_file):
				dic_files[id_file] = {'language_1': language}
			else:
				dic_files[id_file]['language_2'] = language

	counter = 1
	for filename in dic_files:
		language_1 = dic_files[filename]['language_1']
		language_2 = dic_files[filename]['language_2']
		id_file_1 = name_folder+'_'+filename+'_'+language_1
		id_file_2 = name_folder+'_'+filename+'_'+language_2

		try:
			file_1 = codecs.open(input_folder+''+filename+'_'+language_1+'.snt', 'r', 'utf-8')
		except IOError:
			print 'ERROR: System cannot open the '+input_folder+''+filename+'_'+language_1+'.snt file'
			sys.exit(2)
		try:
			file_2 = codecs.open(input_folder+''+filename+'_'+language_2+'.snt', 'r', 'utf-8')
		except IOError:
			print 'ERROR: System cannot open the '+input_folder+''+filename+'_'+language_2+'.snt file'
			sys.exit(2)
		
		content_1 = ''
		for line in file_1:
			#if line.strip():
			content_1 += line

		content_2 = ''
		for line in file_2:
			#if line.strip():
			content_2 += line

		if database.exists(language_1, id_file_1):
			if not database.exists(language_2, id_file_2):
				database.insertInExisting(language_1, id_file_1, language_2, id_file_2, content_2)
		else:
			if database.exists(language_2, id_file_2):
				database.insertInExisting(language_2, id_file_2, language_1, id_file_1, content_1)
			else:
				database.insertNewData(language_1, id_file_1, content_1, language_2, id_file_2, content_2, type_corpus, counter)
		counter += 1
	
	#query = database.queryCollection('en', '2000_UNEP_FAO_PIC_INC7_15_en')
	#for ele in query:
	#	print query

if __name__ == "__main__":
	main(sys.argv[1:])
		
