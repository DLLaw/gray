Dorian Lawton   
10/1/2026

# Lab 1 Report

Language Name: Gray

## Regex used: 

Number: \[0-9\]+(\\.\[0-9\]+)?  
Identifier: \[A-Za-z\_\]\[A-Za-z0-9\_\]\*  
String: \`"(\[^"\\\\r\\n\]

## Design Choices:

Gray is implemented in Python and scans source text without parsing or executing it. Compared to Lox, it uses let instead of var, fn instead of fun, null instead of nil, and \# line comments instead of //. I like these new names and they feel more straightforward to me, but other than that I’d like to stay pretty close to Lox just to make sure it’s easy to understand later. 

## Setup and commands:

Run these from the repository root to run from a file, or run repl mode from root just using src/[gray.py](http://gray.py). Use control+c to exit repl mode. 

python src/gray.py test/lab1/all\_tokens.gray  
python src/gray.py test/lab1/escapes.gray  
python src/gray.py test/lab1/edge\_cases.gray  
python src/gray.py test/lab1/errors.gray  
python src/gray.py test/lab1/empty.gray

(Interactive mode: enter one line at each prompt Ctrl+C exits)  
python src/[gray.py](http://gray.py)

## Test cases:

### all\_tokens.gray 

This tests to make sure every token type is recognized and comments are skipped.   
Source input:  
( ) { } , . \- \+ ; / \*  
\! \!= \= \== \> \>= \< \<=  
and else false fn for if let null or print return true while  
score \_value player2 For letter  
0 21 3.14 \-12  
"" "hello" "hello world" "\# inside a string"

Output:   
LEFT\_PAREN '(' None  
RIGHT\_PAREN ')' None  
LEFT\_BRACE '{' None  
RIGHT\_BRACE '}' None  
COMMA ',' None  
DOT '.' None  
MINUS '-' None  
PLUS '+' None  
SEMICOLON ';' None  
SLASH '/' None  
STAR '\*' None  
BANG '\!' None  
BANG\_EQUAL '\!=' None  
EQUAL '=' None  
EQUAL\_EQUAL '==' None  
GREATER '\>' None  
GREATER\_EQUAL '\>=' None  
LESS '\<' None  
LESS\_EQUAL '\<=' None  
AND 'and' None  
ELSE 'else' None  
FALSE 'false' None  
FN 'fn' None  
FOR 'for' None  
IF 'if' None  
LET 'let' None  
NULL 'null' None  
OR 'or' None  
PRINT 'print' None  
RETURN 'return' None  
TRUE 'true' None  
WHILE 'while' None  
IDENTIFIER 'score' None  
IDENTIFIER '\_value' None  
IDENTIFIER 'player2' None  
IDENTIFIER 'For' None  
IDENTIFIER 'letter' None  
NUMBER '0' 0  
NUMBER '21' 21  
NUMBER '3.14' 3.14  
MINUS '-' None  
NUMBER '12' 12  
STRING '""' ''  
STRING '"hello"' 'hello'  
STRING '"hello world"' 'hello world'  
STRING '"\# inside a string"' '\# inside a string'  
EOF '' None

Expected tokens would be anything listed in src/token\_type.py in the repository.   
Actual lexemes matched the input text. Number literals were 0, 21, 3.14, and 12\. String literals were '', 'hello', 'hello world', and '\# inside a string'. All other literals were None. EOF had an empty lexeme. Actual results matched expectations.

### escapes.gray

This verifies every supported string escape.  
Source input:  
print "First line\\nSecond line";  
print "Name\\tScore";  
print "He said \\"hello\\"";  
print "C:\\\\Users\\\\Student";  
print "Before\\rAfter";

Expected: PRINT, STRING, SEMICOLON for each statement, with escapes decoded in the string literal, then EOF.   
Output:  
PRINT 'print' None  
STRING '"First line\\\\nSecond line"' 'First line\\nSecond line'  
SEMICOLON ';' None  
PRINT 'print' None  
STRING '"Name\\\\tScore"' 'Name\\tScore'  
SEMICOLON ';' None  
PRINT 'print' None  
STRING '"He said \\\\"hello\\\\""' 'He said "hello"'  
SEMICOLON ';' None  
PRINT 'print' None  
STRING '"C:\\\\\\\\Users\\\\\\\\Student"' 'C:\\\\Users\\\\Student'  
SEMICOLON ';' None  
PRINT 'print' None  
STRING '"Before\\\\rAfter"' 'Before\\rAfter'  
SEMICOLON ';' None  
EOF '' None

### edge\_cases.gray

This verifies identifier, number, operator, and string boundaries.   
Source input:  
\# This comment should produce no tokens.  
let letter \= 0;  
For for2 \_value player2  
12\. .5 \-12 123abc  
"" "\# inside a string"  
\!== \===

Output:  
LET 'let' None  
IDENTIFIER 'letter' None  
EQUAL '=' None  
NUMBER '0' 0  
SEMICOLON ';' None  
IDENTIFIER 'For' None  
IDENTIFIER 'for2' None  
IDENTIFIER '\_value' None  
IDENTIFIER 'player2' None  
NUMBER '12' 12  
DOT '.' None  
DOT '.' None  
NUMBER '5' 5  
MINUS '-' None  
NUMBER '12' 12  
NUMBER '123' 123  
IDENTIFIER 'abc' None  
STRING '""' ''  
STRING '"\# inside a string"' '\# inside a string'  
BANG\_EQUAL '\!=' None  
EQUAL '=' None  
EQUAL\_EQUAL '==' None  
EQUAL '=' None  
EOF '' None

Results match expectations: the comment is ignored.Keyword matching is exact. Dots and minus signs split as specified. 123abc splits into two tokens. Empty strings and \# inside strings are valid. Adjacent operators split using their longest supported match.

### errors.gray

This verifies all three demonstrated error categories, line numbers and continued scanning.  
Source input:  
@  
print "after unexpected character";  
"bad\\q"  
print "after invalid escape";  
"unfinished  
print "after unterminated string";  
"unfinished at EOF

Expected: invalid character on line 1, invalid escape on line 3, and unterminated strings on lines 5 and 7\. The three valid statements still produce tokens. Invalid strings produce no tokens.

Output:  
\[line 1\] Error: That character isn't valid: '@'.  
\[line 3\] Error: Not a valid escape sequence: '\\q'.  
\[line 5\] Error: You never closed the string.  
\[line 7\] Error: You never closed the string.  
PRINT 'print' None  
STRING '"after unexpected character"' 'after unexpected character'  
SEMICOLON ';' None  
PRINT 'print' None  
STRING '"after invalid escape"' 'after invalid escape'  
SEMICOLON ';' None  
PRINT 'print' None  
STRING '"after unterminated string"' 'after unterminated string'  
SEMICOLON ';' None  
EOF '' None

Matches expectations

### empty.gray

This verifies scanning with an empty input. The source is completely empty.   
Output:  
EOF '' None  
Matches expectations.

### Repl mode error recovery

Verifies terminal input and recovery after an error.   
Source input (In repl mode) and output:  
\> @  
\[line 1\] Error: That character isn't valid: '@'.  
EOF '' None  
\> print "hello";  
PRINT 'print' None  
STRING '"hello"' 'hello'  
SEMICOLON ';' None  
EOF '' None  
\> "unfinished  
\[line 1\] Error: You never closed the string.  
EOF '' None  
\> let score \= 21;  
LET 'let' None  
IDENTIFIER 'score' None  
EQUAL '=' None  
NUMBER '21' 21  
SEMICOLON ';' None  
EOF '' None

Matches expectations. 

## Limitations and known issues:

I did not notice any issues or failures in the tests listed above. Gray doesn’t parse or execute code, support block comments or specific numbers or allow strings over multiple lines (\\n escapes are supported though). Number range checks are not implemented, so very large numbers could go over Python's limit. The prompt scans one line at a time.