import pathlib
import sys

LETTERS_DICT = {' ': (' ' * 12 + '\n') * 6, 'a': """
    ___    
   /   |   
  / /| |   
 / ___ |   
/_/  |_|
 
""", 'b': """
    ____   
   / __ )  
  / __  |  
 / /_/ /   
/_____/    
           
""", 'c': """
   ______  
  / ____/  
 / /       
/ /___     
\____/     
           
""", 'd': """
    ____   
   / __ \  
  / / / /  
 / /_/ /   
/_____/    
           
""", 'e': """
    ______ 
   / ____/ 
  / __/    
 / /___    
/_____/    
           
""", 'f': """
    ______ 
   / ____/ 
  / /_     
 / __/     
/_/        
           
""", 'g': """
   ______  
  / ____/  
 / / __    
/ /_/ /    
\____/     
           
""", 'h': """
    __  __ 
   / / / / 
  / /_/ /  
 / __  /   
/_/ /_/    
           
""", 'i': """
    ____   
   /  _/   
   / /     
 _/ /      
/___/      
           
""", 'j': """
       __  
      / /  
 __  / /   
/ /_/ /    
\____/     
           
""", 'k': """
    __ __  
   / //_/  
  / ,<     
 / /| |    
/_/ |_|    
           
""", 'l': """
    __     
   / /     
  / /      
 / /___    
/_____/    
           
""", 'm': """
    __  ___
   /  |/  /
  / /|_/ / 
 / /  / /  
/_/  /_/   
           
""", 'n': """
    _   __ 
   / | / / 
  /  |/ /  
 / /|  /   
/_/ |_/    
           
""", 'o': """
   ____    
  / __ \   
 / / / /   
/ /_/ /    
\____/     
           
""", 'p': """
    ____   
   / __ \  
  / /_/ /  
 / ____/   
/_/        
           
""", 'q': """
   ____    
  / __ \   
 / / / /   
/ /_/ /    
\___\_\    
           
""", 'r': """
    ____   
   / __ \  
  / /_/ /  
 / _, _/   
/_/ |_|    
           
""", 's': """
   _____   
  / ___/   
  \__ \    
 ___/ /    
/____/     
           
""", 't': """
  ______  
 /_  __/  
  / /     
 / /      
/_/       
           
""", 'u': """
   __  __  
  / / / /  
 / / / /   
/ /_/ /    
\____/     
           
""", 'v': """
 _    __   
| |  / /   
| | / /    
| |/ /     
|___/      
           
""", 'w': """
 _       __
| |     / /
| | /| / / 
| |/ |/ /  
|__/|__/   
           
""", 'x': """
   _  __   
  | |/ /   
  |   /    
 /   |     
/_/|_|     
           
""", 'y': """
__  __     
\ \/ /     
 \  /      
 / /       
/_/        
           
""", 'z': """
 _____     
/__  /     
  / /      
 / /__     
/____/     
           
""", '0': """
   ____   
  / __ \  
 / / / /  
/ /_/ /   
\____/    
          
""", '1': """
   ___    
  <  /    
  / /     
 / /      
/_/       
          
""", '2': """
   ___    
  |__ \   
  __/ /   
 / __/    
/____/    
          
""", '3': """
   _____  
  |__  /  
   /_ <   
 ___/ /   
/____/    
          
""", '4': """
   __ __  
  / // /  
 / // /_  
/__  __/  
  /_/     
          
""", '5': """
    ______
   / ____/
  /___ \  
 ____/ /  
/_____/   
          
""", '6': """
   _____  
  / ___/  
 / __ \   
/ /_/ /   
\____/    
          
""", '7': """
 _____    
/__  /    
  / /     
 / /      
/_/       
          
""", '8': """
   ____   
  ( __ )  
 / __  |  
/ /_/ /   
\____/    
          
""", '9': """
   ____   
  / __ \  
 / /_/ /  
 \__, /   
/____/    
          
"""}


def get_letters_map(string: str):
    """
    Takes a string and maps it to individual ASCII art letters.
    :param string: The string to convert.
    :return: An array of strings representing ASCII art.
    """
    ascii_art_letters = list(map(lambda letter: (LETTERS_DICT[letter.lower()]), string))
    return ascii_art_letters


def string_to_ascii_art(string: str) -> str:
    """
    Takes a string and converts it to ASCII art style big letters.
    :param string: The string to convert.
    :return: The converted string.
    """
    ascii_art = ''
    for word in string.split():
        letters = get_letters_map(word)
        for i in range(5):
            # maybe rstrip and rjust to the longest line
            ascii_art += ''.join([letter.splitlines()[i + 1].rjust(11) for letter in letters]) + '\n'
        ascii_art += '\n'
    return ascii_art


def print_intro(description: str, script_name=pathlib.Path(sys.argv[0]).name[:-3]):
    """
    Prints an introduction to the script, mainly meant for interactive shells.
    :param description: The description of the script.
    :param script_name: The name of script, by default is taken from the name of the file.
    :return:
    """
    print(string_to_ascii_art(script_name))
    print(description)
