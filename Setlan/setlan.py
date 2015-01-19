#!/usr/bin/env python
# -*- coding: utf-8 -*-'''

import expresiones


expresiones.analizador.input("program 1ola\nint 1a1")

for token in expresiones.analizador:
    print(token)