# Libraries
import numpy as np
import os.path
from os import path
import random
import time
from collections import Counter

# Utilitarian functions for data loading and dictionary creation ===========================

def file_loading(dictionary_path):
    #to load the file
    if path.exists(dictionary_path) == False: #if no file in location
        print("Error : File "+dictionary_path+" not found in the folder")
        return False
    else:
        file = open(dictionary_path,'r')
        lines = file.readlines()
        file.close()
    return lines

def dictionary_creation(lines):
    #to create te dictionary structure we use next
    dictionary = {}
    empty_list = []
    incorrect_list = []
    l_total = len(lines)
    for l_index in range(l_total):
        l = lines[l_index].split()
        if len(l)==0:
            empty_list.append(l_index+1)
            continue
        if len(l)==1: #usually digital key without word, word without digital key or word and digital keys bonded : not usable
            incorrect_list.append(l_index+1)
            continue
        if len(l)>2: #header or incorrect format : not usable (at first intent at least)
            incorrect_list.append(l_index+1)
            continue
        else:
            if l[0].isdigit(): #if correct digital key 
                dictionary.update({l[0]:l[1]})
            elif l[1].isdigit(): #in case digital key and word are inversed. If both are pure digitals, the previous condition (if) has applied normally 
                dictionary.update({l[1]:l[0]})
            else: #incorrect format not taken into account
                incorrect_list.append(l_index+1)
    if len(empty_list)>0:
        output_write(errorfile_path,error_type="empty_lines",error_list=empty_list)
    if len(incorrect_list)>0:
        output_write(errorfile_path,error_type="incorrect",error_list=incorrect_list)
    return dictionary

# Utilitarian function : analyze and validation of the dictionary ==========================

def find_duplicates(dictionary):
    #to find duplicates in the list of words from the dictionary
    values_list = dictionary.values()
    counter = dict(Counter(values_list))
    duplicates = [item for item, count in counter.items() if count > 1]
    if len(duplicates)>0:
        print("Warning : the file "+dictionary_path+" contains duplicates. That might affect the robustness of the passphrase generated with this method. \n")
        output_write(errorfile_path,error_type="duplicates",error_list=duplicates)
    return duplicates

def check_dictionary(dictionary):
    #to analyze and validate the utility of the dictionary in generating good passphrases
    threshold = 100
    if len(dictionary) == 0: #if empty dictionary
        print("Error : the file "+dictionary_path+" provides no word usable for generating a passphrase \n")
        output_write(errorfile_path,error_type="empty_dictionary")
        return False
    #Digital keys of the dictionary : update() function will automatically erase the old key. We voluntary set an "arbitrary" thresholds : 100 (based on the max words we authorize in this passphrase generator and the median size of the standard list provided by the website). Below the threshold, the user has to be warned about security.
    keys_len = len(set(list(dictionary.keys())))
    if keys_len<threshold:
        print("Warning : the file "+dictionary_path+" provides only "+str(keys_len)+" independent key(s). That might have an impact on generating a robust passphrase with this method. Please update the file on website : https://theworld.com/%7Ereinhold/diceware.wordlist.asc \n")
        output_write(errorfile_path,error_type="few_keys",error_len=keys_len)
    #Values of the dictionary : a word has more chances to be chosen. It won't make the algorithm to crash but it can impact the robustness of the passphrase.
    values_len = len(set(list(dictionary.values())))
    if values_len<threshold:
        print("Warning : the file "+dictionary_path+" provides only "+str(values_len)+" independent word(s). That might have an impact on generating a robust passphrase with this method. Please update the file on website : https://theworld.com/%7Ereinhold/diceware.wordlist.asc \n")
        output_write(errorfile_path,error_type="few_values",error_len=values_len)
    return True

def median_length_words(dictionary):
    #to calculate the median length of a word. Useful regarding the criterion on 100-characters limit, if any
    words_list = list(dictionary.values())
    words_len = [len(word) for word in words_list]
    median_len = np.median(words_len)
    return median_len  

def check_length_words(dictionary):
    #to check if the criterion on 100-characters limit can be respected
    median_word = median_length_words(dictionary)
    max_words_from_list = int(100.0/(1+median_word)) #maximum words number calculated from the median length of the words included in the dictionary, spaces taken into account (thus the 1+ at the dividend). This will also reduce the amount of time to generate a passphrase
    max_words = min(max_words_fixed,max_words_from_list)
    if max_words == 0:
        print('Error : impossible to give a passphrase or password with less than 100 characters. Words are too long. Please update the file on website : https://theworld.com/%7Ereinhold/diceware.wordlist.asc \n')
        output_write(errorfile_path,error_type="too_long",error_len=median_word)
    elif max_words == 1:
        print('Warning : only password with less than 100 characters are available. Passphrase shorter than 100 characters might not exist \n')
        output_write(errorfile_path,error_type="long_password",error_len=median_word)
    return max_words

# Utilitarian function : error output in ErrorWarning.txt ==================================

def output_write(errorfile_path,new_run=False,error_type=None,error_list=None,error_len=None):
    # Write the problems encountered during the execution inside a ErrorWarnings.txt file found at 'path errorfile_path'. It also added index of empty lines or incorrect lines, that cannot be handled by the program
    if path.exists(dictionary_path) == False: #no file in location
        errorfile = open(errorfile_path,"w")
        errorfile.close()
    if new_run: #creation of the new log
        with open(errorfile_path, "a") as errorfile:
            errorfile.write("\n====================")
            errorfile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+"\n")
            errorfile.write("Number of lines of the file : "+str(error_len)+"\n")
    elif error_type == "duplicates": #if duplicates
        with open(errorfile_path, "a") as errorfile:
            errorfile.write("Duplicates found at the following line : "+" ".join(map(str,error_list))+"\n")
    elif error_type == "empty_dictionary": #if the dictionary is empty
        with open(errorfile_path, "a") as errorfile:
            errorfile.write("Error : the file "+dictionary_path+" provides no word usable for generating a passphrase\n")
    elif error_type == "few_keys": #if the dictionary has few digital keys
        with open(errorfile_path, "a") as errorfile:
            errorfile.write("Warning : the file "+dictionary_path+" provides only "+str(error_len)+" independent key(s). That might have an impact on generating a robust passphrase with this method. Please update the file on website : https://theworld.com/%7Ereinhold/diceware.wordlist.asc\n")
    elif error_type == "fey_words": #if the dictionary as fey independant words
        with open(errorfile_path, "a") as errorfile:
            errorfile.write("Warning : the file "+dictionary_path+" provides only "+str(error_len)+" independent word(s). That might have an impact on generating a robust passphrase with this method. Please update the file on website : https://theworld.com/%7Ereinhold/diceware.wordlist.asc\n")
    elif error_type == "empty_lines": #if some lines are empty
        with open(errorfile_path, "a") as errorfile:
            errorfile.write("Empty lines have been found : "+" ".join(map(str,error_list))+"\n")
    elif error_type == "incorrect": #if some lines have incorrect format, that connot be handled by the program
        with open(errorfile_path, "a") as errorfile:
            errorfile.write("Incorrect lines have been found (these lines may include header or footer) : "+" ".join(map(str,error_list))+"\n")
    elif error_type == "too_long": #if the words are mainly too long to generate even a password shorter than 100 characters
        with open(errorfile_path, "a") as errorfile:
            errorfile.write("Long words : median length = "+str(error_len)+"\n")
            errorfile.write("'Error : impossible to give a passphrase or password with less than 100 characters. Words are too long. Please update the file on website : https://theworld.com/%7Ereinhold/diceware.wordlist.asc \n")
    elif error_type == "long_password": #if the words are mainly too long to generate a passphrase shorter than 100 characters, but can generate a passworder shorter than this limit
        with open(errorfile_path, "a") as errorfile:
            errorfile.write("Long words : median length = "+str(error_len)+"\n")
            errorfile.write("Warning : only password with less than 100 characters are available. Passphrase shorter than 100 characters might not exist \n")
    return

# Utilitarian functions for the passphrase generation with the diceware method =============

def ask_max_characters():
    #to ask the user if the respect of the standart 100-characters limitation is expected
    ask_test = True
    while ask_test:
        ask = input("Do you want to respect the standard limitation of 100 characters on the passphrase ? (recommanded) Enter Y for Yes or N for No\n")
        if (ask == 'Y') | (ask == 'y') | (ask == 'Yes') | (ask == 'yes') | (ask == 'YES'):
            return True
        elif (ask == 'N') | (ask == 'n') | (ask == 'No') | (ask == 'no') | (ask == 'NO'):
            return False
        elif (ask == 'quit') | (ask == 'QUIT') | (ask == 'Quit'):
            return 3

def ask_number_words(dictionary,max_words,max_100_characters):
    #to input the desired number of words in the passphrase by asking the user
    N_test = True
    while N_test:
        if max_100_characters:
            question = "Number of words in the passphrase ? 1 minimum (password), "+str(max_words)+" maximum, at least 4 words are recommended for good robustness\n"
        else:
            question = "Number of words in the passphrase ? 1 minimum (password), at least 4 words are recommended for good robustness\n"
        N_words = input(question)
        try:
            if (N_words == 'quit') | (N_words == 'QUIT') | (N_words == 'Quit'):
                return N_test, True
        except ValueError:
            pass
        try:
            N_words = int(N_words)
            if N_words<=0: #fordbidding case N_words = 0
                print("Error : no passphrase can be created with 0 word\n")
            elif (N_words>max_words) and (max_100_characters==True): #too many words
                print("Error : too many words required for the passphrase. Risks to exceed the common 100 characters limit\n")
            else:
                N_test = False
        except ValueError:
            pass
    return N_test, N_words

def diceware_generator(dictionary, keys_list,N_words):
    #diceware routine
    passphrase_list = []
    random.seed(time.time()) #seed based on extended computer time for better randomization
    for k in range(N_words):
        key = random.choice(keys_list) #in this situation, using 5 dices with 6 sides is equivalent to a uniform law on each word/key of the dictionary. Moreover, the second choice prevents cases where words/keys are lacking (if 11234 is missing, the user need to try again if using the 5 dices) or corrupted (part of the digital key is missing, for example 1234 which is missing a 5th digit)
        passphrase_list.append(dictionary[key])
    passphrase_w = ' '.join(passphrase_list)
    return passphrase_w

def passphrase_generator(dictionary,max_words):
    #more global function to generate the passphrase from the dictionary
    on_built_test = True
    dtime_max = 60 #60 seconds maximum for the calculation. If more, it means there is a too huge problem on the list.
    while on_built_test:
        if max_words > 1:
            max_100_characters = ask_max_characters()
        else:
            max_100_characters = False
        N_test, N_words = ask_number_words(dictionary,max_words,max_100_characters)
        if type(N_words) == bool: #quit option asked
            return False
        keys_list = list(dictionary.keys())
        if max_100_characters == True:
            time_start = time.time()
            gen_test = True
            while gen_test:
                passphrase_w = diceware_generator(dictionary, keys_list, N_words)
                gen_test = (len(passphrase_w)>100) #check the limit of the 100 characters, counting the spaces as characters for security. If false : new try in the loop.
                on_built_test = gen_test
                if  (on_built_test ==  True) & (time.time()-time_start > dtime_max): #to avoid too much calculations
                    print("Error : too long to be calculated. Please try a smaller number of words or check the "+dictionary_path+" file by comparing with the list on website : https://theworld.com/%7Ereinhold/diceware.wordlist.asc\n")
                    break
        else :
            passphrase_w = diceware_generator(dictionary, keys_list, N_words)
            on_built_test = False
    return passphrase_w

# Utilitarian function : miscellaneous =====================================================

def ask_new_passphrase():
    ask_test = True
    while ask_test:
        ask = input("Do you want a new passphrase ? Y for yes, N to quit")
        if (ask == 'Y') | (ask == 'y') | (ask == 'Yes') | (ask == 'yes') | (ask == 'YES'):
            return True
        elif (ask == 'N') | (ask == 'n') | (ask == 'No') | (ask == 'no') | (ask == 'NO'):
            return False
        elif (ask == 'quit') | (ask == 'QUIT') | (ask == 'Quit'):
            return False

# Main function : core of the program ======================================================

def main():
    lines = file_loading(dictionary_path) #data laoding
    output_write(errorfile_path,new_run=True,error_len=len(lines))
    if type(lines) == bool:
        return
    dictionary = dictionary_creation(lines) #dictionary creation
    dictionary_check = check_dictionary(dictionary) #We keep returning integers from return method for a developing/debbuging issue, even if we do not exhibit the value of check
    if dictionary_check == False:
        return
    max_words = check_length_words(dictionary)
    print("You can quit the program at any time by entering 'quit' as an answer for any question\n")
    stay_test = True
    while stay_test:
        passphrase_w = passphrase_generator(dictionary,max_words)
        if type(passphrase_w) == bool: #quit option asked
            return
        stay_test = ask_new_passphrase()
    #print(passphrase_w)
    return passphrase_w

# Execute main function to generate a passphrase ===========================================

#global variables
dictionary_path = 'diceware.wordlist.asc' # dictionary path
errorfile_path = 'ErrorWarning.txt'       # error file path
max_words_fixed = 15                      # maximum number of words, without any concern on the 100-characters limit

#execution
main()