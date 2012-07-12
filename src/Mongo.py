#!/usr/bin/python
#-*- coding: utf-8 -*-

import pymongo
from pymongo import Connection
 
class Mongo():

	def __init__(self, hostname, dbname, corpus):
		connection = Connection(hostname)
		db = connection[dbname]
		self.collection = db[corpus]
	
	def __del__(self):
		pass

	def insertNewData(self, language_1, id_file_1, content_1, language_2, id_file_2, content_2, type_corpus, counter):
		self.collection.insert({'files':{ 
										 'id_file_'+language_1:id_file_1,
										 'id_file_'+language_2:id_file_2,
										 language_1:[{
													 '_id': counter,
													 'content':content_1,
										 }],
										 language_2:[{
													 '_id': counter,
													 'content':content_2,
										 }],
								},
								'parallel':type_corpus,
		})

	def insertInExisting2(self, language_index, id_file_index, language_update, id_file_update, content_update, line_number):
		self.collection.update({'files.id_file_'+language_index:id_file_index}, {
						   '$set': {'id_file_'+language_update:id_file_update, 
						   			'content_'+language_update:content_update, 
									language_update:[{
												'_id': line_number,
												'content':content_update,
									}],
				 			}
		})

	def insertInExistingSentence(self, language_index, id_file_index, language_update, id_file_update, content_update, line_number):
		self.collection.update({'files.id_file_'+language_index:id_file_index}, {
						   '$push': {'files.'+language_update:{
												'_id': line_number,
												'content':content_update
									}
				 			}
		})

	def insertNewSentence(self, language_index, id_file_index, content_index, language_update, id_file_update, content_update, line_number):
		self.collection.update({'files.id_file_'+language_index:id_file_index}, {
							'$push': {'files.'+language_index:{
												'_id': line_number,
												'content':content_index
									}
				 			}
		})
		self.collection.update({'files.id_file_'+language_index:id_file_index}, {
						   	'$push': {'files.'+language_update:{
												'_id': line_number,
												'content':content_update
									}
				 			}
		})

#db.ted.update({'files.id_file_fr':'train.fr-en.es'},{'$push':{'files.fr':{'_id':2, 'content':'Phrase 2'}}})

		#self.collection.update({'id_file_'+language_index:id_file_index}, {
		#				   '$push': {'lang':language_update,
		#				 }})

	def exists(self, language, id_file):
		query = self.collection.find({'files.id_file_'+language:id_file})
		if query.count() != 0:
			return True
		else:
			return False

	def existsSentence(self, language, id_file, id_sentence):
		query = self.collection.find({'files.id_file_'+language:id_file, 'files.'+language+'._id':id_sentence})
		if query.count() != 0:
			return True
		else:
			return False

	def queryCollection(self, language, id_file):
		query = self.collection.find({'files.id_file_'+language:id_file})
		return query

	def dropDatabase(self, dbname):
		self.connection.drop_database(dbname)
