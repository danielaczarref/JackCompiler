# Lexical Analyzer 

## Computer Engineering
## Subject: Compilers 
## Developed by Daniela Carvalho and André Luiz

Development of a lexical analyzer in the Python 3 programming language in order to identify, through a code made available by the professor in the Jack language, the language tokens, among them:
    
    - language keywords, that is, reserved words:

'class' | 'constructor' | 'function' |
'method' | 'field' | 'static' | 'var' | 'int' |
'char' | 'boolean' | 'void' | 'true' | 'false' |
'null' | 'this' | 'let' | 'do' | 'if' | 'else' |
'while' | 'return’

     - language symbols:

'{' | '}' | '(' | ')' | '[' | ']' | '. ' | ', ' | '; ' | '+' | '-' | '*' |
'/' | '&' | '|' | '<' | '>' | '=' | '~'

     - identifiers (variables);
     - integers;
     - Strings;

The output of the code is written in the "result.txt" file.

We have chosen the Python programming language because it's easier to deal with inputs and outputs from and in another files than JS. It just felt more practical.

The output is similar to an XML file, something like:
```
<tokens>
<keyword> if </keyword>
<symbol> ( </symbol>
<identifier> x </identifier>
<symbol> &lt; </symbol>
<intConst> 0 </intConst>
<symbol> ) </symbol>
<symbol> { </symbol>
<keyword> let </keyword>
<identifier> sign </identifier>
<symbol> = </symbol>
<stringConst> negative </stringConst>
<symbol> ; </symbol>
<symbol> } </symbol>
</tokens>
```

It's important to remember that the symbols <, >, ", and & will be printed as &lt;  &gt;  &quot; and &amp; in order to avoid conflits with XML own symbols. 
