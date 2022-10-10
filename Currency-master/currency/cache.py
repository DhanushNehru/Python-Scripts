#!/bin/env python

""" cache module with utility functions to interact with cache file using json format """

import json
import os

def get_cache_path(filename):
	""" get file path """
	cwd = os.path.dirname(os.path.realpath(__file__))
	return os.path.join(cwd, filename)

def read(filename='cache'):
	"""
	parameter: file_path - path to cache file
	return: data after parsing json file"""
	cache_path = get_cache_path(filename)
	if not os.path.exists(cache_path) or os.stat(cache_path).st_size == 0:
		return None
	with open(cache_path, 'r') as file:
		return json.load(file)

def write(content, filename='cache'):
	""" write data to cache file
	parameters:
		cache_path - path to cache file
		content - a data structure to save into cache file"""
	cache_path = get_cache_path(filename)
	with open(cache_path, 'w') as file:
		if content is not None:
			json.dump(content, file, indent=3, sort_keys=True)

def main():
	# path = {$PWD}/cache_example
	cache = read('example_cache') if read('example_cache') is not None else {}
	# do stuff
	cache['key'] = {'key_1': {'key_2': 'value'}}
	cache['another_key'] = {'a_number': 8}
	# ...
	write(cache, 'example_cache')

if __name__ == '__main__':
	main()

# vim: nofoldenable
