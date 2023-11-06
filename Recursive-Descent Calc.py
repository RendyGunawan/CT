import re


class ParseTree:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class Calculator:
    def __init__(self, expression):
        self.expression = re.sub(r'\s+', '', expression)
        self.index = 0

    def parse(self):
        root = self.parse_expression()
        if self.index < len(self.expression):
            self.error("Unexpected character '{}'".format(self.expression[self.index]))
        return root

    def parse_expression(self):
        left = self.parse_term()
        while self.index < len(self.expression) and self.expression[self.index] in ('+', '-'):
            operator = self.expression[self.index]
            self.index += 1
            right = self.parse_term()
            left = ParseTree(operator, left, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.index < len(self.expression) and self.expression[self.index] in ('*', '/', '^', '%'):
            operator = self.expression[self.index]
            self.index += 1
            right = self.parse_factor()
            left = ParseTree(operator, left, right)
        return left

    def parse_factor(self):
        if self.expression[self.index].isdigit():
            start = self.index
            while self.index < len(self.expression) and self.expression[self.index].isdigit():
                self.index += 1
            return ParseTree(int(self.expression[start:self.index]))
        elif self.expression[self.index] == '(':
            self.index += 1
            node = self.parse_expression()
            if self.expression[self.index] != ')':
                self.error("Expected ')' but found '{}'".format(self.expression[self.index]))
            self.index += 1
            return node
        else:
            self.error("Expected a number or '(' but found '{}'".format(self.expression[self.index]))

    def error(self, message):
        raise ValueError("Error: {}".format(message))

    def display_parse_tree(self, node, level=0):
        if node:
            print('    ' * level + str(node.value))
            self.display_parse_tree(node.left, level + 1)
            self.display_parse_tree(node.right, level + 1)

    def calculate(self, node):
        if node.left and node.right:
            left_val = self.calculate(node.left)
            right_val = self.calculate(node.right)
            if node.value == '+':
                return left_val + right_val
            elif node.value == '-':
                return left_val - right_val
            elif node.value == '*':
                return left_val * right_val
            elif node.value == '/':
                if right_val == 0:
                    raise ValueError("Error: Division by zero")
                return left_val / right_val
            elif node.value == '^':
                return left_val ** right_val
            elif node.value == '%':
                if right_val == 0:
                    raise ValueError("Error: Modulo by zero")
                return left_val % right_val
        else:
            return node.value


if __name__ == '__main__':
    calculator = Calculator("34 + 45 * 4 - 2 ^ 3 + 10 % 3")
    try:
        parse_tree = calculator.parse()
        print("Parse Tree:")
        calculator.display_parse_tree(parse_tree)
        result = calculator.calculate(parse_tree)
        print("Result:", result)
    except ValueError as e:
        print(e)
