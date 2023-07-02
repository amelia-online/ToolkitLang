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

OPERATORS = {"+", "-", "*", "/", "%", "&", "|"}
PARENTHESES = {"(", ")", "[", "]", "{", "}"}


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
    Space = 20,
    RParen = 21,
    LParen = 22,
    RBracket = 23,
    LBracket = 24,
    RCurly = 25,
    LCurly = 26,


def unreachable():
    assert False, "This code is unreachable"


class Token:
    def __init__(self):
        self.pos = 1
        self.line = 1
        self.content: str = ""

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


def process_str(string) -> str:
    index = 1
    result = ""
    while index < len(string) - 1:
        char = string[index]
        match char:

            case "\\":
                index += 1
                match string[index]:

                    case "\"":
                        result += "\""

                    case "\\":
                        result += "\\"

                    case "\'":
                        result += '\''

                    case "t":
                        result += '\t'

                    case "n":
                        result += '\n'

                    case _:
                        print(f"ERROR: Unknown string escape encountered: '{string[index]}'")

            case _:
                result += char
        index += 1
    return result


def is_num(string):
    try:
        _ = float(string)
        return True
    except ValueError:
        return False


def match_operator(string):
    match string:
        case '+':
            return TokenType.Add

        case '-':
            return TokenType.Minus

        case '*':
            return TokenType.Mult

        case "/":
            return TokenType.Divide

        case "%":
            return TokenType.Mod

        case "|":
            return TokenType.Or

        case "&":
            return TokenType.And

        case "**":
            return TokenType.Pow

        case _:
            unreachable()


def match_parentheses(string):
    match string:

        case '(':
            return TokenType.LParen

        case ')':
            return TokenType.RParen

        case '[':
            return TokenType.LBracket

        case ']':
            return TokenType.RBracket

        case '{':
            return TokenType.LCurly

        case '}':
            return TokenType.RCurly

        case _:
            unreachable()


class Lexer:
    def __init__(self):
        self.tokens = []

    def finalize(self):
        categorized_tokens = []

        def categorize(old_token, ttype, lst=None):
            if lst is None:
                lst = categorized_tokens
            lst.append((old_token, ttype))

        for token in self.tokens:
            if token.content == " " or token.content == "":
                continue

            if token.content.startswith("\"") and token.content.endswith("\""):
                categorize(token, TokenType.String)
            elif token.content in OPERATORS:
                categorize(token, match_operator(token.content))
            elif is_num(token.content):
                categorize(token, TokenType.Number)
            elif token.content.startswith("~"):
                categorize(token, TokenType.Function)
            elif token.content == "end":
                categorize(token, TokenType.End)
            elif token.content == "<:":
                categorize(token, TokenType.Out)
            elif token.content == ":>":
                categorize(token, TokenType.In)
            elif token.content == "set":
                categorize(token, TokenType.Set)
            elif token.content == "as":
                categorize(token, TokenType.As)
            elif token.content == "iter":
                categorize(token, TokenType.Iter)
            elif token.content in PARENTHESES:
                categorize(token, match_parentheses(token.content))
            else:
                categorize(token, TokenType.Ident)
        self.tokens = categorized_tokens

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
        target = self.tokens

        def consume(lst=None, token=current_token):
            if lst is None:
                lst = target
            lst.append(token.__copy__())
            token.reset()

        def consume_item(item, token=current_token):
            if not token.content == "":
                consume()
                token.pos += 1
            token.content = item
            consume()

        with open(source) as file:
            quote_found = False
            backslash = False
            in_comment = False
            end_comment = False
            throwaway_buffer = []
            for line in file:
                for char in line:

                    if in_comment:
                        target = throwaway_buffer

                    if end_comment:
                        in_comment = False
                        end_comment = False
                        target = self.tokens

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

                        case '[':
                            consume_item('[')
                            current_token.pos += 1

                        case ']':
                            consume_item(']')
                            current_token.pos += 1

                        case '(':
                            consume_item('(')
                            current_token.pos += 1

                        case ')':
                            consume_item(')')
                            current_token.pos += 1

                        case '{':
                            consume_item('{')
                            current_token.pos += 1

                        case '}':
                            consume_item("}")
                            current_token.pos += 1

                        case '\"':
                            quote_found = True
                            consume()
                            current_token.content += '\"'

                        case _:
                            current_token.content += char
                    if target[-1].content == "<*":
                        in_comment = True
                        target.pop()
                    elif target[-1].content == "*>":
                        end_comment = True
        consume()
