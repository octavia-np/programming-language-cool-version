from components.lexica import MyLexer
from components.memory import Memory
# from lexica import MyLexer
# from memory import Memory
from sly import Parser


from components.ast.statement import *
# from ast.statement import *
class ASTParser(Parser):
    debugfile = 'parser.out'
    start = 'program'
    # Get the token list from the lexer (required)
    tokens = MyLexer.tokens
    precedence = (
        ('left', 'EQUALS', 'NOTEQUALS'),
        ('left', "+", "-"),
        ('left', "*", "/")
        )
    
    def __init__(self, memory):
        self.memory = memory  # Ensure singleton pattern usage from Memory class

    @_('statements')
    def program(self, p):
        if p.statements:
            return p.statements
        return []  # Return an empty list if no statements were parsed


    @_('statement ";" statements')
    def statements(self, p):
        return [p.statement] + p.statements

    @_('statement ";"')
    def statements(self, p):
        return [p.statement]
    

    @_('PRINT "(" expr ")"')
    def statement(self, p):
        return PrintStatement(p.expr)
    
    
    @_('NAME "=" expr')
    def statement(self, p):
        # self.memory.set(p.NAME, p.expr.evaluate(self.memory))
        return AssignmentStatement(p.NAME, p.expr)

    @_('IF "(" expr ")" "{" statements "}" ELSE "{" statements "}"')
    def statement(self, p):
        return IfStatement(p.expr, CompoundStatement(p.statements0), CompoundStatement(p.statements1))

    @_('IF "(" expr ")" "{" statements "}"')
    def statement(self, p):
        return IfStatement(p.expr, CompoundStatement(p.statements))

    @_('WHILE "(" expr ")" "{" statements "}"')
    def statement(self, p):
        return WhileStatement(p.expr, CompoundStatement(p.statements))

    # Extend the grammar to handle string literals in expressions
    @_('STRING')
    def expr(self, p):
        return Expression_string(p.STRING)
        
    # Arithmetic Expressions
    @_('expr "+" expr')
    def expr(self, p):
        if isinstance(p.expr0, bool) or isinstance(p.expr1, bool):
            print("Error: Addition operation between boolean and numeric values is not allowed.")
            return None
        return Expression_math(Operations.PLUS, p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return Expression_math(Operations.MINUS, p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return Expression_math(Operations.TIMES, p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return Expression_math(Operations.DIVIDE, p.expr0, p.expr1)

    # Logical Expressions (assuming your Expression_math can handle logical operators)
    @_('expr LESS expr')
    def expr(self, p):
        return Expression_math(Operations.LESS, p.expr0, p.expr1)

    @_('expr GREATER expr')
    def expr(self, p):
        return Expression_math(Operations.GREATER, p.expr0, p.expr1)

    @_('expr EQUALS expr')
    def expr(self, p):
        return Expression_math(Operations.EQUALS, p.expr0, p.expr1)

    @_('expr NOTEQUALS expr')
    def expr(self, p):
        return Expression_math(Operations.NOTEQUALS, p.expr0, p.expr1)

    @_('NUMBER')
    def expr(self, p) -> Expression:
        return Expression_number(number=p.NUMBER)

    @_('expr')
    def expr(self, p):
        if isinstance(p.expr0, Expression_number):
            return p.expr0
        elif isinstance(p.expr0, str):  # Handling variable names
            value = self.memory.get(p.expr0)
            if value is None:
                raise Exception(f"Variable '{p.expr0}' not defined")
            return Expression_number(value)

    
    @_('NAME')
    def expr(self, p):
        var_name = p.NAME
        return VariableExpression(var_name)


    @_('BOOLEAN')
    def expr(self, p):
        return Expression_boolean(value=p.BOOLEAN)


        

        
if __name__ == "__main__":
    lexer = MyLexer()
    parser = ASTParser()
    text = """
    if (x > 5) {
        print(x)
    } else {
        while (x < 10) {
            print(x)
            x = x + 1
        }
    };
    """
    result = parser.parse(lexer.tokenize(text))
    print(result)
    # Implement a way to run or visualize the result to validate correctness
