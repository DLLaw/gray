Dorian Lawton  
11/17/2026

# Design Choices

Access before declaration: Reading or assigning a name that has no visible declaration reports an undefined-variable runtime error. Gray evaluates an initializer before creating the new binding, so "let x \= x;" only works if an earlier "x" is already visible.

Missing initializer: "let x;" declares "x" with the value "null". It can be read or assigned immediately.

Redeclaration: Declaring a name again in the same scope replaces its previous value. Declaring the same name inside a block creates a separate local variable that shadows the outer one.

Block scope: Each { ... } block has its own environment. Reads and assignments search the current block first, then move outward. Assignment updates the nearest existing binding. When a block ends, its local declarations are no longer visible. The REPL keeps its global environment between prompts.

# Setup and Commands

Run from the repository root:

python src/gray.py  
python src/gray.py test/lab5/scope.gray  
python src/gray.py test/lab5/error\_test.gray  
To reproduce the other file tests, replace the input path with the corresponding file under "test/lab5/".

# Variable Declaration, Access, and Assignment

This REPL test checks the default value, assignment to an outer variable, and shadowing:

let x; print x; { x \= 2; let x \= 3; print x; } print x;

null

3

2

let x; starts at null. The assignment inside the block updates the outer x to 2 because a local x has not yet been declared. Then let x \= 3; creates the local x. After the block ends, print x; reads the outer value 2\.

The following REPL test confirms that variables persist across separate inputs:

let saved \= 7;

print saved;

7

To check redeclaration in the same scope, enter let score \= 1; let score \= 2; print score;. The output is 2\. (This input is saved under test/lab5/variable\_resuse.gray)

# Textbook Scope Example

Input test/lab5/scope.gray

let a \= "global a";   
let b \= "global b";   
let c \= "global c";   
{   
let a \= "outer a";   
let b \= "outer b";   
{   
let a \= "inner a";   
print a;   
print b;   
print c;   
}   
print a;   
print b;   
print c;   
}   
print a;   
print b;   
print c;

Actual output:

inner a   
outer b   
global c   
outer a   
outer b   
global c   
global a   
global b   
global c

The inner block finds its own a, the enclosing block’s b, and the global c. After the inner block ends, a refers to the enclosing block’s declaration again. After the outer block ends, all three names refer to the global declarations. The value of c is the same throughout because neither block declares a local c.

# Error Handling

The following inputs were tested together in test/lab5/error\_test.gray. The parser recovered after each syntax error and reported the remaining ones in the same run.

| Line | Input | Actual Diagnostic |
| :---- | :---- | :---- |
| 1 | (1 \+ 2\) \= 3; | \[line 1\] Error at \=: Invalid assignment target |
| 2 | let \= 3; | \[line 2\] Error at \=: Expected a variable name after let. |
| 3 | let x \= ;	 | \[line 3\] Error at ‘;’: Expected an expression (literal, unary operator, or ‘(‘). |
| 4 | let x \= 1 | \[line 4\] Error at end: Expected ; after declaration. |

The following cases use separate files. Putting the unmatched braces in the same file can make them balance, and syntax errors prevent the file from reaching the runtime checks.

| Test File | Input | Error Message |
| :---- | :---- | :---- |
| missing\_brace.gray | { print 1; | Error at end: Expected ‘}’ to close block. |
| extra\_brace.gray | } | Error at '}': Unmatched '}'. |
| call\_before\_assignment.gray | print missing; let missing \= 1;	 | at 'missing': Undefined variable 'missing'. |
| undefined\_variable.gray | missing \= 1; | at 'missing': Undefined variable 'missing'. |
| out\_of\_scope.gray | { let local \= 1; } print local; | at 'local': Undefined variable 'local'. |

