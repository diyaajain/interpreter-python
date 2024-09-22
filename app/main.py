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
    error_occurred = False

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

        # Handle string literals
        elif c == '"':
            string_start = i
            i += 1
            string_content = ""

            while i < length and file_contents[i] != '"':
                if file_contents[i] == '\n':  # Unterminated string at newline
                    error_occurred = True
                    print(f"[line {line_number}] Error: Unterminated string.", file=sys.stderr)
                    break  # Exit the loop but continue processing
                elif file_contents[i] == '\\' and i + 1 < length and file_contents[i + 1] == '"':
                    string_content += '"'
                    i += 2  # Skip the escape character and the quote
                    continue
                string_content += file_contents[i]
                i += 1

            if not error_occurred and i < length and file_contents[i] == '"':
                i += 1  # Move past the closing "
                lexeme = file_contents[string_start:i]
                tokens.append(Token("STRING", lexeme, string_content))
            else:
                # If an unterminated string was detected, we don’t add a token
                continue

        # Handle number literals
        elif c.isdigit() or (c == '.' and (i + 1 < length and file_contents[i + 1].isdigit())):
            number_start = i
            while i < length and (file_contents[i].isdigit() or file_contents[i] == '.'):
                i += 1
                
            number_str = file_contents[number_start:i]
            try:
                # Convert to float for proper formatting
                literal_value = float(number_str)
                if literal_value.is_integer():
                    literal_value_str = f"{int(literal_value)}.0"
                else:
                    literal_value_str = str(literal_value)
                
                tokens.append(Token("NUMBER", number_str, literal_value_str))
            except ValueError:
                print(f"[line {line_number}] Error: Invalid number literal: {number_str}", file=sys.stderr)

        # Handle operators and other tokens
        elif c == "+":
            tokens.append(Token("PLUS", c, None))
            i += 1
        elif c == "-":
            tokens.append(Token("MINUS", c, None))
            i += 1
        elif c == "*":
            tokens.append(Token("STAR", c, None))
            i += 1
        elif c == "/":
            if i + 1 < length and file_contents[i + 1] == "/":
                # Comment: skip until the end of the line
                while i < length and file_contents[i] != "\n":
                    i += 1
            else:
                tokens.append(Token("SLASH", c, None))
                i += 1
        elif c == "=" and i + 1 < length and file_contents[i + 1] == "=":
            tokens.append(Token("EQUAL_EQUAL", "==", None))
            i += 2
        elif c == "=":
            tokens.append(Token("EQUAL", "=", None))
            i += 1
        elif c == "!" and i + 1 < length and file_contents[i + 1] == "=":
            tokens.append(Token("BANG_EQUAL", "!=", None))
            i += 2
        elif c == "!":
            tokens.append(Token("BANG", "!", None))
            i += 1
        elif c == "<":
            if i + 1 < length and file_contents[i + 1] == "=":
                tokens.append(Token("LESS_EQUAL", "<=", None))
                i += 2
            else:
                tokens.append(Token("LESS", "<", None))
                i += 1
        elif c == ">":
            if i + 1 < length and file_contents[i + 1] == "=":
                tokens.append(Token("GREATER_EQUAL", ">=", None))
                i += 2
            else:
                tokens.append(Token("GREATER", ">", None))
                i += 1
        elif c == "(":
            tokens.append(Token("LEFT_PAREN", "(", None))
            i += 1
        elif c == ")":
            tokens.append(Token("RIGHT_PAREN", ")", None))
            i += 1
        elif c == "{":
            tokens.append(Token("LEFT_BRACE", "{", None))
            i += 1
        elif c == "}":
            tokens.append(Token("RIGHT_BRACE", "}", None))
            i += 1
        elif c == ",":
            tokens.append(Token("COMMA", ",", None))
            i += 1
        elif c == ";":
            tokens.append(Token("SEMICOLON", ";", None))
            i += 1
        else:
            print(f"[line {line_number}] Error: Unexpected character: {c}", file=sys.stderr)
            i += 1

    tokens.append(Token("EOF", "", None))

    return tokens, error_occurred

def evaluate(tokens):
    for token in tokens:
        if token.token_type in ["TRUE", "FALSE", "NIL"]:
            return token.lexeme.lower()  # Return "true", "false", or "nil" as expected
    return "nil"  # Default return if no matching token found

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

    tokens, error_occurred = tokenize(file_contents)

    if command == "tokenize":
        for token in tokens:
            literal_value = token.literal if token.literal is not None else "null"
            print(f"{token.token_type} {token.lexeme} {literal_value}")
    
    if command == "evaluate":
        result = evaluate(tokens)
        print(result)

    if error_occurred:
        exit(65)  # Exit with code 65 if any errors occurred

if __name__ == "__main__":
    main()
