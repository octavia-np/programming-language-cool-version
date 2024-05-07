from sly import Lexer
import sly

class MyLexer(Lexer):
    """
    MyLexer is a class that inherits from sly.Lexer
    It is used to tokenize the input string.
    ref: https://sly.readthedocs.io/en/latest/sly.html#sly-sly-lex-yacc
    

    Python regEX: https://www.w3schools.com/python/python_regex.asp
    """

    ### `tokens` ###
    # set `tokens` so it can be used in the parser.
    # This must be here and all Capitalized. 
    # Please, ignore IDE warning.
    tokens = {NAME, NUMBER, BOOLEAN, EQUALS, NOTEQUALS, IF, ELSE, WHILE, PRINT, LESS, GREATER, STRING}
    
    # https://sly.readthedocs.io/en/latest/sly.html#literal-characters
    literals = { '+', '-', '*', '/', '=', '(', ')', '{', '}', ';'}
    EQUALS = r'=='
    NOTEQUALS = r'!='
    LESS = r'\<'
    GREATER = r'\>'
    IF = r'if'
    ELSE = r'else'
    WHILE = r'while'
    PRINT = r'print'

    
    ### matching rule ###
    # The matching work from top to bottom
    # At least, all toekns must be defined here

    # Regular expression for string literals
    @_(r'\"[^"]*\"')  # Matches double quoted strings
    def STRING(self, token):
        token.value = token.value[1:-1]  # Strip the quotes
        return token
    
    # Boolean pattern
    @_(r'true|false')
    def BOOLEAN(self, token):
        token.value = True if token.value == 'true' else False
        return token

    # Ignore spaces and tabs 
    ignore = ' \t'

    ### EX1: simply define with regEX ###
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Numeric patterns
    @_(r'\d+\.\d+')  # Matches floats like 12.0, 0.4, .5 (leading zero can be omitted)
    @_(r'-?\d+')       # Matches positive and negative integers
    def NUMBER(self, token):
        if '.' in token.value:
            token.value = float(token.value)
        else:
            token.value = int(token.value)
        return token

    # Extra action for newlines
    @_(r'\n+')
    def ignore_newline(self, t):
        # https://sly.readthedocs.io/en/latest/sly.html#line-numbers-and-position-tracking
        self.lineno += t.value.count('\n')

    def error(self, t):
        self.index += 1
        print(f"ERROR: Illegal character '{t.value[0]}' at line {self.lineno}")

if __name__ == '__main__':
    # Write a simple test that only run when you execute this file
    string_input:str = "x1 + 1as! * ()"
    lex:Lexer = MyLexer()
    # assign type to `token`
    token: sly.lex.Token
    for token in lex.tokenize(string_input):
        print(token)