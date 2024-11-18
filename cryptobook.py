#! /usr/bin/env python

from collections.abc import KeysView
import os
import random
import textwrap

import click

class MissingCharacterException(Exception):
    """
    This exception is raised when a character in the message to be encyrpted
    is not in the text of the book being used for the encryption.
    """
    def __init__(self, msg):
        self.message = msg


@click.command()
@click.argument('book', type=click.File('r'))
@click.argument('input', type=click.File('r'))
@click.argument('output', type=click.Path(exists=False))
@click.option('--encrypt', is_flag=True)
@click.option('--decrypt', is_flag=True)
def cryptobook(book, input, output, encrypt, decrypt):
    """
    The main part of the program

    Arguments:
        book - a readable click.File object that points to the book that is
               being used as the basis for the encyrption
        input - a readable click.File object that points to the message that
                is being encrypted or decrypted
        output - a click.Path object into which the output of the encyrption
                 or decryption will be saved. It uses exists=False, but this
                 doesn't seem to work, so a manual check for the existence of
                 the file is made
        encrypt - a flag that indicates the input message should be encrypted
        decrypt - a flag that indicates the input message should be decrypted
    """
    if encrypt and decrypt:
        print("You can't encrypt and decrypt at the same time")
        return
    if not decrypt and not encrypt:
        print("You must select either decrypt or encrypt")

    if os.path.isfile(output):
        # It seems like exists=False should throw an error if the output file exists
        # but it doesn't so, check here and get out if it does
        print("Hey the output file already exists!")
        return

    book_str = book.read()

    if encrypt:
        book_dict = read_book(book_str)
        encrypt_message(input, output, book_dict)

    if decrypt:
        decrypt_message(input, output, book_str)


def read_book(book:str) -> dict[str:list[int]]:
    """
    Takes the text of the book and constructs a dictionary keyed on each
    character found with values that are the list of all the indices where that
    character is found

    Arguments:
        book - a string containing the text of the book
    
    Returns: the dictionary described above
    """
    bd = {}
    for i, c in enumerate(book):
        try:
            bd[c].append(i)
        except KeyError:
            bd[c] = [i]
    return bd


def encrypt_message(input_file: click.File, output_name: click.Path, book: dict[str:list[int]]) -> None:
    """
    Takes the message to be encrypted and for each character finds a random
    location in the book where that character is found. The character indices
    are written in order to output file.

    Arguments:
        input_file - a readable click.File object containing the message to be
                     encrypted
        output_name - the path of the output file that will be created.
        book - a dictionary keyed on every character in the book with values
               that are lists of the indices where each character is found
    
    Returns: N/A

    Raises:
        MissingCharacterException - if there is a character in the message that
                                    isn't in the book
    """
    message = input_file.read()
    check_message(message, book.keys())

    cypher_list = []
    for c in message:
        # Get a random index where character is found in the book
        number = book[c][random.randint(0, len(book[c]) - 1)]
        cypher_list.append(str(number))

    cypher_str = ' '.join(cypher_list)
    with open(output_name, 'w') as outf:
        outf.write(textwrap.fill(cypher_str, width=80))


def decrypt_message(input_file: click.File, output_name: click.Path, book: str) -> None:
    """
    Takes and encrypted message (ie, a list of integers) and looks up the
    character at each of those indices to reconstruct the plain text message

    Arguments:
        input_file - a readable click.File object containing the encrypted
                     message
        output_name - a click.Path pointing to where the plaintext should be
                      saved
        book - a string containing the text of the book used for the encryption
    
    Returns: N/A
    """
    message = input_file.read()
    numbers = [int(x) for x in message.split()]
    message = ''
    for n in numbers:
        c = book[n]
        message += c

    with open(output_name, 'w') as outf:
        outf.write(message)


def check_message(msg: str, book_keys: KeysView) -> None:
    """
    Ensures that every character in the message being encrypted can be found
    in the text of the book

    Arguments:
        msg - a string containing the message being encrypted
        book_keys - the keys from the book dictionary, ie, all the characters
                    used in the book

    Returns: N/A

    Raises:
        MissingCharacterException - if there is at least one character in the
                                    message that isn't in the book
    """
    msg_chars = set(msg)
    book_set = set(book_keys)
    missing_chars = msg_chars.difference(book_set)
    if missing_chars:
        missing_chars = ', '.join(list(missing_chars))
        raise MissingCharacterException(f"The following characters are not in the book: {missing_chars}")


if __name__ == '__main__':
    cryptobook()

