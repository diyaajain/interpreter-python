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
                    break
                string_content += file_contents[i]
                i += 1

            if not error_occurred:
                if i < length and file_contents[i] == '"':
                    i += 1  # Move past the closing "
                    lexeme = file_contents[string_start:i]
                    tokens.append(Token("STRING", lexeme, string_content))
                else:
                    error_occurred = True
                    print(f"[line {line_number}] Error: Unterminated string.", file=sys.stderr)
        
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
            else:
                error_occurred = True
                print(f"[line {line_number}] Error: Unexpected boolean value: {boolean_str}", file=sys.stderr)

        # Handle number literals
        elif c.isdigit() or (c == '.' and (i + 1 < length and file_contents[i + 1].isdigit())):
            number_start = i
            while i < length and (file_contents[i].isdigit() or file_contents[i] == '.'):
                i += 1
                
            number_str = file_contents[number_start:i]
            try:
                literal_value = float(number_str)
                tokens.append(Token("NUMBER", number_str, str(literal_value)))
            except ValueError:
                error_occurred = True
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
        elif c == ".":
            tokens.append(Token("DOT", ".", None))
            i += 1
        else:
            error_occurred = True
            print(f"[line {line_number}] Error: Unexpected character: {c}", file=sys.stderr)
            i += 1  # Move past the unexpected character

    tokens.append(Token("EOF", "", None))

    return tokens, error_occurred

class Unary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

def evaluate(tokens):
    stack = []

    for token in tokens:
        if token.token_type == "NUMBER":
            value = float(token.literal)
            stack.append(value)

        elif token.token_type == "TRUE":
            stack.append(True)

        elif token.token_type == "FALSE":
            stack.append(False)

        elif token.token_type == "NIL":
            stack.append(None)

        elif token.token_type == "MINUS":
            # Ensure there's something to negate
            if not stack:
                print("Error: No value to negate.", file=sys.stderr)
                return "nil"
            right = stack.pop()  # Pop the last value to negate
            stack.append(-right)  # Push negated value directly

        elif token.token_type == "BANG":
            if not stack:
                print("Error: No value for logical NOT.", file=sys.stderr)
                return "nil"
            right = stack.pop()  # Pop the last value to apply logical NOT
            stack.append("true" if right == "false" or right is None else "false")

        elif token.token_type == "LEFT_PAREN":
            stack.append(token)

        elif token.token_type == "RIGHT_PAREN":
            while stack and isinstance(stack[-1], Token) and stack[-1].token_type != "LEFT_PAREN":
                top_token = stack.pop()
                stack.append(top_token)  # Handle other values

            if stack and isinstance(stack[-1], Token) and stack[-1].token_type == "LEFT_PAREN":
                stack.pop()

    # Final evaluation of the stack
    if stack:
        final_value = stack[-1]
        return interpret_value(final_value)

    return "nil"  # Default return if no tokens processed


def evaluate_unary(expr):
    if expr.operator == "-":
        return -interpret_value(expr.right)
    elif expr.operator == "!":
        value = interpret_value(expr.right)
        return "true" if value == "false" or value is None else "false"

def interpret_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    elif value is None:
        return "nil"
    elif isinstance(value, float):
        return str(int(value) if value.is_integer() else value)
    return value

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
        with open(filename, 'r') as file:
            file_contents = file.read()

        tokens, error_occurred = tokenize(file_contents)

        if error_occurred:
            exit(1)

        if command == "tokenize":
            for token in tokens:
                print(token.token_type, token.lexeme)
        elif command == "evaluate":
            result = evaluate(tokens)
            print(result)

    except FileNotFoundError:
        print(f"File not found: {filename}", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()
