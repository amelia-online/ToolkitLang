from toolkit_lexer import Lexer


def main():
    lexer = Lexer()
    lexer.lex("./text.txt")
    lines = lexer.as_lines()

    for line in lines:
        print(line)


if __name__ == '__main__':
    main()
