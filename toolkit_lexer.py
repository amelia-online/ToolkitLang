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
