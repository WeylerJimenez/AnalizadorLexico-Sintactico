import sys

import ply.lex as lex
#from tabulate import tabulate
# Alejandro Ortega, Nicole Rios, Jhon Edison Parra

# https://www.dabeaz.com/ply/ply.html#ply_nn6
reserved = {

    'array': 'ARRAY',
    'break': 'BREAK',
    'case': 'CASE',
    'class': 'CLASS',
    'data': 'DATA',
    'deriving': 'DERIVING',
    'do': 'DO',
    'else': 'ELSE',
    'elseif': 'ELSEIF',
    'exit': 'EXIT',
    'extends': 'EXTENDS',
    'fn': 'FN',
    'for': 'FOR',
    'function': 'FUNCTION',
    'if': 'IF',
    'import': 'IMPORT',
    'in': 'IN',
    'infix': 'INFIX',
    'infixl': 'INFIXL',
    'infixr': 'INFIXR',
    'instance': 'INSTANCE',
    'let': 'LET',
    'module': 'MODULE',
    'newtype': 'NEWTYPE',
    'then': 'THEN',
    'type': 'TYPE',
    'where': 'WHERE',
    'of': 'OF',
    'print': 'PRINT',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'public': 'PUBLIC',
    'require': 'REQUIRE',
    'return': 'RETURN',
    'static': 'STATIC',
    'switch': 'SWITCH',
    'this': 'THIS',
    'var': 'VAR',
    'while': 'WHILE',
    'filter': 'FILTER',
}

tokens = list(reserved.values()) + [
    # Symbols

    'ASSIGN',
    'MOD',
    'SUMA',
    'CONECTARLISTA1',
    'CONECTARLISTA2',
    'IGUALDAD',
    'IGUALDADES',
    'MENOS',
    # 'MINUSMINUS',
    # 'MINUSEQUAL',
    'MULTIPLICAR',
    'DIVISION',
    'MENOSQUE',
    'MENOSOIGUAL',
    'MAYORQUE',
    'MAYOROIGUAL',
    'IGUAL',
    # 'DEQUAL',
    # 'DISTINT',
    # 'ISEQUAL',
    'PUNTOYCOMA',
    'DOBLEPUNTO',
    'PARENTESISIZ',
    'PARENTESISDE',
    'CORCHETEIZ',
    'CORCHETEDE',
    'LBLOCK',
    'RBLOCK',
    'COMA',
    'HASHTAG',
    'PUNTO',
    'QUESTIONMARK',
    'COMILLASIMPLE',
    'COMILLASDOBLES',
    'CONS',

    # variables

    # Others
    'VARIABLE',
    # 'VARIABLE2',
    'NUMBER',
    'CADENAVACIA',
    'CADENA1',
    # 'CADENA2',
    'ID',
    'COMENTARIOENLINEAS',
    'COMENTARIOSENLINEA',
]

# Regular expressions rules for simple tokens
# t_CONECTARLISTA = r'\++'
t_MOD = r'%'
t_SUMA = r'\+'
t_MENOS = r'-'
t_MULTIPLICAR = r'\*'
t_DIVISION = r'/'
t_IGUAL = r'='
t_IGUALDAD = r'=='
# t_DISTINT = r'!'
t_MENOSQUE = r'<'
t_MAYORQUE = r'>'
t_PUNTOYCOMA = ';'
t_COMA = r','
t_PARENTESISIZ = r'\('
t_PARENTESISDE = r'\)'
t_CORCHETEIZ = r'\['
t_CORCHETEDE = r'\]'
t_LBLOCK = r'{'
t_RBLOCK = r'}'
t_DOBLEPUNTO = r':'
t_HASHTAG = r'\#'
t_PUNTO = r'\.'
t_COMILLASIMPLE = r'\''
t_COMILLASDOBLES = r'\"'
t_QUESTIONMARK = r'\?'


def t_IGUALDADES(t):
    r'([a-zA-Z]([\w])*) ([<|<=|=|>|>=])\s*[a-zA-Z]([\w])*'
    return t


def t_CONECTARLISTA1(t):
    r'((\[\d*\w*\])?|(\w+)?)+ \s* (\++) ((\[\d*\w*\]?)|(\w+)?)+ \s* (\++) ((\[\d*\w*\])?|(\w+)?)+'
    return t


def t_CONECTARLISTA2(t):
    r'([a-zA-Z]+\s*(\++)[a-zA-Z]+)'
    return t


def t_CONS(t):
    r'([\d*])?([a-zA-Z]([\w])*)?\:([\d*])?([a-zA-Z]([\w])*)?'
    return t


def t_CADENAVACIA(t):
    r'\[]'
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = float(t.value)
    return t


def t_VARIABLE(t):
    r'[a-zA-Z]([\w])*'
    if t.value in reserved:
        t.type = reserved[t.value]  # Check for reserved words
        return t
    else:
        return t


""" def t_VARIABLE2(t):
    r'[a-zA-Z](\w)*'
    if t.value in reserved:
        t.type = reserved[t.value]  # Check for reserved words
        return t
    else:
        return t """


# Check reserved words
# This approach greatly reduces the number of regular expression rules and is likely to make things a little faster.
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]  # Check for reserved words
        return t
    else:
        t_error(t)


def t_CADENA1(t):
    r'(\"[a-z A-Z]*)\s*([a-z A-Z]*\")'
    return t


# def t_CADENA2(t):
   # r'(\"[a-z A-Z]*)\s*([a-z A-Z]*\")'
    # return t


def t_MENOSOIGUAL(t):
    r'<='
    return t


def t_MAYOROIGUAL(t):
    r'>='
    return t


def t_ASSIGN(t):
    r'=>'
    return t


def t_DEQUAL(t):
    r'!='
    return t

    # def t_ISEQUAL(t):
    r'=='
    return t


#def t_MINUSMINUS(t):
    r'--'
    return t

    # def t_PLUSPLUS(t):
    r'\+\+'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_space(t):
    r'\s+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_COMENTARIOENLINEAS(t):
    r'((\{)(\-)\w*\s*\n\w*\-\})'
    #r'([\{,\-]\s*[a-zA-Z]\s*[\w]*[\-,\}])'
    t.lexer.lineno += t.value.count('\n')


def t_COMENTARIOSENLINEA(t):
    r'((\-\-)([a-zA-Z,\d*,\s*]*)*\n)'
    #r'\#(.)*?\n
    #r'(\-+)([a-zA-Z]*)(\s*)\n'
    #r'\s*(\-\-[a-zA-Z,\s*])([\w,\s*])*\n'
    t.lexer.lineno += 1


def t_error(t):
    print("Lexical error: " + str(t.value))
    t.lexer.skip(1)


def test(data, lexer):
    lexer.input(data)
    i = 1  # Representa la línea
    while True:
        tok = lexer.token()
        if not tok:
            break

        print("\t" + str(i) + " - " + "Line: " + str(tok.lineno) + "\t" + str(tok.type) + "\t-->  " + str(tok.value))
        #print(tabulate(rios3, headers='firstrow', tablefmt='fancy_grid'))
        #print("\t" + str(i) + " - " + "Line: " + str(tok.lineno) + "\t" + str(tok.type) + "\t-->  " + str(tok.value))
        i += 1
        # print(tok)


lexer = lex.lex()

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        fin = 'qsort.hs'
    else:
        fin = sys.argv[1]
    f = open(fin, 'r')
    data = f.read()
    # print (data)
    # lexer.input(data)
    test(data, lexer)
# input()