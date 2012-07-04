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
		root, dirs, files = os.walk(input_folder+''+language_1+'/').next()[:3]
	except IOError:
		print 'ERROR: It was not possible to open the '+input_folder+'en/ folder'
		sys.exit(2)
		
	for corpus_file in files:
		#if (corpus_file ~ "/~/$"):
		if not '.txt~' in corpus_file:
			print 'Working on file: '+corpus_file
			id_file_1 = language_1+'_'+corpus_file[0:-4]
			id_file_2 = language_2+'_'+corpus_file[0:-4]

			try:
				file_1 = codecs.open(input_folder+''+language_1+'/'+corpus_file, 'r', 'utf-8')
			except IOError:
				print 'ERROR: System cannot open the '+root+''+corpus_file+' file'
				sys.exit(2)
			try:
				file_2 = codecs.open(input_folder+''+language_2+'/'+corpus_file, 'r', 'utf-8')
			except IOError:
				print 'ERROR: System cannot open the '+root+'../'+language_2+'/'+corpus_file+' file'
				sys.exit(2)
	
			#Sentences indexed by the number of the line : number_line = _id (sentence)
			line_number = 1
			lines_2 = file_2.readlines()
			content_1 = ''
			content_2 = ''
			for counter, line in enumerate(file_1):
				if re.match('(^<)', line):
					if content_1 != '' and content_2 != '':
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
						content_1 = ''
						content_2 = ''
					if (line_number % 100 == 0):
						print 'Indexing line: ',line_number
				else:
					content_1 += line
					content_2 += lines_2[counter]
	
		file_1.close()
		file_2.close()
					

if __name__ == "__main__":
	main(sys.argv[1:])
	#python indexEuroparl.py -l en-fr -t par dsm_corpora europarl /home/granada/Desktop/europarl/

#{ 
#	"_id" : ObjectId("4ff43edcd2daea753d000000"), 
#	"files" : { 
#		"en" : [ { "content" : "Adoption of the Minutes of the previous sitting\n", "_id" : 1 },    
#				 { "content" : "The Minutes of yesterday' s sitting have been distributed.\n", "_id" : 2 },    
#				 { "content" : "Are there any comments?\n", "_id" : 3 },
#				 { "content" : "Mr President, I respond to an invitation yesterday afternoon.\nI refer to item 11 on the order of business.\n", "_id" : 4 },   
#		], 
#		"fr" : [ { "content" : "Adoption du procès-verbal de la séance précédente\n", "_id" : 1 },
#				 { "content" : "Le procès-verbal de la séance d'hier a été distribué.\n", "_id" : 2 },
#				 { "content" : "Y a-t-il des observations ?\n", "_id" : 3 },
#				 { "content" : "Monsieur le Président, je réponds à une invitation lancée hier.\nJe veux parler du point 11 de l'ordre des travaux.\n", "_id" : 4 },
#		], 
#		"id_file_en" : "en_ep-00-01-18", 
#		"id_file_fr" : "fr_ep-00-01-18" 
#	}, 
#	"parallel" : "par" 
#}		
