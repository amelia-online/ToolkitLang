from enum import Enum

"""
    This file is part of the Toolkit interpreter.
    Copyright (C) 2023 Amelia Johnson

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
"""


class TokenType(Enum):
    String = 1,
    Number = 2,
    Ident = 3,
    Function = 4,
    Add = 5,
    Minus = 6,
    Divide = 7,
    Mod = 8,
    Pow = 9,
    Mult = 10,
    And = 11,
    Or = 12,
    In = 13,
    Out = 14,
    Set = 15,
    Iter = 16,
    As = 17,
    End = 18,
    Type = 19,


class Token:
    def __init__(self):
        self.pos = 1
        self.line = 1
        self.content = ""

    def __repr__(self):
        return f"{self.content} : {self.line} - {self.pos}"

    def __copy__(self):
        token = Token()
        token.pos = self.pos
        token.line = self.line
        token.content = self.content
        return token

    def reset(self):
        self.content = ""


class Lexer:
    def __init__(self):
        self.tokens = []

    def finalize(self) -> list[(Token, TokenType)]:
        pass

    def as_lines(self):
        lines = []
        current_line = []
        current_line_num = 1
        for token in self.tokens:
            if token.line != current_line_num:
                current_line_num += 1
                lines.append(current_line)
                current_line = [token]
            else:
                current_line.append(token)
        return lines

    def lex(self, source):
        current_token = Token()

        def consume(lst=None, token=current_token):
            if lst is None:
                lst = self.tokens
            lst.append(token.__copy__())
            token.reset()

        with open(source) as file:
            quote_found = False
            backslash = False
            for line in file:
                for char in line:

                    if quote_found:
                        match char:

                            case '\\':
                                backslash = True

                            case '\"':
                                if not backslash:
                                    quote_found = False
                                else:
                                    backslash = False

                            case _:
                                pass

                        current_token.content += char
                        continue

                    match char:

                        case '\n':
                            consume()
                            current_token.line += 1
                            current_token.pos = 1

                        case ' ':
                            consume()
                            current_token.pos += 1

                        case '\"':
                            quote_found = True
                            consume()
                            current_token.content += '\"'

                        case _:
                            current_token.content += char
        consume()
