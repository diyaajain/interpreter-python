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
                # Handle unexpected characters
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

def evaluate(tokens):
    stack = []

    for token in tokens:
        if token.token_type == "LEFT_PAREN":
            stack.append(token)
        elif token.token_type == "RIGHT_PAREN":
            # Handle expressions inside parentheses
            expression = []
            while stack and stack[-1].token_type != "LEFT_PAREN":
                expression.append(stack.pop())
            stack.pop()  # Remove the LEFT_PAREN
            expression.reverse()  # Reverse to maintain original order
            result = evaluate_expression(expression)  # Evaluate the inner expression
            stack.append(result)  # Push the result back onto the stack
        elif token.token_type in ["STRING", "TRUE", "FALSE", "NUMBER"]:
            stack.append(token)  # Push literals onto the stack
        elif token.token_type == "MINUS":
            # Handle unary minus
            if stack:
                next_token = stack.pop()
                if next_token.token_type == "NUMBER":
                    negated_value = -float(next_token.literal)
                    # Format the result correctly
                    formatted_value = str(int(negated_value)) if negated_value.is_integer() else str(negated_value)
                    result = Token("NUMBER", formatted_value, formatted_value)
                    stack.append(result)
                else:
                    print(f"[line {token.line_number}] Error: Unary '-' operator must be followed by a number.", file=sys.stderr)
        elif token.token_type == "BANG":
            # Handle the NOT operator
            if stack:
                next_token = stack.pop()
                if next_token.token_type == "TRUE":
                    result = Token("FALSE", "false", "false")
                elif next_token.token_type == "FALSE":
                    result = Token("TRUE", "true", "true")
                elif next_token.token_type == "NUMBER":
                    result = Token("FALSE", "false", "false")  # Non-zero numbers are considered true
                else:
                    print(f"[line {token.line_number}] Error: Invalid operand for '!'.", file=sys.stderr)
                stack.append(result)

    # Final evaluation of the stack
    if stack:
        final_result = stack.pop()
        return final_result.literal  # Return the literal value
    return "nil"

def evaluate_expression(tokens):
    # Implement a basic evaluation for the expression in the context of your language
    for token in tokens:
        if token.token_type == "NUMBER":
            return token  # For simplicity, just return the first number
    return Token("NIL", "nil", None)


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
