import sys
from string import ascii_uppercase as upperc

target = sys.argv[1]
target = target.upper()
wordlen = len(target)

if '.' in target:
	wronglets = sys.argv[2:]
	wronglets = [l.upper() for l in wronglets]

	if wordlen>8:
		sys.exit('Target word too long')

	letterpos = [(i,target[i]) for i in range(len(target)) if target[i] is not '.']
	try:
		lvpos = max([letterpos[i][0] for i in range(len(letterpos)) if \
				letterpos[i][1] in 'AEIOU'])
	except ValueError:
		lvpos = -1

	dictfile = 'dict'+str(wordlen)+'.txt'
	with open(dictfile,'r') as f:
		fulldictstring = f.read()

	#Full dictionary of words same length as target
	fulldict = [fulldictstring[(wordlen+1)*i:(wordlen+1)*i+wordlen] for i in \
			range(len(fulldictstring)/(wordlen+1)+1)]
	#Keep only those words with the target letters in proper spaces
	filterdict = filter(lambda word: all( [letterpos[i][1]==word[letterpos[i][0]] \
			for i in range(len(letterpos)) ]),fulldict)
	#Keep only those words without any already guessed wrong letters
	filterdict = filter(lambda word: all([l not in word for l in wronglets]), \
			filterdict)
	#Keep only those words with correct letters ONLY in correct spaces, nowhere else
	filterdict = filter(lambda word: all([target.count(l)==word.count(l) for l in \
			set(zip(*letterpos)[1]) ]),filterdict)
	#Keep only words with no vowels beyond last known vowel (which is given)
	filterdict = filter(lambda word: \
			all([word[i] not in 'AEIOU' for i in range(lvpos+1,len(word))]),\
			filterdict)

	if len(filterdict) == 0:
		sys.exit("You've eliminated all valid words!")
	lettersbyword = [0]*26
	lettersatpos = [0]*26
	for word in filterdict:
		nontargetletters = filter(lambda l: l not in zip(*letterpos)[1], \
				set(word))
		for letter in nontargetletters:
			lettersbyword[upperc.index(letter)]+=1

	maxletternum = max(lettersbyword)
	maxletterlist = [upperc[i] for i in range(len(lettersbyword)) if \
				lettersbyword[i] == maxletternum]
	s = ''
	for letter in maxletterlist:
		s +=" "+letter
	if len(maxletterlist)==1:
		print "Letter in most words:"+s
	else:
		print "Letters in most words:"+s
	if len(filterdict)>200:
		sys.exit(str(len(filterdict))+" words fit")
	else:
		x = wordlen

		#wpl: words/line = (chars/line) / (chars/word)
		wpl = 90/(x+1)
		#lines: number full 90 char lines = (number words) / (words/line)
		lines = len(filterdict)/wpl
		#remainder: number extra words = (number words) mod (words/line)
		remainder = len(filterdict)%wpl

		s = ''
		for lin in range(lines):
			for word in range(wpl):
				s += filterdict[wpl*lin+word]+' '
			print s
			s = ''
		for word in range(remainder):
			s += filterdict[wpl*lines+word]+' '
		if s != '':
			print s
else:
	if wordlen != 12:
		sys.exit("Put in 12 letters to get all words.")
	
	rawwants = sys.argv[2:]
	wants = [l.upper() for l in set(rawwants)]

	for i in range(5):
		x = 8-i
		dictfile = 'dict'+str(x)+'.txt'
		with open(dictfile,'r') as f:
	                fulldictstr = f.read()
		
		#Full dictionary of words of length l
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

		#wpl: words/line = (chars/line) / (chars/word)
		wpl = 90/(x+1)
		#lines: number of full 90 char lines = (number words) / (words/line)
		lines = len(filterdict)/wpl
		#remainder: number of extra words = (number words) mod (words/line)
		remainder = len(filterdict)%wpl

		print str(x)+" letter words:"
		s = ''
		if lines == 0 and remainder == 0:
			print '----'
		for lin in range(lines):
			for word in range(wpl):
				s += filterdict[wpl*lin+word]+' '
			print s
			s = ''
		for word in range(remainder):
			s += filterdict[wpl*lines+word]+' '
		if s != '':
			print s
