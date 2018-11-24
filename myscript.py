# получает входной файл с текстом и приводит предобработку
# частеричные теги сравнимы с тэгами Unversal POS 
import wget
import requests
import re
from pymystem3 import Mystem
import sys

def tag_mystem(text='Текст нужно передать функции в виде строки!'):  
    m = Mystem()
    processed = m.analyze(text)
    tagged = []
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
    return tagged	

# получает имя входного файла или обращается к стандартному	
if len (sys.argv) > 1:
	textfile = (sys.argv[1] )
else:
	text_url = 'http://rusvectores.org/static/henry_sobolya.txt'
	textfile = wget.download(text_url)

text = open(textfile, 'r', encoding='utf-8').read()

udpipe_url = 'http://rusvectores.org/static/models/udpipe_syntagrus.model'

modelfile = wget.download(udpipe_url)

url = 'https://raw.githubusercontent.com/akutuzov/universal-pos-tags/4653e8a9154e93fe2f417c7fdb7a357b7d6ce333/ru-rnc.map'

mapping = {}
r = requests.get(url, stream=True)
for pair in r.text.split('\n'):
    pair = re.sub('\s+', ' ', pair, flags=re.U).split(' ')
    if len(pair) > 1:
        mapping[pair[0]] = pair[1]	
	
processed_mystem = tag_mystem(text=text)
str = '\n'.join(processed_mystem)

# получает имя выходного файла или создаёт стандартный	
if len (sys.argv) > 2:
	fname = (sys.argv[2] )
else:
	fname = 'output.txt'

f = open(fname, 'w')
f.write(str)
f.close()