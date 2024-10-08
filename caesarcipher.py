#this program is a simple caesar cipher, which encrypts
#a message by shifting each letter three to the right in the alphabet
#this will ignore all characters that are not letters

def caesar_encrypt(plaintext):
    #each letter in plaintext
    finalstring= ""
    for letter in plaintext.lower():
        #get the number value of the letter
        cipher = (ord(letter)+3)
        #wraparound
        #checks letter to see if it's out of range
        if cipher > 122:
            cipher -= 26
            finalstring += chr(cipher)
        #skips any other characters
        elif (ord(letter)) in range (97,123):
            finalstring +=chr(cipher)
        else: 
            continue
    return(finalstring)