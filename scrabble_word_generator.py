'''
This module takes user input of their Scrabble deck
and returns the possible words that could be formed with available tiles
and prints this output as a list, separated by word length, ranked by score

Acceptable input: "abc" "a b c" and "a,b,c"
'''

import re
import itertools

#function that takes input, checks inpu validity
#if input is alphabet, and in correct form, returns formated input with only alphabets
#correct form = "abc" "a,b,c" "a b c"
def get_input():

    while True:
        #prompt input
        print("Enter the each letter in your rack")
        tt = input()

        try:
            ff = str(tt).lower()
        except (ValueError, TypeError):
            print("Please enter alphabets. Try again.")
            continue

        if tt == None or tt == "\n" or tt == "":
            print("Please enter alphabets. Try again.")
            continue
        
        #checking if it is only alphabet
        match2 = re.findall(r'([^a-z\s,])+[^a-z\s,]?', ff)
        if match2 != None:

            for each in match2:
                print(each,end = " ")

        #return messages when there is non alphabet
        if len(match2) == 1:
            print("is not a valid letter. Please try again.")
            continue
        elif len(match2) > 1:
            print("are not valid letters. Please try again.")
            continue

        break
    
    #use regex to identify alphabets
    match4 = re.search(r'([a-z],?\s?)+[a-z]', ff)
    try:
        aa = match4[0]
    except TypeError:
        aa = 0

    #formating string to only alphabets
    bb = aa.replace(" ", "")
    formated_input = bb.replace(",", "")

    return formated_input
    
#function that permutes letters 
def permute_letters(y):

    permuted_list = []

    #permuting strings of different lengths
    for i in range(len(y)+1):
        if i == 0:
            continue
        
        #invoking permutation tool from itertools module, permuting the whole string
        permute_1 = itertools.permutations(y, i)

        #changing to list
        ap = list(permute_1)

        #extracting, making string, appending to list
        qq = []
        for j in range(len(ap)):
            z = ""
            for k in range(len(ap[j])):
                z += ap[j][k]
            qq.append(z)
    
        permuted_list.append(qq)

    return permuted_list


#function that extracts from scrabble word list, returns list
def process_file(filename): 


    list_words = []
    xxx = str(filename)
    f = open(xxx, 'r')
 
    for line in f:
        t = line.strip()
        list_words.append(str(t).lower())

  #sort items in list
    sorted_items = sorted(list_words)

    f.close()

    return sorted_items

#function that calculates the score for a particular word, 
#accepts word argument, returns score
def calc_score_word(y):

    dict1 = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
             "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
             "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
             "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
             "x": 8, "z": 10}
  
    score = 0

    for q in range(len(y)):
        t = dict1[y[q]]
        score += t
  
    return score

#function that takes a list of permuted words from input
#returns dict of words that are valid scrabble words
#keys = length of word
def check_words(az):
    #put correct file address for scrabble word list here
    fileaddress = "/Users/ianyuen/Documents/GitHub/mpcs50101-2020-autumn-assignment-6-pirateontheseas/scrabble_list.txt"
    word_list = process_file(fileaddress)

    possible_word = {}

    #nested loops to get beween layers of lists
    for i in range(len(az)):
        for j in range(len(az[i])):
            if az[i][j] in word_list:
                #remove that word so no duplicaate
                word_list.remove(az[i][j])
                key = len(az[i][j])
                #invoking calculate score of a particular word
                score = calc_score_word(az[i][j])
                #forming into tuple pair
                pair = (az[i][j], score)
                try:
                    #checking if the key for that word length exists
                    #puting it in the dictionary
                    possible_word[key].append(pair)
                except KeyError:
                    possible_word[key] = []
                    possible_word[key].append(pair)

    return possible_word

#takes a list of tuples of valid scrbble words with scores
#sorts said list by score
def sort_by_score(y):
    temporary_dict = {}
    sorted_list = []

    #first received list into a dict
    for i in range(len(y)):
        temporary_dict[y[i][0]] = y[i][1]

    #sorting by the value of the score
    for k in sorted(temporary_dict, key=temporary_dict.get, reverse=True):
        sorted_list.append((k, temporary_dict[k]))

    return sorted_list

#function that prints the output in specified format
def print_output(y):
    
    global input1
    print("\n")
    
    #printing each word length
    #takes possible word list as argument, prints output
    for i in range(len(input1)+1):

        #if no such word length, print "no words"
        try:
            a = y[i]
        except KeyError:
            #skip word lengths 0 and 1
            if i != 0 and i != 1:
                q = str(i) + " Letter Words"
                print(q)
                print("-" * len(q))
                print("no words")
                print("\n")
                continue
            else:
                continue
        
        #sort list, note this is a sublist of the larger dictionary
        sorted_list = sort_by_score(a)

        q = str(i) + " Letter Words"

        print(q)
        print("-" * len(q)) #formating line

        #printing each tuple of word and their score, only print top 10
        for j in range(0, 9):
            print(str(sorted_list[j][0]) + " - " + str(sorted_list[j][1]) + " points")

        print("\n")

    return 0




def main():

    global input1
    #getting input
    input1 = get_input()
    #permuting input
    permuted_words = permute_letters(input1)
    #checking which permutations are valid words, scoring them
    possible_words_collected = check_words(permuted_words)
    #sorting dict, printing output
    print_output(possible_words_collected)






if __name__=="__main__":
    main()
