Dorian Lawton  
11/1/2026

## Implementation

Gray now supports expression statements and print statements. Both end with a semicolon. Expression statements evaluate a value without displaying it. Print statements evaluate and display the value. Gray uses null instead of Lox's nil.

program \-\> statement\* EOF ;  
statement \-\> print\_statement \| expression\_statement ;  
print\_statement \-\> "print" expression ";" ;  
expression\_statement \-\> expression ";" ;

stmt.py defines ExpressionStmt and PrintStmt. The parser returns a list of statements, and the evaluator executes them in order. Only print statements produce normal output.

When a syntax error occurs, the parser reports its location and uses panic-mode recovery. It skips tokens through the next semicolon or stops before a new print statement, then continues parsing. If any syntax errors were found, the program does not execute that input. The interactive prompt remains usable for the next input.

## Setup and commands

From the repository root, run:

python src/gray.py test/lab4/errors.gray  
python src/gray.py test/lab4/statements.gray

For interactive mode, run python src/gray.py and enter statements ending in semicolons. Ctrl+C or EOF exits.

## Test 1: Syntax errors and recovery

Purpose: detect a missing semicolon and a missing operand, and verify that parsing continues after the first error.

Input (test/lab4/errors.gray):

"one"  
true;  
print 2 \+

Expected: an error at true on line 2 because the preceding string expression has no semicolon, followed by an error at EOF on line 3 because \+ has no right operand. No statements should execute.

Actual output:  
\[line 2\] Error at 'true': Expected ';' after expression.  
\[line 3\] Error at end: Expected an expression (literal, unary operator, or '(').

Result: PASS. Both errors were reported. After the first error, recovery skipped through true;, allowing the parser to reach the incomplete print statement and report the second error.

## Test 2: Expression and print statements

Purpose: execute multiple statements and print strings, booleans, arithmetic results, and null.

Input (test/lab4/statements.gray):  
4 \+ 2;  
print "one";  
print true;  
print 1 \+ 2;  
print null;

Expected output:  
one  
true  
3  
null

Actual output:  
one  
true  
3  
null

Result: PASS. The expression statement 4 \+ 2; produced no output, and all print statements displayed the expected values.

## Limitations 

This version supports expression and print statements only. Variable declarations, blocks, and control-flow statements are not implemented. Interactive input is processed one line at a time. No failures in the two required tests.

