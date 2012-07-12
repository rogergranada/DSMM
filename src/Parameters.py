#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, getopt, os

class Parameters:

	def __init__(self, argv):
		self.hostname = 'localhost'
		self.port = '27017'
		self.language_1 = ''
		self.language_2 = ''
		self.type_corpus = 'doc'
		self.dbname = ''
		self.collection = ''
		self.inputfile_1 = ''
		self.inputfile_2 = ''
		self.inputfolder = ''

		try:
			opts, args = getopt.getopt(argv,\
				"h:p:l:t:", \
				["hostname=", "port=", "language", "usage", "help", "type"])
		except getopt.GetoptError:
			self.usage()
			sys.exit(2)
		for opt, arg in opts:
			if opt in ('-h', '--hostname'):
				self.hostname = arg
			elif opt in ('-p', '--port'):
				self.port = arg
			elif opt in ('-l', '--language'):
				list_languages = arg.split('-')
				if len(list_languages) != 2:
					print '\nError: Languages must be informed in a pair such as \'en-fr\''
					sys.exit(2)
				else:
					self.language_1, self.language_2 = list_languages
			elif opt in ('-t', '--type'):
				self.type_corpus = arg
			elif opt in ('--help', '--usage'):
				self.usage()
				sys.exit(0)

		if len(args) < 3:
			print 'Error: Missing arguments.'
			self.usage()
		else:
			self.dbname = args[0]
			self.collection = args[1]
			if os.path.isdir(args[2]): 
				if (args[2])[-1] == '/':
					self.inputfolder = args[2]
				else:
					self.inputfolder = args[2]+'/'
			else:
				if os.path.isfile(args[2]): self.inputfile_1 = args[2]
				else: print 'Error: Unvalid input file.'	
				if os.path.isfile(args[3]): self.inputfile_2 = args[3]
				else: print 'Error: Unvalid input file.'		

	def __del__(self):
		pass

	def getHostname(self):
		return self.hostname

	def getPort(self):
		return self.port

	def getLanguage(self):
		return self.language_1, self.language_2

	def getDBName(self):
		return self.dbname

	def getCollection(self):
		return self.collection

	def getInputFile_1(self):
		return self.inputfile_1

	def getInputFile_2(self):
		return self.inputfile_2

	def getInputFolder(self):
		return self.inputfolder

	def getType(self):
		return self.type_corpus

	def usage(self):
		usage = """
   Usage: python foo.py [OPTION] <DBNAME> <CORPUS> <[FILE_1] [FILE_2]> <[INPUT_FOLDER]>\n
   [INPUT]
      DBNAME :       Name of the database
      CORPUS :       Name of the corpus
      FILE_1 :       Input file pre-processed by WebAligner
      FILE_2 :       Input file pre-processed by WebAligner
      INPUT_FOLDER : Folder containing the corpus

   [OPTIONS]
      -h  --hostname=            Hostname to connect in MongoDB (default: localhost)
      -p  --port=                Port to connect in MongoDB (default: 27017)
      -l  --language=            Language of the documents (ex: 'en-fr')
      -t  --type=                Type of corpus ['doc'|'par'|'sen'] (default: 'doc')
   """
		print usage 
