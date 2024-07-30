# README DICEWARE PASSPHRASE GENERATOR

This program generates a passphrase for security. It uses the principle of the Diceware Passphrase Generator (https://theworld.com/~reinhold/diceware.html) which combine "keys" as digits with "words". The words are chosen randomly from the list by a random choice on the digital "keys". This list is provided by the 'diceware.wordlist.asc' file lying in the same folder as the program. Usually, digits and words of a same couple are separated by tabulation, and couples by carriage return. This algorithm can handle some minor deviations from this format.

## Program Building

If the program has been correctly downloaded from the Github deposite, the program is already built. The executable application can be found in the main folder as DicewarePassphraseGenerator.exe. This program has been compiled via the PyInstaller module for Python on Windows machine. It can be executed on Linux machine with 'wine' method. Check the Program Execution part.

If you do not find the executable file in the main folder, copy the DicewarePassphraseGenetero.exe file from dist\ folder to the main folder. For that purpose, move to the main folder and enter in terminal :
cp dist\DicewarepassphraseGenerator.exe .

To be built from the Python file, this program requires to have both Python and the PyInstaller package already installed on the machine. Compilation is then performed by entering in the terminal the following instructions : py -m PyInstaller --onefile DicewarePassphraseGenerator.py
You must then copy the DicewarePassphraseGenetero.exe file from dist\ folder to the main folder. For that purpose, move to the main folder and enter in terminal :
cp dist\DicewarepassphraseGenerator.exe .     (Windows)
cp dist\DicewarepassphraseGenerator .         (Linux)


## Program Execution

To be executed, the application requires to have the file 'diceware.wordlist.asc' in the same folder as the code the user are executing. This file is already present if the user downloaded the program from the Github deposite. If missing, or if corrupted, the user can download it directly from the following website : https://theworld.com/%7Ereinhold/diceware.wordlist.asc

The program can be executed by entering the following instructions in the terminal, while being in the main folder, then pressing Enter :

DicewarePassphraseGenerator.exe          (Windows)
wine DicewarePassphraseGenerator.exe     (Linux)

If you compiled yourself the program on a Linux machine, execute the program by entering the following sntructions while being in the main folder :

DicewarePassphraseGenerator

## Program Specifications

While using the program, the user will be asked to choose if the passphrase should respect the common rule on passphrases and password length (ie: being shorter than 100 characters). Enter on command either Y for yes (recommanded choice) or N for no (if the user can accept a longer passphrase). The user then will be asked about the number of words required to build the passphrase. Enter the desired number of words on terminal. 0 or negative number will result in an error message (no passphrase or password can be generated without any word) and 1 with an warning message (1 word is for password and not passphrase). A maximum number of words is stated by the algorithm, based on the characters' limit (if relevant) and the size of the list provided by the 'diceware.wordlist.asc' file. It cannot be exceeded.

The user can quit the program at any moment by entering 'quit' as an answer to any question. Once the program has generated a passphrase, it will ask the user about generating a new one or leaving. The user can then stop by entering 'quit' or 'no' as an answer.

Several error or warning messages are encrypted in the program. They tend to drag the user to the source of the problem, or explicit the risk of lack of robustness due to some corruption on the 'diceware.wordlist.asc' file. Such problems can be solve by accessing to the website and downloading the source file again. In particular, if the user chooses to restrict the number of characters while a warning message has warned about the huge length of the words present in the file, it might force the algorithm to take up to 1 minute to search a solution. At this stage, if it fails, the user will be invited to try another option. Whatever the outcome, in such case, we invite the user to check on the 'diceware.wordlist.asc' file, that might be corrupted. Keep in mind that the program is able to deal with minor corruption, but that major corruption of the 'diceware.wordlist.asc' file may result in downgrade of the quality of the passphrase.

The program also includes a routine to generate or update an error file named ErrorWarning.txt. This file gathers the different warning and error messages, plus other informations that could be useful to track issues and a potential corruption of the file. It includes systematically the total number of lines of the 'diceware.wordlist.asc' file during the last run of the program and may add the index of empty lines, the index of incorrect lines with a non-readable format (which might include header or footer if any) and the median length of the words if the words are mainly very large.