from toolkit_lexer import Lexer


def main():
    lexer = Lexer()
    lexer.lex("./text.txt")

    for token in lexer.tokens:
        print(token)


if __name__ == '__main__':
    main()
