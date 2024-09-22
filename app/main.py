import sys

# Define reserved words and their corresponding token types
RESERVED_WORDS = {
    "and": "AND",
    "class": "CLASS",
    "else": "ELSE",
    "false": "FALSE",
    "for": "FOR",
    "fun": "FUN",
    "if": "IF",
    "nil": "NIL",
    "or": "OR",
    "print": "PRINT",
    "return": "RETURN",
    "super": "SUPER",
    "this": "THIS",
    "true": "TRUE",
    "var": "VAR",
    "while": "WHILE",
}

class Token:
    def __init__(self, token_type, lexeme, literal):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal

def tokenize(file_contents):
    tokens = []
    i = 0
    length = len(file_contents)
    line_number = 1

    while i < length:
        c = file_contents[i]

        # Ignore whitespace characters
        if c in (' ', '\t'):
            i += 1
            continue
        elif c == '\n':
            line_number += 1
            i += 1
            continue

        # Handle identifiers and reserved words
        elif c.isalpha() or c == '_':
            identifier_start = i
            while i < length and (file_contents[i].isalnum() or file_contents[i] == '_'):
                i += 1
            
            identifier_str = file_contents[identifier_start:i]
            if identifier_str in RESERVED_WORDS:
                tokens.append(Token(RESERVED_WORDS[identifier_str], identifier_str, None))
            else:
                tokens.append(Token("IDENTIFIER", identifier_str, None))

        # Handle boolean literals
        elif c in ('t', 'f'):
            boolean_start = i
            while i < length and file_contents[i].isalpha():
                i += 1

            boolean_str = file_contents[boolean_start:i]
            if boolean_str == "true":
                tokens.append(Token("TRUE", boolean_str, None))
            elif boolean_str == "false":
                tokens.append(Token("FALSE", boolean_str, None))

        # Handle number literals
        elif c.isdigit() or (c == '.' and (i + 1 < length and file_contents[i + 1].isdigit())):
            number_start = i
            while i < length and (file_contents[i].isdigit() or file_contents[i] == '.'):
                i += 1
                
            number_str = file_contents[number_start:i]
            tokens.append(Token("NUMBER", number_str, str(float(number_str))))

        # Handle operators and other tokens
        elif c == "-":
            tokens.append(Token("MINUS", c, None))
            i += 1
        elif c == "!":
            tokens.append(Token("BANG", c, None))
            i += 1
        elif c == "(":
            tokens.append(Token("LEFT_PAREN", "(", None))
            i += 1
        elif c == ")":
            tokens.append(Token("RIGHT_PAREN", ")", None))
            i += 1
        else:
            print(f"[line {line_number}] Error: Unexpected character: {c}", file=sys.stderr)
            i += 1  # Move past the unexpected character

    tokens.append(Token("EOF", "", None))
    return tokens

def evaluate(tokens):
    stack = []

    for token in tokens:
        if token.token_type == "NUMBER":
            stack.append(float(token.literal))
        elif token.token_type == "TRUE":
            stack.append(True)
        elif token.token_type == "FALSE":
            stack.append(False)
        elif token.token_type == "MINUS":
            if not stack:
                print("Error: No value to negate.", file=sys.stderr)
                return "nil"
            right = stack.pop()  # Pop the last value to negate
            stack.append(-right)  # Negate and push back
        elif token.token_type == "BANG":
            if not stack:
                print("Error: No value for logical NOT.", file=sys.stderr)
                return "nil"
            right = stack.pop()
            stack.append(not right)  # Logical NOT

    if stack:
        final_value = stack[-1]
        if isinstance(final_value, bool):
            return "true" if final_value else "false"
        elif isinstance(final_value, float):
            return str(int(final_value) if final_value.is_integer() else final_value)

    return "nil"

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh [tokenize|evaluate] <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ["tokenize", "evaluate"]:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    try:
        with open(filename) as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        exit(1)

    tokens = tokenize(file_contents)

    if command == "tokenize":
        for token in tokens:
            literal_value = token.literal if token.literal is not None else "null"
            print(f"{token.token_type} {token.lexeme} {literal_value}")

    if command == "evaluate":
        result = evaluate(tokens)
        print(result)

if __name__ == "__main__":
    main()
