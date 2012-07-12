#!/usr/bin/python
#-*- coding: utf-8 -*-

# All documents MUST be first aligned by WebAligner

import sys
from collections import OrderedDict
from ParseXml import XML
from Mongo import Mongo
from Parameters import Parameters
 
def main(argv):

	parameters = Parameters(argv)
	hostname = parameters.getHostname()
	port = parameters.getPort()
	dbname = parameters.getDBName()
	language_1, language_2 = parameters.getLanguage()
	collection = parameters.getCollection()
	filexml_1 = parameters.getInputFile_1()
	filexml_2 = parameters.getInputFile_2()
	type_corpus = parameters.getType()

	print 'Using parameters of configuration: '
	print '- Host : ',hostname
	print '- Port : ',port
	print '- Coll : ',collection
	print '- DBase: ',dbname
	print '- XML1 : ',filexml_1
	print '- XML2 : ',filexml_2

	database = Mongo(hostname, dbname, collection)	

	dic_content_1 = OrderedDict()
	parserxml_1 = XML(filexml_1, language_1)
	dic_content_1 = parserxml_1.getContent()
	size_1 = len(dic_content_1)
	del parserxml_1

	dic_content_2 = OrderedDict()
	parserxml_2 = XML(filexml_2, language_2)
	dic_content_2 = parserxml_2.getContent()
	size_2 = len(dic_content_2)
	del parserxml_2
	
	counter = 1
	if size_1 == size_2:
		#As both files come from WebAligner, they must have the same number of documents
		for id_order in dic_content_1:
			id_file_1 = dic_content_1[id_order]['id_file']
			language_1 = dic_content_1[id_order]['language']
			content_1 = dic_content_1[id_order]['content']
			
			id_file_2 = dic_content_2[id_order]['id_file']
			language_2 = dic_content_2[id_order]['language']
			content_2 = dic_content_2[id_order]['content']

			if database.exists(language_1, id_file_1):
				if not database.exists(language_2, id_file_2):
					database.insertInExisting(language_1, id_file_1, language_2, id_file_2, content_2)
			else:
				if database.exists(language_2, id_file_2):
					database.insertInExisting(language_2, id_file_2, language_1, id_file_1, content_1)
				else:
					database.insertNewData(language_1, id_file_1, content_1, language_2, id_file_2, content_2, type_corpus, counter, counter)
			counter += 1
	else:
		#Files have different number of documents, so they are not aligned
		print '\nError: Files not aligned. Please align them with WebAligner.'

if __name__ == "__main__":
	main(sys.argv[1:])
	#python main.py dsm_corpora euronews /home/granada/Desktop/portuguese.xml /home/granada/Desktop/spanish.xml
