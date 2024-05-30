#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiplication(line, index):
    token = {'type': 'MULTIPLICATION'}
    return token, index + 1

def read_division(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1

def read_left_parenthesis(line, index):
    token = {'type': 'LEFT_PARENTHESIS'}
    return token, index + 1

def read_right_parenthesis(line, index):
    token = {'type': 'RIGHT_PARENTHESIS'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiplication(line, index)
        elif line[index] == '/':
            (token, index) = read_division(line, index)
        elif line[index] == '(':
            (token, index) = read_left_parenthesis(line, index)
        elif line[index] == ')':
            (token, index) = read_right_parenthesis(line, index)
        elif line[index].isspace():
            index += 1
            continue
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def evaluate_multiplication_division(tokens):
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTIPLICATION':
                tokens[index - 2]['number'] *= tokens[index]['number']
                tokens.pop(index - 1)
                tokens.pop(index - 1)
                index -= 1
            elif tokens[index - 1]['type'] == 'DIVISION':
                tokens[index - 2]['number'] /= tokens[index]['number']
                tokens.pop(index - 1)
                tokens.pop(index - 1)
                index -= 1
            else:
                index += 1
        else:
            index += 1
    return tokens

def evaluate_addition_subtraction(tokens):
    answer = 0
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def find_corresponding_closing_parenthesis(tokens, index):
    count = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'LEFT_PARENTHESIS':
            count += 1
        if tokens[index]['type'] == 'RIGHT_PARENTHESIS':
            count -= 1
        if count == 0:
            return index
        index += 1
    print('Invalid syntax')
    exit(1)


def evaluate_parenthesis(tokens):
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'LEFT_PARENTHESIS':
                right_index = find_corresponding_closing_parenthesis(tokens, index - 1)
                tokens_inside = []
                tokens_inside.append({'type': 'PLUS'})
                tokens_inside += tokens[index:right_index]
                tokens_inside = evaluate_parenthesis(tokens_inside)
                tokens_inside = evaluate_multiplication_division(tokens_inside)
                answer = evaluate_addition_subtraction(tokens_inside)
                tokens[index - 1]['number'] = answer
                tokens[index - 1]['type'] = 'NUMBER'
                del tokens[index:right_index+1]
                index -= 1
        index += 1
    return tokens
    
def evaluate(tokens):
    tokens.insert(0, {'type': 'PLUS'})  # Insert a dummy '+' token
    tokens = evaluate_parenthesis(tokens)
    tokens = evaluate_multiplication_division(tokens)
    answer = evaluate_addition_subtraction(tokens)
    return answer

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1+(3+5)*4+1")
    test("1.0+2.1-3")
    test("1.0+2.1*3")  
    test("1.0+2.1/3")
    test("(1.0+2.1)*3")
    test("1.0/(2.1-3)")
    test("(1.0+2.1)/3")
    test("1.0+2.1*3-4/2")
    test("(1.0+2.1*3-4)/2")
    test("1.0+2.1*3-4/(2*2)")
    test("1.0+2.1*3-(4/(2*2))")
    test("(1.0+2.1)*3-4/(2*2)")
    test("1.0 + 2.1 * 3 - 4 / 2")   
    test("(1.0 + 2.1) * (3 - 4) / 2")
    test("1")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
