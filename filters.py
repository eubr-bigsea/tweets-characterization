#!/usr/bin/python
# -*- coding: utf-8 -*-

# Install PyStemmer
import Stemmer
import re
import string
import unicodedata

def filter_punct (ent):
	''' Remove sinais de pontuaçao STRING --> STRING '''
	punct = re.compile('[%s]' % string.punctuation.replace('#', '').replace('@', ''))  #Tags precisam ser mantidas, bem como @ 
	ent = punct.sub('', ent)
	
	return ent

def filter_charRepetition (ent):
	''' Remover caracteres repetidos em excesso, com o "o" em gooooooooooooooooool STRING --> STRING '''
	expRepeticao1 = re.compile('^([rs])\\1')
	expRepeticao2 = re.compile('([rs])\\1$')
	expRepeticao3 = re.compile('([^rs])\\1{1,}')
	expRepeticao4 = re.compile('([\\S\\s])\\1{2,}')
	
	ent = expRepeticao4.sub('\\1\\1', ent)
	ent = expRepeticao3.sub('\\1', ent)
	ent = expRepeticao2.sub('\\1', ent)
	ent = expRepeticao1.sub('\\1', ent)
	
	return ent
	
def filter_url (ent):
	''' Remove URL STRING --> STRING '''
	urlRef = re.compile("((https?|ftp):[\/]{2}[\w\d:#@%/;\$()~_?\+-=\\\.&]*)")
	
	ent = urlRef.sub('', ent)
	
	return ent

def gen_NGrams(N,text, ignore_stops = True, create_subgrams=True, ngram_sep='', stop_words = []):
	''' Retorna um SET contendo as N-gramas do texto STRING --> SET '''
	NList = [] # start with an empty list
	if N > 1:
		partes = text.split() + (N *[''])
	else:
		partes = text.split()
	# append the slices [i:i+N] to NList
	for i in range(len(partes) - (N - 1) ):
		NList.append(partes[i:i+N])

	result = set()
	for item in NList:
		if create_subgrams:
			list_iterations = xrange(1, N + 1)
		else:
			list_iterations = [N]
		for i in list_iterations:
			stops_found = [x for x in item[0:i] if x in stop_words or x == ""]
			#Ignora N-gramas so com stop words
			dado = ngram_sep.join(item[0:i])
			if ngram_sep.join(stops_found) != dado or ignore_stops == False:
				if dado != ngram_sep:
					result.add(dado)
	return result
	
# Filtra Acentos String --> String
def filter_accents(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def filter_stemmer(words = set([]), lang="pt"):
	'''
	    Invoca a biblioteca que retira de uma palavra todas a partes desnecessárias.
	    
	    @param words: Um set com as palavras para aplicar o stemmer.
	    @return: List com as palavras após o stemmer.
	'''
	
	stemmer = Stemmer.Stemmer(lang) #@UndefinedVariable
	text = []
	for word in words:
		stm = stemmer.stemWord(word)
		if len(stm) > 0:
			text.append(stm.lower())
	return text

def filter_stopwords(gramsSet, use_file=False, stop_words_file='', stop_words=[]):
	''' 
	Filtra Stopwords Set --> Set
	@param gramsSet: Set com palavras a serem filtradas
	@param use_file: Boolean informando se deve ou não ler as stop words de um arquivo
	@return: Set com a diferença entre o set original(gramsSet) e o set de stopwords da lingua informada 
	'''
	if use_file:
		with open(stop_words_file, 'r') as stops_file:
			all_stops = []
			for line in stops_file:
				line = line.strip()
				if type(line) is str:
					line = filter_accents(line.decode('utf8'))
				all_stops.append(line)
	else:
		all_stops = stop_words
	all_stops = set(all_stops)
	return [item for item in gramsSet if item not in all_stops]

def filter_numbers(gramsSet):
	''' Filtra numeros sozinhos Set --> Set '''
	return [item for item in gramsSet if not item.isdigit()]
	
def filter_small_words(gramsSet, min_size):
	''' Filtra termos menores que min_size  set--> Set '''
	return [item for item in gramsSet if len(item)>= min_size]

def __non_empty_container_or_object__(obj):
	if isinstance(obj, dict) or isinstance(obj, tuple) or isinstance(obj, list):
		return len(obj) > 0
	else:
		return True

def __dict_find__(paths, dic):
	if isinstance(dic, list) or isinstance(dic, tuple):
		#Case 1: dic is a list. We search each item recursively
		result = []
		for item in dic: 
			f = __dict_find__(paths, item)
			if __non_empty_container_or_object__(f):
				result.append(f)
		return result
	elif isinstance(dic, dict):
		#Case 2: dic is a dictionary. We find keys that 
		#match any path on the list and recurse on them
		result = {}
		for p in paths:
			if len(p) == 0:
				result = dic
			elif p[0] in dic:
				#paths beginning with p[0] with p[0] poped
				new_paths = map(lambda x : x[1:], filter(lambda x : x and x[0] == p[0], paths))
				f = __dict_find__(new_paths, dic[p[0]])
				if __non_empty_container_or_object__(f):
					result[p[0]] = f
		return result
	else:
		#Case 3: dic is neither a dictionary nor a list. 
		#We return if there's an empty path
		empty_paths = filter(lambda x : len(x) == 0, paths)
		if len(empty_paths) > 0:
			return dic

def dict_find(paths, dic):
	p = map(lambda x : x.split("."), paths)
	return __dict_find__(p, dic)

def flat_dict(dic, previous_path=''):
	results = []
	if type(dic) is dict:
		for key in dic.keys():
			if len(previous_path) == 0:
				prior_path = key
			else:
				prior_path = previous_path + "." + key
			results.extend( flat_dict(dic[key], prior_path) )
		results.extend([previous_path])
		return results
	if type(dic) is list or type(dic) is tuple:
		for item in dic:
			results.extend(flat_dict(item, previous_path ))
		results.extend([previous_path])
		return results

	results.extend([previous_path])
	return [previous_path]

def paths_to_include(dic, transformacoes, default='$remove'):
	all_flat_paths = set(flat_dict(dic))
	copy = set([key for key in transformacoes.keys() if transformacoes[key] == '$copy'])
	remove = set([key for key in transformacoes.keys() if transformacoes[key] == '$remove'])
	
	if default=='$remove':
		valid_paths = copy
	else:
		valid_paths = all_flat_paths - remove
	return valid_paths
	
