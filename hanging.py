import sys
from string import ascii_uppercase as upperc

target = sys.argv[1]
target = target.upper()
wordlen = len(target)

char_per_line = 100

def print_words(word_list,word_length):
	num_words = len(word_list)
	#words/line = (chars/line) / (chars/word including a space)
	words_per_line = char_per_line/(word_length+1)
	#lines: number full char_per_line-character lines = (number words) / (words/line)
	lines = num_words/words_per_line
	#remainder: number extra words = (number words) mod (words/line)
	remainder = num_words % words_per_line

	for line in range(lines):
		print ' '.join( word_list[words_per_line*line : words_per_line*(line +1)] )
	if remainder > 0:
		print ' '.join( word_list[-remainder:] )


if '.' in target:
	wronglets = sys.argv[2:]
	wronglets = [l.upper() for l in wronglets]

	if wordlen>8:
		sys.exit('Target word too long')

	letterpos = [(i,target[i]) for i in range(len(target)) if target[i] is not '.']
	try:
		last_vowel_pos = max([letterpos[i][0] for i in range(len(letterpos)) if \
				letterpos[i][1] in 'AEIOU'])
	except ValueError:
		last_vowel_pos = -1

	#Read in the string of words from the dictionary file
	dictfile = 'dict'+str(wordlen)+'.txt'
	with open(dictfile,'r') as f:
		fulldictstring = f.read()

	#List of all words in the dictionary that are the same length as target
	fulldict = [fulldictstring[ (wordlen+1)*i : (wordlen+1)*i+wordlen ] \
			for i in range(len(fulldictstring)/(wordlen+1)+1)]
	#Keep only those words with the target letters in proper spaces
	filterdict = filter(lambda word: all( [letterpos[i][1]==word[letterpos[i][0]] \
			for i in range(len(letterpos)) ]),fulldict)
	#Keep only those words with none of the already guessed wrong letters
	filterdict = filter(lambda word: all([l not in word for l in wronglets]), \
			filterdict)
	#Keep only those words with correct letters ONLY in correct spaces, nowhere else
	filterdict = filter(lambda word: all([target.count(l)==word.count(l) for l in \
			set(zip(*letterpos)[1]) ]),filterdict)
	#Keep only words with no vowels beyond last known vowel (which is always given)
	filterdict = filter(lambda word: \
			all([word[i] not in 'AEIOU' for i in range(last_vowel_pos+1,len(word))]),\
			filterdict)

	# filterdict now holds only valid words. We must find the most common letter.
	# We start by creating an array to hold a count of how many words contain 
	# each letter.
	if len(filterdict) == 0:
		sys.exit("You've eliminated all valid words!")
	lettersbyword = [0]*26
	for word in filterdict:
		nontargetletters = filter(lambda l: l not in zip(*letterpos)[1], \
				set(word))
		for letter in nontargetletters:
			lettersbyword[upperc.index(letter)]+=1

	# The max value of this array is the frequency of most common letter.
	maxletternum = max(lettersbyword)
	# There might be more than one letter in this number of words.
	maxletterlist = [upperc[i] for i in range(len(lettersbyword)) if \
				lettersbyword[i] == maxletternum]
	
	if len(maxletterlist)>1:
		print 'Letters in most words: '+' '.join(maxletterlist)
	else:
		print 'Letter in most words: '+maxletterlist[0]

	# Print all the valid states (if there are fewer than 200)
	if len(filterdict)>200:
		sys.exit('{} words fit'.format(num_words))
	else:
		print_words(filterdict,wordlen)
else:
	if wordlen != 12:
		sys.exit("Put in 12 letters to get all words.")
	
	raw_wants = sys.argv[2:]
	wants = [l.upper() for l in set(raw_wants)]

	for i in range(5):
		x = 8-i
		dictfile = 'dict'+str(x)+'.txt'
		with open(dictfile,'r') as f:
	                fulldictstr = f.read()
		
		#Full dictionary of words of length x
		fulldict = [fulldictstr[(x+1)*j:(x+1)*j+x] \
				for j in range(len(fulldictstr)/(x+1)+1)]

		#Filter out words that have any non-target letters
		filterdict = filter(lambda word: \
				all( [word.count(l)<=target.count(l)\
				for l in set(word)] ), \
				fulldict)

		#Filter out words that don't have all the letters we want
		if len(wants)>0:
			filterdict = filter(lambda word: \
					all( [l in word for l in wants]),\
					filterdict)

		# Printing the words
		print '{} letter words:'.format(x)

		num_words = len(filterdict)
		if num_words == 0:
			print '----'
		else:
			print_words(filterdict,x)