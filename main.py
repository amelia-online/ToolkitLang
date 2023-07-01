from toolkit_lexer import Lexer

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


def main():
    lexer = Lexer()
    lexer.lex("./text.txt")
    lines = lexer.as_lines()

    for line in lines:
        print(line)


if __name__ == '__main__':
    main()
