# -*- encoding: utf-8 -*-
import re

def get_filetype_by_content(text):
    title_string = "^([a-zA-Z_]+\d*)+:([\ a-zA-Z_]+\d*,{0,1})*$"
    member_string = "^[\ ]{4}([a-z,A-Z,_]+\d*)+$"
    # TODO: terminar la expresión.
    method_string = "^[\ ]{4}([a-z,A-Z,_]+[\d,\(,\),\,,\;\:\ \"\'\=]*)+$"
    title_expresion = re.compile(title_string)
    member_expresion = re.compile(member_string)
    method_expresion = re.compile(method_string)

    for line in text.split("\n"):

        print "line:", line
        print "\ttitle:", title_expresion.match(line)
        print "\tmember:", member_expresion.match(line)
        print "\tmethod:", method_expresion.match(line)
    return ""

if __name__ == '__main__':
    text = \
"""Perro: Mascota, Animal
    nombre
    apellido
    - ladrar()
    - comer()"""

    print get_filetype_by_content(text)
