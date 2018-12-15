# получает входной файл с текстом и приводит предобработку
# частеричные теги сравнимы с тэгами Unversal POS 
import wget
import requests
import re
from pymystem3 import Mystem
import sys

import csv

class Tagger:
	input = ""
	output = ""
	
	def __init__(self, input="input.txt", output="output.txt"):		
		self.input = input
		self.output = output

	def tag_mystem(self): 
		try:
			text = open(self.input, 'r', encoding='utf-8').read()
		except IOError as e:
			print(u'Не удалось открыть файл ' + self.input)
			exit()
		
		m = Mystem()
		processed = m.analyze(text)
		tagged = []
		
		url = 'https://raw.githubusercontent.com/akutuzov/universal-pos-tags/4653e8a9154e93fe2f417c7fdb7a357b7d6ce333/ru-rnc.map'

		mapping = {}
		r = requests.get(url, stream=True)
		for pair in r.text.split('\n'):
			pair = re.sub('\s+', ' ', pair, flags=re.U).split(' ')
			if len(pair) > 1:
				mapping[pair[0]] = pair[1]	
		
		for w in processed:
			try:
				lemma = w["analysis"][0]["lex"].lower().strip()
				pos = w["analysis"][0]["gr"].split(',')[0]
				pos = pos.split('=')[0].strip()
				if pos in mapping:
					tagged.append(lemma + '_' + mapping[pos]) # здесь мы конвертируем тэги
				else:
					tagged.append(lemma + '_X') # на случай, если попадется тэг, которого нет в маппинге
			except KeyError:
				continue # я здесь пропускаю знаки препинания, но вы можете поступить по-другому	
			
		str = '\n'.join(tagged)

		f = open(self.output, 'w')
		f.write(str)
		f.close()