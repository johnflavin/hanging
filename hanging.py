import sys
import csv
from string import ascii_uppercase as upperc

target = sys.argv[1]
target = target.upper()
wordlen = len(target)

char_per_line = 100

def print_words(word_list,word_length):
	num_words = len(word_list)
	#words/line = (chars/line) / (chars/word including a space)
	words_per_line = int(char_per_line/(word_length+1))
	#remainder: number extra words = (number words) mod (words/line)
	remainder = num_words % words_per_line
	#lines: number full char_per_line-character lines = (number words) / (words/line)
	lines = int( num_words/words_per_line )

	for line in range(lines):
		print(' '.join( word_list[words_per_line*line : words_per_line*(line +1)] ))
	if remainder > 0:
		print(' '.join( word_list[-remainder:] ))


if '.' in target:
	wronglets = sys.argv[2:]
	wronglets = [l.upper() for l in wronglets]

	if wordlen>8:
		sys.exit('Target word too long')

	letters = [char for char in target if char != '.']
	indices = [target.index(char) for char in letters]
	num_letters = len(letters)
	try:
		last_vowel_pos = max([indices[i] for i in range(num_letters) if letters[i] in 'AEIOU'])
	except ValueError:
		last_vowel_pos = -1

	#Read in the string of words from the dictionary file
	dictfile = 'dict{0}.csv'.format(wordlen)
	try:
		f = open(dictfile,'r')
	except:
		sys.exit('could not open dictionary file')
	reader = csv.reader(f)

	#List of all words in the dictionary that are the same length as target
	fulldict = []
	for line in reader:
		fulldict += line
	f.close()

	#Keep only those words with the target letters in proper spaces
	filterdict = [word for word in fulldict if all( [letters[i]==word[indices[i]] for i in range(num_letters) ] )]

	#Keep only those words with none of the already guessed wrong letters
	filterdict = [word for word in filterdict if all([lett not in word for lett in wronglets])]

	#Keep only those words with correct letters ONLY in correct spaces, nowhere else
	filterdict = [word for word in filterdict if all([target.count(lett)==word.count(lett) for lett in set(letters)])]

	#Keep only words with no vowels beyond last known vowel (which is always given)
	filterdict = [word for word in filterdict if all([lett not in 'AEIOU' for lett in word[last_vowel_pos+1:] ])]


	# filterdict now holds only valid words. We must find the most common letter.
	# We create an array to hold a count of how many words contain each letter.
	if len(filterdict) == 0:
		sys.exit("You've eliminated all valid words!")
	lettersbyword = [0]*26
	for word in filterdict:
		for letter in set(word):
			if letter not in letters:
				lettersbyword[upperc.index(letter)]+=1

	# The max value of this array is the frequency of most common letter.
	maxletternum = max(lettersbyword)
	# There might be more than one letter with this frequency, so list them all.
	maxletterlist = [upperc[i] for i in range(26) if lettersbyword[i] == maxletternum]
	
	if len(maxletterlist)>1:
		print('Letters in most words: '+' '.join(maxletterlist))
	else:
		print('Letter in most words: '+maxletterlist[0])

	# Print all the valid states (if there are fewer than 200)
	if len(filterdict)>200:
		sys.exit('{0} words fit'.format(num_words))
	else:
		print_words(filterdict,wordlen)
else:
	if wordlen != 12:
		sys.exit("Put in 12 letters to get all words.")
	
	raw_wants = sys.argv[2:]
	wants = [lett.upper() for lett in set(raw_wants)]

	for i in range(5):
		x = 8-i

		#Read in the string of words from the dictionary file
		dictfile = 'dict{0}.csv'.format(x)
		try:
			f = open(dictfile,'r')
		except:
			sys.exit('could not open dictionary file')
		reader = csv.reader(f)

		#List of all words in the dictionary that are the same length as target
		fulldict = []
		for line in reader:
			fulldict += line
		f.close()

		#Filter out words that have any non-target letters
		filterdict = [word for word in fulldict if all( [word.count(lett)<=target.count(lett) for lett in set(word)] )]

		#Filter out words that don't have all the letters we want
		filterdict = [word for word in filterdict if all( [lett in word for lett in wants] )]

		# Printing the words
		print('{0} letter words:'.format(x))

		if len(filterdict) == 0:
			print('----')
		else:
			print_words(filterdict,x)