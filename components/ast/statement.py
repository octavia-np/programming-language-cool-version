from enum import Enum
from abc import ABC, abstractmethod

class Statement(ABC):
    @abstractmethod
    def run(self):
        pass

class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def run(self, context):
        value = self.expression.evaluate(context)
        print(value)

class IfStatement(Statement):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def run(self, context):
        if self.condition.evaluate(context):
            self.true_block.run(context)
        elif self.false_block:
            self.false_block.run(context)

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def run(self, context):
        while self.condition.evaluate(context):
            # print(f"Debug: Before loop iteration, context: {context}")
            self.body.run(context)
            # print(f"Debug: After loop iteration, context: {context}")



class CompoundStatement(Statement):
    def __init__(self, statements):
        self.statements = statements

    def run(self, context):
        for statement in self.statements:
            statement.run(context)

class AssignmentStatement(Statement):
    def __init__(self, variable_name, expression):
        self.variable_name = variable_name
        self.expression = expression

    def run(self, context):
        # Evaluate the expression in the given context (memory)
        value = self.expression.evaluate(context)
        # Set the evaluated value in memory under the variable name
        context.set(self.variable_name, value, type(value))
        # print(f"Updated {self.variable_name} to {value}")  # Debugging output



        

class Operations(Enum):
    PLUS = 0
    MINUS = 1
    TIMES = 2
    DIVIDE = 3
    GREATER = 4
    LESS = 5
    EQUALS = 6
    NOTEQUALS = 7


class Expression(ABC):
    @abstractmethod
    def evaluate(self, context):
        pass

class Expression_string(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return self.value


class Expression_number(Expression):
    def __init__(self, number):
        self.number = number  # This can be a direct value or a callable

    def evaluate(self, context):
        # Ensure it calls the number if it's callable, passing the context
        return self.number(context) if callable(self.number) else self.number



class Expression_boolean(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return self.value

class Expression_math(Expression):
    def __init__(self, operation, parameter1, parameter2):
        self.operation = operation
        self.parameter1 = parameter1
        self.parameter2 = parameter2

    def evaluate(self, context):
        val1 = self.parameter1.evaluate(context)
        val2 = self.parameter2.evaluate(context)
        # Check if either value is boolean and if operation is addition
        if isinstance(val1, bool) or isinstance(val2, bool):
            if self.operation == Operations.PLUS:
                print("Addition operation between boolean and numeric values is not allowed.")
                
        #arithmetic operation for numeric values
        if self.operation == Operations.PLUS:
            return val1 + val2
        elif self.operation == Operations.MINUS:
            return val1 - val2
        elif self.operation == Operations.TIMES:
            return val1 * val2
        elif self.operation == Operations.DIVIDE:
            return val1 / val2
        elif self.operation == Operations.GREATER:
            return val1 > val2
        elif self.operation == Operations.LESS:
            return val1 < val2
        elif self.operation == Operations.EQUALS:
            return val1 == val2
        elif self.operation == Operations.NOTEQUALS:
            return val1 != val2
        else:
            raise ValueError("Unsupported operation")
        
class Expression_string(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return self.value

        
class VariableManipulation(Statement):
    def __init__(self, variable_name, expression):
        self.variable_name = variable_name
        self.expression = expression

    def run(self, context):
        # Evaluate the expression and update the variable in the context
        new_value = self.expression.evaluate(context)
        context.set_variable(self.variable_name, new_value)

class VariableExpression(Expression):
    def __init__(self, name):
        self.name = name

    def evaluate(self, context):
        try:
            return context.get(self.name)
        except KeyError:
            raise Exception(f"Variable '{self.name}' not defined")




class Context:
    def __init__(self):
        self.variables = {}

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        return self.variables.get(name)



def test_expressions():
    context = Context()
    assert Expression_number(42).evaluate(context) == 42, "Test Number Evaluation Failed"
    assert Expression_boolean(True).evaluate(context) is True, "Test Boolean Evaluation Failed"
    
    expr1 = Expression_math(Operations.PLUS, Expression_number(10), Expression_number(5))
    expr2 = Expression_math(Operations.TIMES, Expression_number(2), Expression_number(3))
    assert expr1.evaluate(context) == 15, "Test Addition Failed"
    assert expr2.evaluate(context) == 6, "Test Multiplication Failed"

    print("All expression tests passed.")

### 2. Test Compound Statements

# Test sequences of statements and control structures like if-else and while loops.

def test_compound_statements():
    context = Context()
    context.set_variable('count', 3)

    # Test while loop: simple countdown
    while_condition = Expression_math(Operations.GREATER, 
                                      Expression_number(lambda ctx: ctx.get_variable('count')), 
                                      Expression_number(0))
    decrement_expr = Expression_math(Operations.MINUS, 
                                     Expression_number(lambda ctx: ctx.get_variable('count')), 
                                     Expression_number(1))
    decrement_statement = VariableManipulation('count', decrement_expr)

    while_body = CompoundStatement([
        PrintStatement(Expression_number(lambda ctx: ctx.get_variable('count'))),
        decrement_statement
    ])
    while_stmt = WhileStatement(while_condition, while_body)
    while_stmt.run(context)  # Should print 3, 2, 1

    print("All compound statement tests passed.")





### 3. Test Print Functionality

# Ensure that the `print()` function works as expected within different contexts.

def test_print_functionality():
    context = Context()
    print_stmt = PrintStatement(Expression_number(123))
    print_stmt.run(context)  # Should print 123

    print("Print functionality test passed.")

### 4. Integration Tests

# Combine various elements to simulate real usage scenarios.

def test_integration():
    context = Context()
    
    # Initialize a loop counter in the context
    context.set_variable('loop_counter', 3)

    statements = CompoundStatement([
        PrintStatement(Expression_math(Operations.PLUS, Expression_number(5), Expression_number(3))),
        IfStatement(Expression_boolean(True),
                    PrintStatement(Expression_number(1)),
                    PrintStatement(Expression_number(0))),
        WhileStatement(Expression_math(Operations.GREATER, 
                                       Expression_number(lambda ctx: ctx.get_variable('loop_counter')), 
                                       Expression_number(0)),
                       CompoundStatement([
                           PrintStatement(Expression_string("Looping")),
                           VariableManipulation('loop_counter', 
                                                Expression_math(Operations.MINUS, 
                                                                Expression_number(lambda ctx: ctx.get_variable('loop_counter')), 
                                                                Expression_number(1)))
                       ]))
    ])
    statements.run(context)

    print("Integration tests passed.")




### Running Tests

if __name__ == "__main__":
    test_expressions()
    test_compound_statements()
    test_print_functionality()
    test_integration()

