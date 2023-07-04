Configuration data structure

A list of strings where a valid of string is of type substr1=substr2 

The algorithm will then replace the = in every valid string with $, then append all the modifed valid strings together, seperated by |  

This requires the physicists to co-ordinates with g4beamline to help output the correct setup


STEP 1: develop a function that takes in a list of strings representing files, and another list of string representing already existed files, return the index of only existed files.

STEP 2: develop a function that takes in a list of strings of type substr1=substr2, returns a list of string substr1$substr2

STEP 3: develop a function that takes in a list of strings, concatenate them into one single string of type string1|string2|string3.txt

STEP 4: use step 2 function -> step 3 function 

STEP 5: given a list of number representing indices, and a list of objects, select only the list of objects that is indices of the list 
