# cryptobook
I have, for some reason, been thinking about being able to securely communicate ever since early November 2024. People much smarter than me have written all manner of secure, mathy encryption techniques. I don't feel the needd to try to learn all that math just to do something that's been done already. But then I remembered something I read in a book many years ago where the characters exchanged encyprted messages by looking looking for each word they wanted to encode in a book and writing down the page, line, and position on the line of the word they wanted to include in the message. eg, I just picked up a book and on page 266, line 6 word 3 we see the word "and". So as long as my correspondent and I agree on what book we're using, we can exchange groups of number triplets and communicate with one another without anyone who doesn't know what book we're using to decode the messages.

Cryptobook takes that idea and modifies it for the internet age. It reads in a text file (say a book downloaded from [Project Gutenberg](https://www.gutenberg.org/)) and constructs a dictionary keyed on each unique character found in the book with values that lists of the indices in the file where that letter is found. It then runs through the plaintext message character by character, looks up the list of indices of that character and selects one at random from the list and adds it to the cyphertext version of the file. That cyphertext can be passed on to the recipient and they can read in the same text file and look up the characters at each index in the cyphertext to produce the plaintext version of the message.

Is this the most secure method to encrypt/decrypt messages? No. But it is simple and as long as someone who intercepts the message doesn't know what text file was used to produce the indices, it is not crackable mathematically. Cryptobook is command line utility that can be executed like this:
```
./cryptobook.py -b <path to the book file> -i <path to the plaintext> -o <path to the encrypted file> --encrypt
```
or
```
./cryptobook.py -b <path to the book file> -i <path to the encyrpted message> -o <path to the decrypted file> --decrypt
```

The main weakness of cryptobook is that the people on each end of the conversation need to have a secure way to agree on the book to use as the basis of the encryption, but that's a small piece of information to exchange that can be done face-to-face.

Another weakness of sending encrypted messages over the internet is that exchaning files that are just lots of numbers looks like you're trying to encrypt you communication and could raise flags. That's where my repo thagomizer comes in. It uses steganography to embed lists of integers into tiff or png files that can then be extracted to reveal the list of numbers which cryptobook can decrypt. Thagomizer can handles messages up to 65,536 characters long and can handle character indices up to 16,777,216 (ie, the length of the book file).
