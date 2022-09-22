# CS 4395.001 - NLP
# Leo Nguyen
# NetID: ldn190002

# Porfolio Chapter 5: Word Guess Game


import sys
import os
import nltk

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

# Preprocessing raw text
def text_processing(raw_text):

	# Tokenize
	tokens =  word_tokenize(raw_text)

	processed_tokens = [t.lower() for t in tokens if t.isalpha() and
				t not in stopwords.words('english') and
				len(t)>5]

	# Lemmatize
	wnl = WordNetLemmatizer()
	lemmas = [wnl.lemmatize(t) for t in processed_tokens]
	unique_lemmas = set(lemmas) 	# make unique

	# POS Tagging in unique_lemmas
	tags = pos_tag(unique_lemmas)

	print('First 20 tagged items in unique_lemmas: ')
	for i in range(0,20):
		print(tags[i])

	# List of nouns in lemmas: 
	tags = pos_tag(lemmas)
	nouns = []
	for token, pos in tags:
		if pos in ['NN', 'NNS', 'NNP', 'NNPS']:
			nouns.append(token)

	print('\nNumber of tokens: ', len(processed_tokens))
	print('Number of nouns: ', len(nouns))
	
	return processed_tokens, nouns

# main
def main():
    # Method to handle the filepath in both Window and Mac
    def read_file(filepath):
        with open(os.path.join(os.getcwd(), filepath), 'r') as f:
            input_file = f.read()
        return input_file

    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        raw_text = read_file(fp)
       
        # Calculate the lexical diversity
        tokens =  word_tokenize(raw_text)
        unique_tokens = set(tokens)
        print('Lexical diversity: %.2f' %(len(unique_tokens) / len(tokens)))

       	processed_tokens, nouns = text_processing(raw_text)


       	# The nouns list was extract from lemmas.
       	# Some word in lemmas form is different from original form in token.
       	# So some nouns in nouns_dict have count 0

       	nouns_dict = {}
       	for noun in nouns: # Initialize nouns dictionary
       		nouns_dict[noun] = 0

       	for noun in nouns_dict:
       		if noun in processed_tokens:
       				nouns_dict[noun] += 1

        print('\n 50 most common:')
        i = 0
       	for noun in sorted(nouns_dict, key=nouns_dict.get, reverse=True):
       		print(noun, ':', nouns_dict[noun])
       		i += 1
       		if i > 10:
       			break

if __name__ == "__main__":
	main()