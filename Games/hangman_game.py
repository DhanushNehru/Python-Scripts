import random


word_list = [
    'wares',
    'soup',
    'mount',
    'extend',
    'brown',
    'expert',
    'tired',
    'humidity',
    'backpack',
    'crust',
    'dent',
    'market',
    'knock',
    'smite',
    'windy',
    'coin',
    'throw',
    'silence',
    'bluff',
    'downfall',
    'climb',
    'lying',
    'weaver',
    'snob',
    'kickoff',
    'match',
    'quaker',
    'foreman',
    'excite',
    'thinking',
    'mend',
    'allergen',
    'pruning',
    'coat',
    'emerald',
    'coherent',
    'manic',
    'multiple',
    'square',
    'funded',
    'funnel',
    'sailing',
    'dream',
    'mutation',
    'strict',
    'mystic',
    'film',
    'guide',
    'strain',
    'bishop',
    'settle',
    'plateau',
    'emigrate',
    'marching',
    'optimal',
    'medley',
    'endanger',
    'wick',
    'condone',
    'schema',
    'rage',
    'figure',
    'plague',
    'aloof',
    'there',
    'reusable',
    'refinery',
    'suffer',
    'affirm',
    'captive',
    'flipping',
    'prolong',
    'main',
    'coral',
    'dinner',
    'rabbit',
    'chill',
    'seed',
    'born',
    'shampoo',
    'italian',
    'giggle',
    'roost',
    'palm',
    'globe',
    'wise',
    'grandson',
    'running',
    'sunlight',
    'spending',
    'crunch',
    'tangle',
    'forego',
    'tailor',
    'divinity',
    'probe',
    'bearded',
    'premium',
    'featured',
    'serve',
    'borrower',
    'examine',
    'legal',
    'outlive',
    'unnamed',
    'unending',
    'snow',
    'whisper',
    'bundle',
    'bracket',
    'deny',
    'blurred',
    'pentagon',
    'reformed',
    'polarity',
    'jumping',
    'gain',
    'laundry',
    'hobble',
    'culture',
    'whittle',
    'docket',
    'mayhem',
    'build',
    'peel',
    'board',
    'keen',
    'glorious',
    'singular',
    'cavalry',
    'present',
    'cold',
    'hook',
    'salted',
    'just',
    'dumpling',
    'glimmer',
    'drowning',
    'admiral',
    'sketch',
    'subject',
    'upright',
    'sunshine',
    'slide',
    'calamity',
    'gurney',
    'adult',
    'adore',
    'weld',
    'masking',
    'print',
    'wishful',
    'foyer',
    'tofu',
    'machete',
    'diced',
    'behemoth',
    'rout',
    'midwife',
    'neglect',
    'mass',
    'game',
    'stocking',
    'folly',
    'action',
    'bubbling',
    'scented',
    'sprinter',
    'bingo',
    'egyptian',
    'comedy',
    'rung',
    'outdated',
    'radical',
    'escalate',
    'mutter',
    'desert',
    'memento',
    'kayak',
    'talon',
    'portion',
    'affirm',
    'dashing',
    'fare',
    'battle',
    'pupil',
    'rite',
    'smash',
    'true',
    'entrance',
    'counting',
    'peruse',
    'dioxide',
    'hermit',
    'carving',
    'backyard',
    'homeless',
    'medley',
    'packet',
    'tickle',
    'coming',
    'leave',
    'swing',
    'thicket',
    'reserve',
    'murder',
    'costly',
    'corduroy',
    'bump',
    'oncology',
    'swatch',
    'rundown',
    'steal',
    'teller',
    'cable',
    'oily',
    'official',
    'abyss',
    'schism',
    'failing',
    'guru',
    'trim',
    'alfalfa',
    'doubt',
    'booming',
    'bruised',
    'playful',
    'kicker',
    'jockey',
    'handmade',
    'landfall',
    'rhythm',
    'keep',
    'reassure',
    'garland',
    'sauna',
    'idiom',
    'fluent',
    'lope',
    'gland',
    'amend',
    'fashion',
    'treaty',
    'standing',
    'current',
    'sharpen',
    'cinder',
    'idealist',
    'festive',
    'frame',
    'molten',
    'sill',
    'glisten',
    'fearful',
    'basement',
    'minutia',
    'coin',
    'stick',
    'featured',
    'soot',
    'static',
    'crazed',
    'upset',
    'robotics',
    'dwarf',
    'shield',
    'butler',
    'stitch',
    'stub',
    'sabotage',
    'parlor',
    'prompt',
    'heady',
    'horn',
    'bygone',
    'rework',
    'painful',
    'composer',
    'glance',
    'acquit',
    'eagle',
    'solvent',
    'backbone',
    'smart',
    'atlas',
    'leap',
    'danger',
    'bruise',
    'seminar',
    'tinge',
    'trip',
    'narrow',
    'while',
    'jaguar',
    'seminary',
    'command',
    'cassette',
    'draw',
    'anchovy',
    'scream',
    'blush',
    'organic',
    'applause',
    'parallel',
    'trolley',
    'pathos',
    'origin',
    'hang',
    'pungent',
    'angular',
    'stubble',
    'painted',
    'forward',
    'saddle',
    'muddy',
    'orchid',
    'prudence',
    'disprove',
    'yiddish',
    'lobbying',
    'neuron',
    'tumor',
    'haitian',
    'swift',
    'mantel',
    'wardrobe',
    'consist',
    'storied',
    'extreme',
    'payback',
    'control',
    'dummy',
    'influx',
    'realtor',
    'detach',
    'flake',
    'consign',
    'adjunct',
    'stylized',
    'weep',
    'prepare',
    'pioneer',
    'tail',
    'platoon',
    'exercise',
    'dummy',
    'clap',
    'actor',
    'spark',
    'dope',
    'phrase',
    'welsh',
    'wall',
    'whine',
    'fickle',
    'wrong',
    'stamina',
    'dazed',
    'cramp',
    'filet',
    'foresee',
    'seller',
    'award',
    'mare',
    'uncover',
    'drowning',
    'ease',
    'buttery',
    'luxury',
    'bigotry',
    'muddy',
    'photon',
    'snow',
    'oppress',
    'blessed',
    'call',
    'stain',
    'amber',
    'rental',
    'nominee',
    'township',
    'adhesive',
    'lengthy',
    'swarm',
    'court',
    'baguette',
    'leper',
    'vital',
    'push',
    'digger',
    'setback',
    'accused',
    'taker',
    'genie',
    'reverse',
    'fake',
    'widowed',
    'renewed',
    'goodness',
    'featured',
    'curse',
    'shocked',
    'shove',
    'marked',
    'interact',
    'mane',
    'hawk',
    'kidnap',
    'noble',
    'proton',
    'effort',
    'patriot',
    'showcase',
    'parish',
    'mosaic',
    'coil',
    'aide',
    'breeder',
    'concoct',
    'pathway',
    'hearing',
    'bayou',
    'regimen',
    'drain',
    'bereft',
    'matte',
    'bill',
    'medal',
    'prickly',
    'sarcasm',
    'stuffy',
    'allege',
    'monopoly',
    'lighter',
    'repair',
    'worship',
    'vent',
    'hybrid',
    'buffet',
    'lively']



def get_word():
    word = random.choice(word_list)
    return word.upper()

def play(word):
   word_completion = "_" * len(word)
   guessed = False
   guessed_letters = []
   guessed_words = []
   tries = 6
   print("Let's play Hangman!")
   print(display_hangman(tries))
   print(word_completion) 
   print("\n")
    
   while not guessed and tries > 0:
      guess = input("Please guess a letter or word:").upper()
      if len(guess) == 1 and guess.isalpha():
         if guess in guessed_letters:
            print("You have already guessed this letter : ", guess)   
         
         elif guess not in word:
            print(guess, "is not in the word.")
            tries = tries - 1
            guessed_letters.append(guess)
            
         else:
            print("Good job !", guess, "is in the word.")
            guessed_letters.append(guess)
            word_as_list = list(word_completion)     #Find all instances where guess appears in the word so we first convert that into a list
            indices = [i for i, letter in enumerate(word) if letter == guess]
            for index in indices:
               word_as_list[index] = guess
            word_completion = "". join(word_as_list)
            if "_" not in word_completion:
               guessed = True
         
        
      elif len(guess) == len(word) and guess.isalpha():
         if guess in guessed_words:
            print("you already guessed this word !")
            
         elif guess != word:
            print(guess, "is not the word")
            tries = tries - 1
            guessed_words.append(guess)
         else:
            guessed = True
            word_completion = word
           
      
      else:
         print("Not a valid guess!")
      
      print(display_hangman(tries))
      print(word_completion)
      print("\n")
   
   if guessed :
      print("Congrats, yoiu guessed the word You win.")
   else:
      print("sorry you ran out of tries. The word was " + word + " Maybe next time")
      
def display_hangman(tries):
    stages = [  # final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # head
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[tries]
 
 
def main():
   word = get_word()
   play(word)
   while input("Play again ? (Y/N) ").upper() == "Y":
      word = get_word()
      play(word)
      
      
if __name__ == "__main__" :      #our program will run by running our script on the command line
   main()