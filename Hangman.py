from os import truncate
import random

HANGMAN_PHOTOS = {
1:  
r"""
    x-------x

""", 
2:
r"""
    x-------x
    |       |
    |       0
    |
    |
    |
""", 
3:
r"""
    x-------x
    |       |
    |       0
    |       |
    |
    |
""",
4:
r"""
    x-------x
    |       |
    |       0
    |      /|\
    |
    |
""",
5:
r"""
    x-------x
    |       |
    |       0
    |      /|\
    |      / 
    |
""",
6:
r"""
    x-------x
    |       |
    |       0
    |      /|\
    |      / \
    |
"""
}
HANGMAN_ASCII_ART = (r"""Welcome to Hangman!
    _    _
   | |  | |
   | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
   |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_  \
   | |  | | (_| | | | | (_| | | | | | | (_| | | | |
   |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                        __/ |
                       |___/
""")
MAX_TRIES = 6

old_letters_guessed = []

def check_valid_input(letter_guessed: str, old_letters_guessed: list) -> bool:
    """ checks if the user entered a valid input
    :param letter_guessed: the letter that the user guessed
    :param old_letters_guessed: a list of the old letters that the user had already guessed and are valid
    :return: true if the input is valid (only one character, in english and wasn't typed before)
    """
    if len(letter_guessed) == 1 and letter_guessed.isalpha() == True and letter_guessed not in old_letters_guessed:
        return True
    else:
        return False
 
def try_update_letter_guessed(letter_guessed: str, old_letters_guessed: list) -> bool:
    """ If the character is valid, adds him to the list of the old letters guessed and prints the letter in lowercase 
    else, prints X
    :param letter_guessed: the letter that the user guessed
    :param old_letters_guessed: a list of the old letters that the user had already guessed and are valid
    :type letter_guessed: String
    :type old_letters_guessed: List
    :return: true if the input was added to the list successfully 
    :rtype: Boolean 
    """
    #TODO - הבדיקה אם התו נמצא ברשימה לא טובה , תו המוקלד באותיות קטנות לא שווה לתו המוקלד באותיות גדולות
    if check_valid_input(letter_guessed, old_letters_guessed):
        # case of a valid input
        old_letters_guessed.append(letter_guessed)
        
        # adding the guessed letter to the list of the guessed letters so far 
        return True

    else: 
        print("\n\tX\n\n\tPlease make sure you typed a single letter in English that wasn't typed before" + 
        "\n\n\tletters guessed so far :" + " -> ".join(sorted(old_letters_guessed)))
        return False


def show_hidden_word(secret_word: str, old_letters_guessed: list) -> str:
    """
    updates the visual of the user with the letters that he had guessed right
    :param secret_word: the word that the user need to guess
    :param old_letter_guessed: a list of the old letters that the user had already guessed and are valid
    :rtype secret_word: string
    :rtype old_letter_guessed: list 
    :return: the user visual of the secret word, with '_' as what he didn't guess.
    :rtype: string
    """
    updated_string = ''
    for char in secret_word:
        if char in old_letters_guessed:
            updated_string = updated_string + char + ' '
        else:
            updated_string = updated_string + '_ '
    
    return updated_string[:-1]
    # in order to uninclude to last backspace

def check_win(secret_word: str, old_letters_guessed: list) -> bool:
    """
    checks if all the letters of the secret words has been discovered
    :param secret_word: the word that the user need to guess
    :param old_letter_guessed: a list of the old letters that the user had already guessed and are valid
    :rtype secret_word: string
    :rtype old_letter_guessed: list 
    :return: true if the secret word has been discovered, else, false
    :rtype: boolean
    """
    if secret_word == show_hidden_word(secret_word, old_letters_guessed).replace(' ',''):
        return True
    return False

def print_hangman(num_of_tries: int) -> dict[int, str]:
    """
    Prints an ascii art of a hangman according to the number of tries
    :param num_of_tries: number of wrong tries of guessing a letter
    :return: a photo out of the dictionary
    """
    return HANGMAN_PHOTOS[num_of_tries]

def choose_word(file_path: str, index: int) -> tuple[int, str]:
        """"Chooses a word for the user that will be the secret word, out of a text file called words.txt
        :param file_path: the file path of words.txt
        :param index: an integer the represents the location of a certain word

        :return: number of DIFFERENT words in the file, a word in the location of the argument index, that will be the secret word
        :rtype: tuple
        """
        with open(file_path, 'r') as words_file:
            words_text = words_file.read()
    
        words_list = list(dict.fromkeys(words_text.split(' ')))
        word = words_list[(len(words_list) % int(index)) - 1]
        return len(words_list), word
    
def game(word: int) -> None:
    """
    The progression of the game
    :param word: the word that the user need to guess
    """
    num_of_tries = 1
    while not check_win(word, old_letters_guessed) and num_of_tries <= MAX_TRIES:

        letter_guessed = input("\n\nGuess a Letter: ")
        if not letter_guessed in word and check_valid_input(letter_guessed, old_letters_guessed):
            # case of guessing a wrong, valid letter
            print(":(")
            print(print_hangman(num_of_tries))
            num_of_tries = num_of_tries + 1
        
        try_update_letter_guessed(letter_guessed, old_letters_guessed)
        print("\n\t" + show_hidden_word(word, old_letters_guessed)) 

            
    if check_win(word, old_letters_guessed):
        print("\n\t\tWIN\n\n")
    else:
        print("\n\t\tLOSE\n\n")

def initiallize() -> str:
    """
    Setting up the game
    """
    print(HANGMAN_ASCII_ART)
    while True:
        file_path = input("Enter file path: ")
        index = input("Enter index: ")
        try:
            word = choose_word(file_path, index)[1]
            break
        except FileNotFoundError or OSError:
            print("Please enter a valid file path: ")
        except ValueError:
            print("Please enter a valid index: ")

    print("Let's Start!")
    print(("\n\n\t" + "_ " * int(len(word)))[0:-1])
    return word

    
def main():
    game(initiallize())

if __name__ == "__main__":
    main()     