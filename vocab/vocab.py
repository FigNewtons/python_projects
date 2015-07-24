import json
from FileHandle import File

# from vocab import Vocab
class Vocab(File):
    def __init__(self, jsonfile):
        self.subjects = set()
        self.dictionary = {}
        
        with open(jsonfile) as jfile:
            d = json.load(jfile)
            self.dictionary = d['dictionary']
        
        for term in self.dictionary:
            if 'subject' in self.dictionary[term]:
                self.subjects.add(self.dictionary[term]['subject'])
        
        super().__init__(jsonfile)
    
    
    def define(self, term):
        """Return just the definition of a term. """
        if term in self.dictionary:
            try:
                return(self.dictionary[term]['meaning'])
            except KeyError:
                print('Definition not found')
        else:
            print('Word not in the dictionary')
        return None
    
    
    def entry(self, term):
        """Return the term, part-of-speech, and definition of a term. """
        if term in self.dictionary:
            try:
                pos = self.dictionary[term]['pos']
                definition = self.dictionary[term]['meaning']
                return term + " (" + pos + ") - " + definition
            except KeyError:
                print('Either part-of-speech and/or definition not found')
        else:
            print('Word not in dictionary')
        return None
    
    
    def words_about(self, subject):
        """Return a list of all words pertaining to a given subject. """
        terms = []
        for term in self.dictionary:
            if 'subject' in self.dictionary[term]:
                s = self.dictionary[term]['subject']
                if s == subject:
                    terms.append(term)
        return terms
    
    
    def wordlist(self):
        """Return a sorted list of all words in the dictionary. """
        return sorted(self.dictionary.keys)
    
    #TODO: Allow writing to dictionary
    def add_word(term, meaning):
        return term + " - " + meaning

