import random 

def hangman():
    words_list = ['eduyear', 'hangman', 'computer', 'smartphone', "laptop"]
    word = random.choice(words_list)
    turns = 10 
    guessed = ''
    valid_entry = set('abcdefghijklmnopqrstuvwxyz')
    
    while len(word)>0:
        main_word = ""
        missed = 0 
        
        for letter in word:
            if letter in guessed:
                main_word = main_word + letter 
            else:
                main_word = main_word + "_ "
                
        if main_word == word:
            print(main_word)
            print("You won !")
            break
        
        
        print('Guess the Word', main_word)
        guess = input()
        
        if guess in valid_entry:
            guessed = guess + guessed 
        else:
            print("Enter the valid character !")
            guess = input()
            
        
        if guess not in word:
            turns -= 1 
            print(f"You're left with {turns} moves")
            if turns == 9:
                print("""
                    ----------
                    """)
                
            if turns == 8:
                print("""
                    ----------
                        O
                    """)
            
            if turns == 7:
                print(
                    """
                    ----------
                        O
                        |
                    """
                )
            
            if turns == 6:
                print("""
                ----------
                    O
                    |
                   /
                """)
            
            if turns == 5:
                print("""
                    ----------
                        O
                        |
                       / \
                    """)
            
            if turns == 4:
                print("""
                    ----------
                        O/
                        |
                       / \
                    """)
            
            if turns == 3:
                print("""
                    ----------
                       \O/
                        |
                       / \
                    """)
            
            if turns ==2:
                print("""
                    ----------
                        |
                       \O/
                        |
                       / \
                    """)   
            
            if turns == 1:
                print("""
                    ----------
                        O |
                       /|\
                       / \
                    """)            
            

name = input("Enter Your name :- ")
print("Welcome ", name)
print("------------------------------")
print("Try to guess the words in less than 10 attempts.")

hangman()