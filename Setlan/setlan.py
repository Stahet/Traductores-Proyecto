#!/usr/bin/env python
# -*- coding: utf-8 -*-'''

import ply.lex as lexi
import expresiones

analizador = lexi.lex(module = expresiones)

analizador.input("program hola\nint 1a1\n")

tokens = []

for token in analizador:  # @UndefinedVariable
    tokens.append(token.value[1])

if not expresiones.ERROR_:
    for t in tokens:
        print(t)