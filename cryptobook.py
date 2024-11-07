#! /usr/bin/env python

import os
import random
import textwrap

import click

@click.command()
@click.argument('book', type=click.File('r'))
@click.argument('input', type=click.File('r'))
@click.argument('output', type=click.Path(exists=False))
@click.option('--encrypt', is_flag=True)
@click.option('--decrypt', is_flag=True)
def cryptobook(book, input, output, encrypt, decrypt):
    if encrypt and decrypt:
        print("You can't encrypt and decrypt at the same time")
        return
    if not decrypt and not encrypt:
        print("You must select either decrypt or encrypt")

    if os.path.isfile(output):
        # It seems like exists=False should throw an error if the output file exists
        # but it doesn't so check here and get out if it does
        print("Hey the output file already exists!")
        return

    book_str = book.read()

    if encrypt:
        book_dict = read_book(book_str)
        encrypt_message(input, output, book_dict)

    if decrypt:
        decrypt_message(input, output, book_str)


def read_book(book):
    bd = {}
    for i, c in enumerate(book):
        try:
            bd[c].append(i)
        except KeyError:
            bd[c] = [i]
    return bd


def encrypt_message(input_file, output_name, book):
    message = input_file.read()
    cypher_list = []
    for c in message:
        number = book[c][random.randint(0, len(book[c]) - 1)]
        cypher_list.append(str(number))
    cypher_str = ' '.join(cypher_list)
    with open(output_name, 'w') as outf:
        outf.write(textwrap.fill(cypher_str, width=80))


def decrypt_message(input_file, output_name, book):
    message = input_file.read()
    numbers = [int(x) for x in message.split()]
    message = ''
    for n in numbers:
        c = book[n]
        message += c

    with open(output_name, 'w') as outf:
        outf.write(message)


if __name__ == '__main__':
    cryptobook()

