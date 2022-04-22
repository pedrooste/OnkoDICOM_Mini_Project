"""Fuzzy Wuzzy example demonstrating functionality"""
from fuzzywuzzy import fuzz, process
from Levenshtein import distance

"""
FuzzyWuzzy

fuzzywuzzy is a string matching library that uses Levenshtein Distance (the number of single character edits) to 
calculate the difference between two strings, calculated as a ratio.

This library also depends on Python-Levenshtein, otherwise it will use a slower method
"""

# Quick test of Levenshtein
print(distance('pedro', 'bodro')) # 2

# Compares entire string
print(fuzz.ratio('pedro', 'bedro'))  # 80
print(fuzz.ratio('pedro', 'ordep'))  # 20

# Ensures first string can be found within the second
print(fuzz.partial_ratio('pedro is rad', 'pedro is rad!'))  # 100
print(fuzz.partial_ratio('pedro is rad', 'pedro rad'))  # 67

# Ensures all words can be found
print(fuzz.token_sort_ratio('pedro is mad', 'pedro mad is'))  # 100
print(fuzz.token_sort_ratio('pedro is mad', 'pedro is mad mad'))  # 86

# Sorting dosn't matter (like a set)
print(fuzz.token_set_ratio('pedro is mad', 'pedro is mad mad'))  # 100

# Extracting choices
print(process.extract(
    "pedro is pretty cool", ["pedro", "pedro is ", "bredbo is pretty cool", "pedro cool"]
))
print(process.extractOne(
    "pedro is pretty cool", ["pedro", "pedro is ", "bredbo is pretty cool", "pedro cool"]
))
