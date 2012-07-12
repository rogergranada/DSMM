#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
from xml.dom import minidom
from collections import OrderedDict

class XML():
	""" Output:
		OrderedDict([(u'1', {'id_file': u'50', 'content': u'From infants to industry ... together.', 'language': u'en'}), 
					 (u'2', {'id_file': u'52', 'content': u'Europe\u2019s gambling ... in Reporters.', 'language': u'en'}), 
					 (u'3', {'id_file': u'45', 'content': u'A senior Iraqi ... after the US election.', 'language': u'en'})
					])
	"""
	
	def __init__(self, fileinput, language):

		self.dic_content = OrderedDict()
		listaEstado = []
		print 'Loading XML file...',fileinput
		xmlDoc = minidom.parse(fileinput)
		#dom = minidom.parse( xmlData.encode( "utf-8" ) )
		print 'Building elements...'
		self.element = xmlDoc.getElementsByTagName('file')
		id_order = 1
		for node in self.element:
			file_id = node.getAttribute('id')
			if (language == ''):
				try:
					language_list = node.getElementsByTagName('meta_content-language')
					language = language_list[0].childNodes[0].nodeValue
				except:
					print '\nError: A pair of languages must be informed.'
					sys.exit(2)			
			content_list = node.getElementsByTagName('content')
			content = content_list[0].childNodes[0].nodeValue
			self.dic_content[id_order] = {'id_file':file_id, 'content':content, 'language':language}
			id_order += 1
		#print self.dic_content

	def __del__(self):
		del self.element

	def getContent(self):
		return self.dic_content
