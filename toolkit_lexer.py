
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

    def lex(self, source):
        current_token = Token()

        def consume(lst=None, token=current_token):
            if lst is None:
                lst = self.tokens
            lst.append(token.__copy__())
            token.reset()

        with open(source) as file:
            for line in file:
                for char in line:
                    match char:

                        case '\n':
                            consume()
                            current_token.line += 1
                            current_token.pos = 1

                        case ' ':
                            consume()
                            current_token.pos += 1

                        case _:
                            current_token.content += char
        consume()
