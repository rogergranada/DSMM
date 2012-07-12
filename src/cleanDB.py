#!/usr/bin/python
#-*- coding: utf-8 -*-

import pymongo
from pymongo import Connection
 
def main():
	connection = Connection('localhost')
	db = connection['banktest']
	connection.drop_database('collection')

if __name__ == "__main__":
	main()
