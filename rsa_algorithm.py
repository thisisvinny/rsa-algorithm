"""
Write a program to implement the RSA algorithm for cryptography.

Set up:

Choose two large primes, p and q. (There are a number of sites on-line where you can find large primes.)
Compute n = p * q, and Φ = (p-1)(q-1).
Select an integer e, with 1 < e < Φ , gcd(e, Φ) = 1.
Compute the integer d, 1 < d < Φ such that ed ≡ 1 (mod Φ). The numbers e and d are called inverses (mod Φ). To do this, I suggest two possibilities:
Research the BigInteger class in Java. It has a method to compute inverses modulo a specified number. (It also has other methods that would be useful!)
Look up the Extended Euclidean Algorithm. This is an algorithm to find d. Save this number d in a constant or variable.
(Make n and e public)
Encryption:

Convert the message into numbers, using the ASCII representation for characters. (For example, in ASCII, A = 65, B = 66, ... , space = 32, period = 46. You may find an ASCII table online.)
Obtain the public key (n, e) of who you want to send a message to. (You should choose yourself for testing purposes. Then try a classmate's.)
Encipher each letter (now a number, say m) by computing c ≡ me (mod n).
Decryption:

When you receive a string of numbers, such as 1743 452 625, use your private key d to compute 1743d (mod n), 452d (mod n) and 625d (mod n). This n is from your public key.
Take the results of these and translate back into letters, using the same scheme as above.
"""

#Vincent Yu
#RSA Algorithm

import math
import random

#determines if n is a prime number
def isPrime(n):
	if n == 0 or n == 1:
		return False
	else:
		#loops until you find a number that evenly divides into n
		for i in range(2, int(math.sqrt(n)) + 1):
			if n%i == 0:
				return False
	return True

#generates the prime numbers up to n
def generatePrimes(n):
	listPrimes = []
	for i in range(0,n):
		if isPrime(i) == True:
			listPrimes.append(i)
	return listPrimes

#gcd function
def gcd(a,b):
	if a==0:
		return b
	else:
		return gcd(b%a, a)

#get first instance of a valid e, starting at p+q+1
def selectE(p,q,phi):
	e = p+q + 1
	while(gcd(e, phi) != 1):
		e = e + 1
	return e

#compute d, the inverse of e mod phi
#if d is neg, add phi (computed later)
def computeD(e, phi, t, t2):
	r = phi
	r2 = e
	if r2 == 0:
		if r>1:
			return "e is not invertible"
		else:
			return t
	q = r // r2
	return computeD(r-q*r2, r2, t2, t-q*t2)

#encrypt
def encrypt(s, e, n):
	i=0
	encrypted = ""
	while i != len(s):
		encrpytLetter = ord(s[i]) ** e % n
		encrypted += str(encrpytLetter) + " "
		i+=1
	return encrypted


#decrypt
def decrypt(s, d ,n):
	i=0
	decrpyted = ""
	s2 = s.split() #split each letter by white space
	while i != len(s2):
		decrpytLetter = int(s2[i])**d % n
		decrpyted += chr(decrpytLetter)
		i+=1
	return decrpyted

def main():
	userInput = str(input("Would you like to encrypt(e), encrypt with someone else's keys(ee), decrypt(d), generate new keys(g), or exit(x)?\n"))
	#encrypt with previously generated keys
	if userInput == "e":
		readPublicKeys = open("PublicKeys.txt", "r")
		e = int(readPublicKeys.readline().split(" ")[1])
		n = int(readPublicKeys.readline().split(" ")[1])
		toEncrypt = str(input("What is your message you are encrypting?\n"))
		encrypted = encrypt(toEncrypt, e, n)
		print("Your encrypted message is: " + encrypted)
	#encrypt with someone else's keys
	elif userInput == "ee":
		e = int(input("What is the other person's e?\n"))
		n = int(input("What is the other person's n?\n"))
		toEncrypt = str(input("What is your message you are encrypting?\n"))
		encrypted = encrypt(toEncrypt, e, n)
		print("Your encrypted message is: " + encrypted)
	#decrypt
	elif userInput == "d":
		readPrivateKeys = open("PrivateKeys.txt", "r")
		d = int(readPrivateKeys.readline().split(" ")[1])
		n = int(readPrivateKeys.readline().split(" ")[1])
		toDecrypt = str(input("What is the message you are decrypting?\n"))
		decrypted = decrypt(toDecrypt, d, n)
		print("Your decrypted message is: " + decrypted)
	#generate keys
	elif userInput == "g":
		listPrimes = generatePrimes(1000)
		#p and q are 2 random prime numbers less than 1000
		p = listPrimes[random.randrange(0,len(listPrimes))]
		q = listPrimes[random.randrange(0,len(listPrimes))]
		#generate n, phi, e, d 
		n = p*q
		phi = (p-1)*(q-1)
		e = selectE(p,q,phi)
		d = computeD(e,phi,0,1)
		if d<0:
			d = d+phi
		#write public (e,n) and private (d,n) keys into files for encrypting and decrypting
		writePublicKeys = open("PublicKeys.txt", "w")
		writePublicKeys.write("e: " + str(e) + "\nn: " + str(n))
		writePrivateKeys = open("PrivateKeys.txt", "w")
		writePrivateKeys.write("d: " + str(d) + "\nn: " + str(n))
	#exit
	elif userInput == "x":
		pass
	#invalid response
	else:
		print("You did not enter a valid option. Try again.")
		main()

main()

