from automata.fa.Moore import Moore
import sys, os
import string
from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom import minidom
from myerror import MyError

error_handler = MyError('LexerErrors')

global check_cm
global check_key

#
# ALPHABET
#

alphabet = list(string.ascii_lowercase + string.ascii_uppercase)

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

misc = ['\n', ' ', '(', ')', '[', ']', '{', '}', ';', ',', '+', '-', '/', '*', '=', '!']

fullList = alphabet + numbers + misc

#
# STATES
#

statesInit = ['q0']

statesINT = [
            'q_INT_1',
            'q_INT_2',
            'q_INT_3'
            ]

statesFLOAT = [
            'q_FLOAT_1',
            'q_FLOAT_2',
            'q_FLOAT_3',
            'q_FLOAT_4',
            'q_FLOAT_5'
            ]

statesVOID = [
            'q_VOID_1',
            'q_VOID_2',
            'q_VOID_3',
            'q_VOID_4'
            ]

statesRETURN = [
            'q_RETURN_1',
            'q_RETURN_2',
            'q_RETURN_3',
            'q_RETURN_4',
            'q_RETURN_5',
            'q_RETURN_6'
            ]

statesIF = [
            'q_IF_1'
            ]

statesELSE = [
            'q_ELSE_1',
            'q_ELSE_2',
            'q_ELSE_3',
            'q_ELSE_4'
            ]

statesLPAREN = [
            'q_LPAREN'
            ]

statesRPAREN = [
            'q_RPAREN'
            ]

statesLBRACKETS = [
            'q_LBRACKETS'
            ]

statesRBRACKETS = [
            'q_RBRACKETS'
            ]

statesLBRACES= [
            'q_LBRACES'
            ]

statesRBRACES= [
            'q_RBRACES'
            ]

statesSEMICOLON= [
            'q_SEMICOLON'
            ]

statesCOMMA= [
            'q_COMMA'
            ]

statesPLUS= [
            'q_PLUS'
            ]

statesMINUS= [
            'q_MINUS'
            ]

statesDIVIDE= [
            'q_DIVIDE'
            ]

statesTIMES= [
            'q_TIMES'
            ]

statesEQUALS= [
            'q_ATTRIBUTION_1',
            'q_ATTRIBUTION_2',
            'q_EQUALS_1',
            'q_EQUALS_2'
            ]

statesDIFFERENT= [
            'q_DIFFERENT_1',
            'q_DIFFERENT_2'
            ]

statesCOMMENT = [
            'q_COMMENT_1',
            'q_COMMENT_2',
            'q_COMMENT_3',
            'q_DIVIDE_SPACE',
            'q_DIVIDE_LINEBREAK',
            'q_DIVIDE_LPAREN',
            'q_DIVIDE_RPAREN',
            'q_DIVIDE_LBRACKETS',
            'q_DIVIDE_RBRACKETS',
            'q_DIVIDE_LBRACES',
            'q_DIVIDE_RBRACES',
            'q_DIVIDE_SEMICOLON',
            'q_DIVIDE_COMMA',
            'q_DIVIDE_PLUS',
            'q_DIVIDE_MINUS',
            'q_DIVIDE_DIVIDE',
            'q_DIVIDE_TIMES',
            'q_DIVIDE_NUMBER',
            'q_DIVIDE_ID'
            ]

statesNUMBER = [
            'q_NUMBER_1',
            'q_NUMBER_2'
            ]

statesID = [
            'q_ID_1',
            'q_ID_2',
            'q_ID_SPACE',
            'q_ID_LINEBREAK',
            'q_ID_LPAREN',
            'q_ID_RPAREN',
            'q_ID_LBRACKETS',
            'q_ID_RBRACKETS',
            'q_ID_LBRACES',
            'q_ID_RBRACES',
            'q_ID_SEMICOLON',
            'q_ID_COMMA',
            'q_ID_PLUS',
            'q_ID_MINUS',
            'q_ID_DIVIDE',
            'q_ID_TIMES'
            ]

states = statesInit
states += statesINT
states += statesFLOAT
states += statesVOID
states += statesRETURN
states += statesIF
states += statesELSE
states += statesLPAREN
states += statesRPAREN
states += statesLBRACKETS
states += statesRBRACKETS
states += statesLBRACES
states += statesRBRACES
states += statesSEMICOLON
states += statesCOMMA
states += statesPLUS
states += statesMINUS
states += statesDIVIDE
states += statesTIMES
states += statesEQUALS
states += statesDIFFERENT
states += statesCOMMENT
states += statesNUMBER
states += statesID

#
# TRANSTIONS
#

# Função para combinar as transições
def combine_transitions(*transition_dicts):
    # Criar um defaultdict para lidar com a combinação sem sobrescrever as transições
    combined = defaultdict(dict)

    for transition_dict in transition_dicts:
        for state, transitions in transition_dict.items():
            for symbol, next_state in transitions.items():
                # Se a transição já existir, não sobrescreve
                if symbol not in combined[state]:
                    combined[state][symbol] = next_state

    return dict(combined)

transitionsInit = {
    'q0': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsINT = {
    'q0': {
        'i': 'q_INT_1',
    },
    'q_INT_1': {
        'n': 'q_INT_2',
    },
    'q_INT_2': {
        't': 'q_INT_3',
    },
    'q_INT_3': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsFLOAT = {
    'q0': {
        'f': 'q_FLOAT_1',
    },
    'q_FLOAT_1': {
        'l': 'q_FLOAT_2',
    },
    'q_FLOAT_2': {
        'o': 'q_FLOAT_3',
    },
    'q_FLOAT_3': {
        'a': 'q_FLOAT_4',
    },
    'q_FLOAT_4': {
        't': 'q_FLOAT_5',
    },
    'q_FLOAT_5': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsVOID = {
    'q0': {
        'v': 'q_VOID_1',
    },
    'q_VOID_1': {
        'o': 'q_VOID_2',
    },
    'q_VOID_2': {
        'i': 'q_VOID_3',
    },
    'q_VOID_3': {
        'd': 'q_VOID_4',
    },
    'q_VOID_4': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsRETURN = {
    'q0': {
        'r': 'q_RETURN_1',
    },
    'q_RETURN_1': {
        'e': 'q_RETURN_2',
    },
    'q_RETURN_2': {
        't': 'q_RETURN_3',
    },
    'q_RETURN_3': {
        'u': 'q_RETURN_4',
    },
    'q_RETURN_4': {
        'r' : 'q_RETURN_5',
    },
    'q_RETURN_5': {
        'n' : 'q_RETURN_6',
    },
    'q_RETURN_6': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsIF = {
    'q_INT_1': {
        'f': 'q_IF_1',
    },
    'q_IF_1': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsELSE = {
    'q0': {
        'e': 'q_ELSE_1',
    },
    'q_ELSE_1': {
        'l': 'q_ELSE_2',
    },
    'q_ELSE_2': {
        's': 'q_ELSE_3',
    },
    'q_ELSE_3': {
        'e': 'q_ELSE_4',
    },
    'q_ELSE_4': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsLPAREN = {
    'q0': {
        '(': 'q_LPAREN',
    },
    'q_LPAREN': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[': 'q_LBRACKETS',
        ']': 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_INT_3': {
        '(' : 'q_LPAREN',
    },
    'q_FLOAT_5': {
        '(' : 'q_LPAREN',
    },
    'q_VOID_4': {
        '(' : 'q_LPAREN',
    },
    'q_RETURN_6': {
        '(' : 'q_LPAREN',
    },
    'q_IF_1': {
        '(' : 'q_LPAREN',
    },
    'q_ELSE_4': {
        '(' : 'q_LPAREN',
    },
    'q_NUMBER_1': {
        '(' : 'q_LPAREN',
    },
    'q_NUMBER_2': {
        '(' : 'q_LPAREN',
    },
    'q_DIVIDE_NUMBER': {
        '(' : 'q_LPAREN',
    },
    'q_ID_1': {
        '(' : 'q_LPAREN',
    },
    'q_ID_2': {
        '(' : 'q_LPAREN',
    },
    'q_DIVIDE_ID': {
        '(' : 'q_LPAREN',
    }
}

# Adicionar conexões de q_LPAREN para q_ID_1 com todas as letras do alfabeto
transitionsLPAREN['q_LPAREN'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_LPAREN para q_NUMBER_1 com todos os numeros
transitionsLPAREN['q_LPAREN'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_LPAREN para 'i': 'q_INT_1'
transitionsLPAREN['q_LPAREN'].update({'i': 'q_INT_1'})

# Mudar conexões de q_LPAREN para 'f': 'q_FLOAT_1'
transitionsLPAREN['q_LPAREN'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_LPAREN para 'v': 'q_VOID_1'
transitionsLPAREN['q_LPAREN'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_LPAREN para 'r': 'q_RETURN_1'
transitionsLPAREN['q_LPAREN'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_LPAREN para 'e': 'q_ELSE_1'
transitionsLPAREN['q_LPAREN'].update({'e': 'q_ELSE_1'})

transitionsRPAREN = {
    'q0': {
        ')': 'q_RPAREN',
    },
    'q_RPAREN': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[': 'q_LBRACKETS',
        ']': 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_INT_3': {
        ')' : 'q_RPAREN',
    },
    'q_IF_1': {
        ')' : 'q_RPAREN',
    },
    'q_ELSE_1': {
        ')' : 'q_RPAREN',
    },
    'q_FLOAT_5': {
        ')' : 'q_RPAREN',
    },
    'q_VOID_4': {
        ')' : 'q_RPAREN',
    },
    'q_RETURN_6': {
        ')' : 'q_RPAREN',
    },
    'q_NUMBER_1': {
        ')' : 'q_RPAREN',
    },
    'q_NUMBER_2': {
        ')' : 'q_RPAREN',
    },
    'q_DIVIDE_NUMBER': {
        ')' : 'q_RPAREN',
    },
    'q_ID_1': {
        ')' : 'q_RPAREN',
    },
    'q_ID_2': {
        ')' : 'q_RPAREN',
    },
    'q_DIVIDE_ID': {
        ')' : 'q_RPAREN',
    }
}

# Adicionar conexões de q_RPAREN para q_ID_1 com todas as letras do alfabeto
transitionsRPAREN['q_RPAREN'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_RPAREN para q_NUMBER_1 com todos os numeros
transitionsRPAREN['q_RPAREN'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_RPAREN para 'i': 'q_INT_1'
transitionsRPAREN['q_RPAREN'].update({'i': 'q_INT_1'})

# Mudar conexões de q_RPAREN para 'f': 'q_FLOAT_1'
transitionsRPAREN['q_RPAREN'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_RPAREN para 'v': 'q_VOID_1'
transitionsRPAREN['q_RPAREN'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_RPAREN para 'r': 'q_RETURN_1'
transitionsRPAREN['q_RPAREN'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_RPAREN para 'e': 'q_ELSE_1'
transitionsRPAREN['q_RPAREN'].update({'e': 'q_ELSE_1'})

transitionsLBRACKETS = {
    'q0': {
        '[': 'q_LBRACKETS',
    },
    'q_LBRACKETS': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[': 'q_LBRACKETS',
        ']': 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_INT_3': {
        '[': 'q_LBRACKETS',
    },
    'q_FLOAT_5': {
        '[': 'q_LBRACKETS',
    },
    'q_VOID_4': {
        '[': 'q_LBRACKETS',
    },
    'q_RETURN_6': {
        '[': 'q_LBRACKETS',
    },
    'q_IF_1': {
        '[': 'q_LBRACKETS',
    },
    'q_ELSE_4': {
        '[': 'q_LBRACKETS',
    },
    'q_NUMBER_1': {
        '[': 'q_LBRACKETS',
    },
    'q_NUMBER_2': {
        '[': 'q_LBRACKETS',
    },
    'q_DIVIDE_NUMBER': {
        '[': 'q_LBRACKETS',
    },
    'q_ID_1': {
        '[': 'q_LBRACKETS',
    },
    'q_ID_2': {
        '[': 'q_LBRACKETS',
    },
    'q_DIVIDE_ID': {
        '[': 'q_LBRACKETS',
    }
}

# Adicionar conexões de q_LBRACKETS para q_ID_1 com todas as letras do alfabeto
transitionsLBRACKETS['q_LBRACKETS'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_LBRACKETS para q_NUMBER_1 com todos os numeros
transitionsLBRACKETS['q_LBRACKETS'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_LBRACKETS para 'i': 'q_INT_1'
transitionsLBRACKETS['q_LBRACKETS'].update({'i': 'q_INT_1'})

# Mudar conexões de q_LBRACKETS para 'f': 'q_FLOAT_1'
transitionsLBRACKETS['q_LBRACKETS'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_LBRACKETS para 'v': 'q_VOID_1'
transitionsLBRACKETS['q_LBRACKETS'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_LBRACKETS para 'r': 'q_RETURN_1'
transitionsLBRACKETS['q_LBRACKETS'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_LBRACKETS para 'e': 'q_ELSE_1'
transitionsLBRACKETS['q_LBRACKETS'].update({'e': 'q_ELSE_1'})

transitionsRBRACKETS = {
    'q0': {
        ']': 'q_RBRACKETS',
    },
    'q_RBRACKETS': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[': 'q_LBRACKETS',
        ']': 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_INT_3': {
        ']': 'q_RBRACKETS',
    },
    'q_IF_1': {
        ']': 'q_RBRACKETS',
    },
    'q_ELSE_1': {
        ']': 'q_RBRACKETS',
    },
    'q_FLOAT_5': {
        ']': 'q_RBRACKETS',
    },
    'q_VOID_4': {
        ']': 'q_RBRACKETS',
    },
    'q_RETURN_6': {
        ']': 'q_RBRACKETS',
    },
    'q_NUMBER_1': {
        ']': 'q_RBRACKETS',
    },
    'q_NUMBER_2': {
        ']': 'q_RBRACKETS',
    },
    'q_DIVIDE_NUMBER': {
        ']': 'q_RBRACKETS',
    },
    'q_ID_1': {
        ']': 'q_RBRACKETS',
    },
    'q_ID_2': {
        ']': 'q_RBRACKETS',
    },
    'q_DIVIDE_ID': {
        ']': 'q_RBRACKETS',
    }
}

# Adicionar conexões de q_RBRACKETS para q_ID_1 com todas as letras do alfabeto
transitionsRBRACKETS['q_RBRACKETS'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_RBRACKETS para q_NUMBER_1 com todos os numeros
transitionsRBRACKETS['q_RBRACKETS'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_RBRACKETS para 'i': 'q_INT_1'
transitionsRBRACKETS['q_RBRACKETS'].update({'i': 'q_INT_1'})

# Mudar conexões de q_RBRACKETS para 'f': 'q_FLOAT_1'
transitionsRBRACKETS['q_RBRACKETS'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_RBRACKETS para 'v': 'q_VOID_1'
transitionsRBRACKETS['q_RBRACKETS'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_RBRACKETS para 'r': 'q_RETURN_1'
transitionsRBRACKETS['q_RBRACKETS'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_RBRACKETS para 'e': 'q_ELSE_1'
transitionsRBRACKETS['q_RBRACKETS'].update({'e': 'q_ELSE_1'})

transitionsLBRACES = {
    'q0': {
        '{': 'q_LBRACES',
    },
    'q_LBRACES': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsRBRACES = {
    'q0': {
        '}': 'q_RBRACES',
    },
    'q_RBRACES': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

transitionsSEMICOLON = {
    'q0': {
        ';': 'q_SEMICOLON',
    },
    'q_SEMICOLON': {
        '\n': 'q0',
        ' ' : 'q0',
    },
    'q_INT_3': {
        ';': 'q_SEMICOLON',
    },
    'q_IF_1': {
        ';': 'q_SEMICOLON',
    },
    'q_ELSE_1': {
        ';': 'q_SEMICOLON',
    },
    'q_FLOAT_5': {
        ';': 'q_SEMICOLON',
    },
    'q_VOID_4': {
        ';': 'q_SEMICOLON',
    },
    'q_RETURN_6': {
        ';': 'q_SEMICOLON',
    },
    'q_NUMBER_1': {
        ';': 'q_SEMICOLON',
    },
    'q_NUMBER_2': {
        ';': 'q_SEMICOLON',
    },
    'q_DIVIDE_NUMBER': {
        ';': 'q_SEMICOLON',
    },
    'q_ID_1': {
        ';': 'q_SEMICOLON',
    },
    'q_ID_2': {
        ';': 'q_SEMICOLON',
    },
    'q_DIVIDE_ID': {
        ';': 'q_SEMICOLON',
    }
}

transitionsCOMMA = {
    'q0': {
        ',': 'q_COMMA',
    },
    'q_COMMA': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[': 'q_LBRACKETS',
        ']': 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_INT_3': {
        ',' : 'q_COMMA',
    },
    'q_IF_1': {
        ';': 'q_SEMICOLON',
    },
    'q_ELSE_1': {
        ';': 'q_SEMICOLON',
    },
    'q_FLOAT_5': {
        ',' : 'q_COMMA',
    },
    'q_VOID_4': {
        ',' : 'q_COMMA',
    },
    'q_RETURN_6': {
        ',' : 'q_COMMA',
    },
    'q_NUMBER_1': {
        ',' : 'q_COMMA',
    },
    'q_NUMBER_2': {
        ',' : 'q_COMMA',
    },
    'q_DIVIDE_NUMBER': {
        ',' : 'q_COMMA',
    },
    'q_ID_1': {
        ',' : 'q_COMMA',
    },
    'q_ID_2': {
        ',' : 'q_COMMA',
    },
    'q_DIVIDE_ID': {
        ',' : 'q_COMMA',
    }
}

# Adicionar conexões de q_COMMA para q_ID_1 com todas as letras do alfabeto
transitionsCOMMA['q_COMMA'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_COMMA para q_NUMBER_1 com todos os numeros
transitionsCOMMA['q_COMMA'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_COMMA para 'i': 'q_INT_1'
transitionsCOMMA['q_COMMA'].update({'i': 'q_INT_1'})

# Mudar conexões de q_COMMA para 'f': 'q_FLOAT_1'
transitionsCOMMA['q_COMMA'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_COMMA para 'v': 'q_VOID_1'
transitionsCOMMA['q_COMMA'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_COMMA para 'r': 'q_RETURN_1'
transitionsCOMMA['q_COMMA'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_COMMA para 'e': 'q_ELSE_1'
transitionsCOMMA['q_COMMA'].update({'e': 'q_ELSE_1'})

transitionsPLUS = {
    'q0': {
        '+' : 'q_PLUS',
    },
    'q_PLUS': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[': 'q_LBRACKETS',
        ']': 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_INT_3': {
        '+' : 'q_PLUS',
    },
    'q_IF_1': {
        '+' : 'q_PLUS',
    },
    'q_ELSE_1': {
        '+' : 'q_PLUS',
    },
    'q_FLOAT_5': {
        '+' : 'q_PLUS',
    },
    'q_VOID_4': {
        '+' : 'q_PLUS',
    },
    'q_RETURN_6': {
        '+' : 'q_PLUS',
    },
    'q_NUMBER_1': {
        '+' : 'q_PLUS',
    },
    'q_NUMBER_2': {
        '+' : 'q_PLUS',
    },
    'q_DIVIDE_NUMBER': {
        '+' : 'q_PLUS',
    },
    'q_ID_1': {
        '+' : 'q_PLUS',
    },
    'q_ID_2': {
        '+' : 'q_PLUS',
    },
    'q_DIVIDE_ID': {
        '+' : 'q_PLUS',
    }
}

# Adicionar conexões de q_PLUS para q_ID_1 com todas as letras do alfabeto
transitionsPLUS['q_PLUS'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_PLUS para q_NUMBER_1 com todos os numeros
transitionsPLUS['q_PLUS'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_PLUS para 'i': 'q_INT_1'
transitionsPLUS['q_PLUS'].update({'i': 'q_INT_1'})

# Mudar conexões de q_PLUS para 'f': 'q_FLOAT_1'
transitionsPLUS['q_PLUS'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_PLUS para 'v': 'q_VOID_1'
transitionsPLUS['q_PLUS'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_PLUS para 'r': 'q_RETURN_1'
transitionsPLUS['q_PLUS'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_PLUS para 'e': 'q_ELSE_1'
transitionsPLUS['q_PLUS'].update({'e': 'q_ELSE_1'})

transitionsMINUS = {
    'q0': {
        '-' : 'q_MINUS',
    },
    'q_MINUS': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[': 'q_LBRACKETS',
        ']': 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_INT_3': {
        '-' : 'q_MINUS',
    },
    'q_IF_1': {
        '-' : 'q_MINUS',
    },
    'q_ELSE_1': {
        '-' : 'q_MINUS',
    },
    'q_FLOAT_5': {
        '-' : 'q_MINUS',
    },
    'q_VOID_4': {
        '-' : 'q_MINUS',
    },
    'q_RETURN_6': {
        '-' : 'q_MINUS',
    },
    'q_NUMBER_1': {
        '-' : 'q_MINUS',
    },
    'q_NUMBER_2': {
        '-' : 'q_MINUS',
    },
    'q_DIVIDE_NUMBER': {
        '-' : 'q_MINUS',
    },
    'q_ID_1': {
        '-' : 'q_MINUS',
    },
    'q_ID_2': {
        '-' : 'q_MINUS',
    },
    'q_DIVIDE_ID': {
        '-' : 'q_MINUS',
    }
}

# Adicionar conexões de q_MINUS para q_ID_1 com todas as letras do alfabeto
transitionsMINUS['q_MINUS'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_MINUS para q_NUMBER_1 com todos os numeros
transitionsMINUS['q_MINUS'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_MINUS para 'i': 'q_INT_1'
transitionsMINUS['q_MINUS'].update({'i': 'q_INT_1'})

# Mudar conexões de q_MINUS para 'f': 'q_FLOAT_1'
transitionsMINUS['q_MINUS'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_MINUS para 'v': 'q_VOID_1'
transitionsMINUS['q_MINUS'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_MINUS para 'r': 'q_RETURN_1'
transitionsMINUS['q_MINUS'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_MINUS para 'e': 'q_ELSE_1'
transitionsMINUS['q_MINUS'].update({'e': 'q_ELSE_1'})

transitionsDIVIDE = {
    'q_DIVIDE': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[': 'q_LBRACKETS',
        ']': 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_INT_3': {
        '/' : 'q_COMMENT_1',
    },
    'q_IF_1': {
        '/' : 'q_COMMENT_1',
    },
    'q_ELSE_1': {
        '/' : 'q_COMMENT_1',
    },
    'q_FLOAT_5': {
        '/' : 'q_COMMENT_1',
    },
    'q_VOID_4': {
        '/' : 'q_COMMENT_1',
    },
    'q_RETURN_6': {
        '/' : 'q_COMMENT_1',
    },
    'q_NUMBER_1': {
        '/' : 'q_COMMENT_1',
    },
    'q_NUMBER_2': {
        '/' : 'q_COMMENT_1',
    },
    'q_DIVIDE_NUMBER': {
        '/' : 'q_COMMENT_1',
    },
    'q_ID_1': {
        '/' : 'q_COMMENT_1',
    },
    'q_ID_2': {
        '/' : 'q_COMMENT_1',
    },
    'q_DIVIDE_ID': {
        '/' : 'q_COMMENT_1',
    }
}

# Adicionar conexões de q_DIVIDE para q_ID_1 com todas as letras do alfabeto
transitionsDIVIDE['q_DIVIDE'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_DIVIDE para q_NUMBER_1 com todos os numeros
transitionsDIVIDE['q_DIVIDE'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_DIVIDE para 'i': 'q_INT_1'
transitionsDIVIDE['q_DIVIDE'].update({'i': 'q_INT_1'})

# Mudar conexões de q_DIVIDE para 'f': 'q_FLOAT_1'
transitionsDIVIDE['q_DIVIDE'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_DIVIDE para 'v': 'q_VOID_1'
transitionsDIVIDE['q_DIVIDE'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_DIVIDE para 'r': 'q_RETURN_1'
transitionsDIVIDE['q_DIVIDE'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_DIVIDE para 'e': 'q_ELSE_1'
transitionsDIVIDE['q_DIVIDE'].update({'e': 'q_ELSE_1'})

transitionsTIMES = {
    'q0': {
        '*' : 'q_TIMES',
    },
    'q_TIMES': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[': 'q_LBRACKETS',
        ']': 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_INT_3': {
        '*' : 'q_TIMES',
    },
    'q_IF_1': {
        '*' : 'q_TIMES',
    },
    'q_ELSE_1': {
        '*' : 'q_TIMES',
    },
    'q_FLOAT_5': {
        '*' : 'q_TIMES',
    },
    'q_VOID_4': {
        '*' : 'q_TIMES',
    },
    'q_RETURN_6': {
        '*' : 'q_TIMES',
    },
    'q_NUMBER_1': {
        '*' : 'q_TIMES',
    },
    'q_NUMBER_2': {
        '*' : 'q_TIMES',
    },
    'q_DIVIDE_NUMBER': {
        '*' : 'q_TIMES',
    },
    'q_ID_1': {
        '*' : 'q_TIMES',
    },
    'q_ID_2': {
        '*' : 'q_TIMES',
    },
    'q_DIVIDE_ID': {
        '*' : 'q_TIMES',
    }
}

# Adicionar conexões de q_TIMES para q_ID_1 com todas as letras do alfabeto
transitionsTIMES['q_TIMES'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_TIMES para q_NUMBER_1 com todos os numeros
transitionsTIMES['q_TIMES'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_TIMES para 'i': 'q_INT_1'
transitionsTIMES['q_TIMES'].update({'i': 'q_INT_1'})

# Mudar conexões de q_TIMES para 'f': 'q_FLOAT_1'
transitionsTIMES['q_TIMES'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_TIMES para 'v': 'q_VOID_1'
transitionsTIMES['q_TIMES'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_TIMES para 'r': 'q_RETURN_1'
transitionsTIMES['q_TIMES'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_TIMES para 'e': 'q_ELSE_1'
transitionsTIMES['q_TIMES'].update({'e': 'q_ELSE_1'})

transitionsEQUALS = {
    'q0': {
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_ATTRIBUTION_1': {
        '\n': 'q_ATTRIBUTION_2',
        ' ' : 'q_ATTRIBUTION_2',
        '=' : 'q_EQUALS_1',
    },
    'q_ATTRIBUTION_2': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[': 'q_LBRACKETS',
        ']': 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
    },
    'q_EQUALS_1': {
        '\n': 'q_EQUALS_2',
        ' ' : 'q_EQUALS_2',
    },
    'q_EQUALS_2': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[': 'q_LBRACKETS',
        ']': 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    }
}

"""
    Busca por todas as opções possiveis após q_ATTRIBUTION_2
"""

# Adicionar conexões de q_ATTRIBUTION_2 para q_ID_1 com todas as letras do alfabeto
transitionsEQUALS['q_ATTRIBUTION_2'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_ATTRIBUTION_2 para q_NUMBER_1 com todos os numeros
transitionsEQUALS['q_ATTRIBUTION_2'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_ATTRIBUTION_2 para 'i': 'q_INT_1'
transitionsEQUALS['q_ATTRIBUTION_2'].update({'i': 'q_INT_1'})

# Mudar conexões de q_ATTRIBUTION_2 para 'f': 'q_FLOAT_1'
transitionsEQUALS['q_ATTRIBUTION_2'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_ATTRIBUTION_2 para 'v': 'q_VOID_1'
transitionsEQUALS['q_ATTRIBUTION_2'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_ATTRIBUTION_2 para 'r': 'q_RETURN_6'
transitionsEQUALS['q_ATTRIBUTION_2'].update({'r': 'q_RETURN_6'})

"""
    Busca por todas as opções possiveis após q_EQUALS_2
"""

# Adicionar conexões de q_EQUALS_2 para q_ID_1 com todas as letras do alfabeto
transitionsEQUALS['q_EQUALS_2'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_EQUALS_2 para q_NUMBER_1 com todos os numeros
transitionsEQUALS['q_EQUALS_2'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_EQUALS_2 para 'i': 'q_INT_1'
transitionsEQUALS['q_EQUALS_2'].update({'i': 'q_INT_1'})

# Mudar conexões de q_EQUALS_2 para 'f': 'q_FLOAT_1'
transitionsEQUALS['q_EQUALS_2'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_EQUALS_2 para 'v': 'q_VOID_1'
transitionsEQUALS['q_EQUALS_2'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_EQUALS_2 para 'r': 'q_RETURN_6'
transitionsEQUALS['q_EQUALS_2'].update({'r': 'q_RETURN_6'})

transitionsDIFFERENT = {
    'q0': {
        '!' : 'q_DIFFERENT_1',
    },
    'q_DIFFERENT_1': {
        '=' : 'q_DIFFERENT_2',
    },
    'q_DIFFERENT_2': {
        ' ' : 'q0',
        '\n': 'q0',
    }
}

transitionsCOMMENT = {
    'q0': {
        '/': 'q_COMMENT_1',
    },
    'q_COMMENT_1': {
        '*': 'q_COMMENT_2',
        ' ' : 'q_DIVIDE_SPACE',
        '\n': 'q_DIVIDE_LINEBREAK',
        '(' : 'q_DIVIDE_LPAREN',
        ')' : 'q_DIVIDE_RPAREN',
        '[' : 'q_DIVIDE_LBRACKETS',
        ']' : 'q_DIVIDE_RBRACKETS',
        '{' : 'q_DIVIDE_LBRACES',
        '}' : 'q_DIVIDE_RBRACES',
        ';' : 'q_DIVIDE_SEMICOLON',
        ',' : 'q_DIVIDE_COMMA',
        '+' : 'q_DIVIDE_PLUS',
        '-' : 'q_DIVIDE_MINUS',
        '/' : 'q_DIVIDE_DIVIDE',
    },
    'q_COMMENT_2': {
        '*': 'q_COMMENT_3',
    },
    'q_COMMENT_3': {
        '/': 'q0',
    },
    'q_DIVIDE_SPACE': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_LINEBREAK': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_LPAREN': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_RPAREN': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_LBRACKETS': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_RBRACKETS': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_LBRACES': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_RBRACES': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_SEMICOLON': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_COMMA': {
        '\n': 'q0',
        ' ' : 'q0',
        '(': 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_PLUS': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_MINUS': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_DIVIDE': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_TIMES': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_NUMBER': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_DIVIDE_ID': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    }
}

# Adicionar conexões de q_COMMENT_2 para q_COMMENT_2 com todos os numeros
transitionsCOMMENT['q_COMMENT_2'].update({item: 'q_COMMENT_2' for item in fullList})

# Adicionar conexões de q_COMMENT_2 para '*': 'q_COMMENT_3'
transitionsCOMMENT['q_COMMENT_2'].update({'*': 'q_COMMENT_3'})

# Adicionar conexões de q_COMMENT_3 para q_COMMENT_2 com todos os numeros
transitionsCOMMENT['q_COMMENT_3'].update({item: 'q_COMMENT_2' for item in fullList})

# Adicionar conexões de q_COMMENT_3 para '*': 'q_COMMENT_3'
transitionsCOMMENT['q_COMMENT_3'].update({'*': 'q_COMMENT_3'})

# Adicionar conexões de q_COMMENT_3 para '/': 'q0'
transitionsCOMMENT['q_COMMENT_3'].update({'/': 'q0'})

"""
    DIVIDE seguido de SPACE
"""

# Adicionar conexões de q_DIVIDE_SPACE para q_ID_1 com todas as letras do alfabeto
transitionsCOMMENT['q_DIVIDE_SPACE'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_DIVIDE_SPACE para q_NUMBER_1 com todos os numeros
transitionsCOMMENT['q_DIVIDE_SPACE'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_DIVIDE_SPACE para 'i': 'q_INT_1'
transitionsCOMMENT['q_DIVIDE_SPACE'].update({'i': 'q_INT_1'})

# Mudar conexões de q_DIVIDE_SPACE para 'f': 'q_FLOAT_1'
transitionsCOMMENT['q_DIVIDE_SPACE'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_DIVIDE_SPACE para 'v': 'q_VOID_1'
transitionsCOMMENT['q_DIVIDE_SPACE'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_DIVIDE_SPACE para 'r': 'q_RETURN_1'
transitionsCOMMENT['q_DIVIDE_SPACE'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_DIVIDE_SPACE para 'e': 'q_ELSE_1'
transitionsCOMMENT['q_DIVIDE_SPACE'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de LINEBREAK
"""

# Adicionar conexões de q_DIVIDE_LINEBREAK para q_ID_1 com todas as letras do alfabeto
transitionsCOMMENT['q_DIVIDE_LINEBREAK'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_DIVIDE_LINEBREAK para q_NUMBER_1 com todos os numeros
transitionsCOMMENT['q_DIVIDE_LINEBREAK'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_DIVIDE_LINEBREAK para 'i': 'q_INT_1'
transitionsCOMMENT['q_DIVIDE_LINEBREAK'].update({'i': 'q_INT_1'})

# Mudar conexões de q_DIVIDE_LINEBREAK para 'f': 'q_FLOAT_1'
transitionsCOMMENT['q_DIVIDE_LINEBREAK'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_DIVIDE_LINEBREAK para 'v': 'q_VOID_1'
transitionsCOMMENT['q_DIVIDE_LINEBREAK'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_DIVIDE_LINEBREAK para 'r': 'q_RETURN_1'
transitionsCOMMENT['q_DIVIDE_LINEBREAK'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_DIVIDE_LINEBREAK para 'e': 'q_ELSE_1'
transitionsCOMMENT['q_DIVIDE_LINEBREAK'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de LPAREN
"""

# Adicionar conexões de q_DIVIDE_LPAREN para q_ID_1 com todas as letras do alfabeto
transitionsCOMMENT['q_DIVIDE_LPAREN'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_DIVIDE_LPAREN para q_NUMBER_1 com todos os numeros
transitionsCOMMENT['q_DIVIDE_LPAREN'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_DIVIDE_LPAREN para 'i': 'q_INT_1'
transitionsCOMMENT['q_DIVIDE_LPAREN'].update({'i': 'q_INT_1'})

# Mudar conexões de q_DIVIDE_LPAREN para 'f': 'q_FLOAT_1'
transitionsCOMMENT['q_DIVIDE_LPAREN'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_DIVIDE_LPAREN para 'v': 'q_VOID_1'
transitionsCOMMENT['q_DIVIDE_LPAREN'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_DIVIDE_LPAREN para 'r': 'q_RETURN_1'
transitionsCOMMENT['q_DIVIDE_LPAREN'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_DIVIDE_LPAREN para 'e': 'q_ELSE_1'
transitionsCOMMENT['q_DIVIDE_LPAREN'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de RPAREN
"""

# Adicionar conexões de q_DIVIDE_RPAREN para q_ID_1 com todas as letras do alfabeto
transitionsCOMMENT['q_DIVIDE_RPAREN'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_DIVIDE_RPAREN para q_NUMBER_1 com todos os numeros
transitionsCOMMENT['q_DIVIDE_RPAREN'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_DIVIDE_RPAREN para 'i': 'q_INT_1'
transitionsCOMMENT['q_DIVIDE_RPAREN'].update({'i': 'q_INT_1'})

# Mudar conexões de q_DIVIDE_RPAREN para 'f': 'q_FLOAT_1'
transitionsCOMMENT['q_DIVIDE_RPAREN'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_DIVIDE_RPAREN para 'v': 'q_VOID_1'
transitionsCOMMENT['q_DIVIDE_RPAREN'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_DIVIDE_RPAREN para 'r': 'q_RETURN_1'
transitionsCOMMENT['q_DIVIDE_RPAREN'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_DIVIDE_RPAREN para 'e': 'q_ELSE_1'
transitionsCOMMENT['q_DIVIDE_RPAREN'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de COMMA
"""

# Adicionar conexões de q_DIVIDE_COMMA para q_ID_1 com todas as letras do alfabeto
transitionsCOMMENT['q_DIVIDE_COMMA'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_DIVIDE_COMMA para q_NUMBER_1 com todos os numeros
transitionsCOMMENT['q_DIVIDE_COMMA'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_DIVIDE_COMMA para 'i': 'q_INT_1'
transitionsCOMMENT['q_DIVIDE_COMMA'].update({'i': 'q_INT_1'})

# Mudar conexões de q_DIVIDE_COMMA para 'f': 'q_FLOAT_1'
transitionsCOMMENT['q_DIVIDE_COMMA'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_DIVIDE_COMMA para 'v': 'q_VOID_1'
transitionsCOMMENT['q_DIVIDE_COMMA'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_DIVIDE_COMMA para 'e': 'q_ELSE_1'
transitionsCOMMENT['q_DIVIDE_COMMA'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de PLUS
"""

# Adicionar conexões de q_DIVIDE_PLUS para q_ID_1 com todas as letras do alfabeto
transitionsCOMMENT['q_DIVIDE_PLUS'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_DIVIDE_PLUS para q_NUMBER_1 com todos os numeros
transitionsCOMMENT['q_DIVIDE_PLUS'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_DIVIDE_PLUS para 'i': 'q_INT_1'
transitionsCOMMENT['q_DIVIDE_PLUS'].update({'i': 'q_INT_1'})

# Mudar conexões de q_DIVIDE_PLUS para 'f': 'q_FLOAT_1'
transitionsCOMMENT['q_DIVIDE_PLUS'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_DIVIDE_PLUS para 'v': 'q_VOID_1'
transitionsCOMMENT['q_DIVIDE_PLUS'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_DIVIDE_PLUS para 'r': 'q_RETURN_1'
transitionsCOMMENT['q_DIVIDE_PLUS'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_DIVIDE_PLUS para 'e': 'q_ELSE_1'
transitionsCOMMENT['q_DIVIDE_PLUS'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de MINUS
"""

# Adicionar conexões de q_DIVIDE_MINUS para q_ID_1 com todas as letras do alfabeto
transitionsCOMMENT['q_DIVIDE_MINUS'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_DIVIDE_MINUS para q_NUMBER_1 com todos os numeros
transitionsCOMMENT['q_DIVIDE_MINUS'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_DIVIDE_MINUS para 'i': 'q_INT_1'
transitionsCOMMENT['q_DIVIDE_MINUS'].update({'i': 'q_INT_1'})

# Mudar conexões de q_DIVIDE_MINUS para 'f': 'q_FLOAT_1'
transitionsCOMMENT['q_DIVIDE_MINUS'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_DIVIDE_MINUS para 'v': 'q_VOID_1'
transitionsCOMMENT['q_DIVIDE_MINUS'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_DIVIDE_MINUS para 'r': 'q_RETURN_1'
transitionsCOMMENT['q_DIVIDE_MINUS'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_DIVIDE_MINUS para 'e': 'q_ELSE_1'
transitionsCOMMENT['q_DIVIDE_MINUS'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de DIVIDE
"""

# Adicionar conexões de q_DIVIDE_DIVIDE para q_ID_1 com todas as letras do alfabeto
transitionsCOMMENT['q_DIVIDE_DIVIDE'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_DIVIDE_DIVIDE para q_NUMBER_1 com todos os numeros
transitionsCOMMENT['q_DIVIDE_DIVIDE'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_DIVIDE_DIVIDE para 'i': 'q_INT_1'
transitionsCOMMENT['q_DIVIDE_DIVIDE'].update({'i': 'q_INT_1'})

# Mudar conexões de q_DIVIDE_DIVIDE para 'f': 'q_FLOAT_1'
transitionsCOMMENT['q_DIVIDE_DIVIDE'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_DIVIDE_DIVIDE para 'v': 'q_VOID_1'
transitionsCOMMENT['q_DIVIDE_DIVIDE'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_DIVIDE_DIVIDE para 'r': 'q_RETURN_1'
transitionsCOMMENT['q_DIVIDE_DIVIDE'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_DIVIDE_DIVIDE para 'e': 'q_ELSE_1'
transitionsCOMMENT['q_DIVIDE_DIVIDE'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de TIMES
"""

# Adicionar conexões de q_DIVIDE_TIMES para q_ID_1 com todas as letras do alfabeto
transitionsCOMMENT['q_DIVIDE_TIMES'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_DIVIDE_TIMES para q_NUMBER_1 com todos os numeros
transitionsCOMMENT['q_DIVIDE_TIMES'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_DIVIDE_TIMES para 'i': 'q_INT_1'
transitionsCOMMENT['q_DIVIDE_TIMES'].update({'i': 'q_INT_1'})

# Mudar conexões de q_DIVIDE_TIMES para 'f': 'q_FLOAT_1'
transitionsCOMMENT['q_DIVIDE_TIMES'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_DIVIDE_TIMES para 'v': 'q_VOID_1'
transitionsCOMMENT['q_DIVIDE_TIMES'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_DIVIDE_TIMES para 'r': 'q_RETURN_1'
transitionsCOMMENT['q_DIVIDE_TIMES'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_DIVIDE_TIMES para 'e': 'q_ELSE_1'
transitionsCOMMENT['q_DIVIDE_TIMES'].update({'e': 'q_ELSE_1'})

"""
    DIVIDE seguido de NUMBER
"""

# Adicionar conexões de q_COMMENT_1 para q_NUMBER_1 com todos os numeros
transitionsCOMMENT['q_COMMENT_1'].update({number: 'q_DIVIDE_NUMBER' for number in numbers})

# Adicionar conexões de q_DIVIDE_NUMBER para q_NUMBER_2 com todos os numeros
transitionsCOMMENT['q_DIVIDE_NUMBER'].update({number: 'q_NUMBER_2' for number in numbers})

"""
    DIVIDE seguido de ID
"""

# Adicionar conexões de q_COMMENT_1 para DIVIDE_ID com todas as letras do alfabeto
transitionsCOMMENT['q_COMMENT_1'].update({letter: 'q_DIVIDE_ID' for letter in alphabet})

# Adicionar conexões de q_DIVIDE_ID para q_ID_2 com todas as letras do alfabeto e todos os numeros
transitionsCOMMENT['q_DIVIDE_ID'].update({letter: 'q_ID_2' for letter in alphabet})
transitionsCOMMENT['q_DIVIDE_ID'].update({number: 'q_ID_2' for number in numbers})

transitionsNUMBER = {
    'q0': {
        
    },
    'q_NUMBER_1': {
        '\n': 'q0',
        ' ' : 'q0',
    },
    'q_NUMBER_2': {
        '\n': 'q0',
        ' ' : 'q0',
    }
}

# Adicionar conexões de q0 para q_NUMBER_1 com todos os numeros
transitionsNUMBER['q0'].update({number: 'q_NUMBER_1' for number in numbers})

# Adicionar conexões de q_NUMBER_1 para q_NUMBER_2 com todos os numeros
transitionsNUMBER['q_NUMBER_1'].update({number: 'q_NUMBER_2' for number in numbers})

# Adicionar conexões de q_NUMBER_2 para q_NUMBER_2 com todos os numeros
transitionsNUMBER['q_NUMBER_2'].update({number: 'q_NUMBER_2' for number in numbers})

transitionsID = {
    'q0': {
        
    },
    'q_ID_1': {
        '\n': 'q0',
        ' ' : 'q0',
    },
    'q_ID_2': {
        '\n': 'q0',
        ' ' : 'q0',
    },
    'q_ID_SPACE': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_ID_LINEBREAK': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_ID_LPAREN': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_ID_RPAREN': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_ID_LBRACES': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_ID_RBRACES': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_ID_SEMICOLON': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_ID_COMMA': {
        '\n': 'q0',
        ' ' : 'q0',
        '(': 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_ID_PLUS': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_ID_MINUS': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_ID_DIVIDE': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_ID_TIMES': {
        '\n': 'q0',
        ' ' : 'q0',
        '(' : 'q_LPAREN',
        ')' : 'q_RPAREN',
        '[' : 'q_LBRACKETS',
        ']' : 'q_RBRACKETS',
        '{' : 'q_LBRACES',
        '}' : 'q_RBRACES',
        ';' : 'q_SEMICOLON',
        ',' : 'q_COMMA',
        '+' : 'q_PLUS',
        '-' : 'q_MINUS',
        '/' : 'q_COMMENT_1',
        '*' : 'q_TIMES',
        '=' : 'q_ATTRIBUTION_1',
    },
    'q_INT_1': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_INT_2': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_INT_3': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_IF_1': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_ELSE_1': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_ELSE_2': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_ELSE_3': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_ELSE_4': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_FLOAT_1': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_FLOAT_2': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_FLOAT_3': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_FLOAT_4': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_FLOAT_5': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_VOID_1': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_VOID_2': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_VOID_3': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_VOID_4': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_RETURN_1': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_RETURN_2': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_RETURN_3': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_RETURN_4': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_RETURN_5': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    },
    'q_RETURN_6': {
        ' ' : 'q_ID_SPACE',
        '\n': 'q_ID_LINEBREAK',
        '(' : 'q_ID_LPAREN',
        ')' : 'q_ID_RPAREN',
        '[' : 'q_ID_LBRACKETS',
        ']' : 'q_ID_RBRACKETS',
        '{' : 'q_ID_LBRACES',
        '}' : 'q_ID_RBRACES',
        ';' : 'q_ID_SEMICOLON',
        ',' : 'q_ID_COMMA',
        '+' : 'q_ID_PLUS',
        '-' : 'q_ID_MINUS',
        '/' : 'q_ID_DIVIDE',
        '*' : 'q_ID_TIMES',
    }
}

# Adicionar conexões de q0 para q_ID_1 com todas as letras do alfabeto
transitionsID['q0'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_ID_1 para q_ID_2 com todas as letras do alfabeto e todos os numeros
transitionsID['q_ID_1'].update({letter: 'q_ID_2' for letter in alphabet})
transitionsID['q_ID_1'].update({number: 'q_ID_2' for number in numbers})

# Adicionar conexões de q_ID_2 para q_ID_2 com todas as letras do alfabeto e todos os numeros
transitionsID['q_ID_2'].update({letter: 'q_ID_2' for letter in alphabet})
transitionsID['q_ID_2'].update({number: 'q_ID_2' for number in numbers})

"""
    Busca de ID em meio a busca INT
"""

# Adicionar conexões de q_INT_1 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_INT_1'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_INT_1'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_INT_2 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_INT_2'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_INT_2'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_INT_3 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_INT_3'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_INT_3'].update({number: 'q_ID_1' for number in numbers})

"""
    Busca de ID em meio a busca FLOAT
"""

# Adicionar conexões de q_FLOAT_1 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_FLOAT_1'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_FLOAT_1'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_FLOAT_2 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_FLOAT_2'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_FLOAT_2'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_FLOAT_3 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_FLOAT_3'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_FLOAT_3'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_FLOAT_4 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_FLOAT_4'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_FLOAT_4'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_FLOAT_5 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_FLOAT_5'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_FLOAT_5'].update({number: 'q_ID_1' for number in numbers})

"""
    Busca de ID em meio a busca VOID
"""

# Adicionar conexões de q_VOID_1 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_VOID_1'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_VOID_1'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_VOID_2 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_VOID_2'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_VOID_2'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_VOID_3 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_VOID_3'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_VOID_3'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_VOID_4 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_VOID_4'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_VOID_4'].update({number: 'q_ID_1' for number in numbers})

"""
    Busca de ID em meio a busca RETURN
"""

# Adicionar conexões de q_RETURN_1 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_RETURN_1'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_RETURN_1'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_RETURN_2 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_RETURN_2'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_RETURN_2'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_RETURN_3 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_RETURN_3'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_RETURN_3'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_RETURN_4 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_RETURN_4'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_RETURN_4'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_RETURN_5 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_RETURN_5'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_RETURN_5'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_RETURN_6 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_RETURN_6'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_RETURN_6'].update({number: 'q_ID_1' for number in numbers})

"""
    Busca de ID em meio a busca IF
"""

# Adicionar conexões de q_IF_1 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_IF_1'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_IF_1'].update({number: 'q_ID_1' for number in numbers})

"""
    Busca de ID em meio a busca ELSE
"""

# Adicionar conexões de q_ELSE_1 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_ELSE_1'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_ELSE_1'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_ELSE_2 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_ELSE_2'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_ELSE_2'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_ELSE_3 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_ELSE_3'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_ELSE_3'].update({number: 'q_ID_1' for number in numbers})

# Adicionar conexões de q_ELSE_4 para q_ID_1 com todas as letras do alfabeto e todos os numeros
transitionsID['q_ELSE_4'].update({letter: 'q_ID_1' for letter in alphabet})
transitionsID['q_ELSE_4'].update({number: 'q_ID_1' for number in numbers})

"""
    ID seguido de SPACE
"""

# Adicionar conexões de q_ID_SPACE para q_ID_1 com todas as letras do alfabeto
transitionsID['q_ID_SPACE'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_ID_SPACE para q_NUMBER_1 com todos os numeros
transitionsID['q_ID_SPACE'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_ID_SPACE para 'i': 'q_INT_1'
transitionsID['q_ID_SPACE'].update({'i': 'q_INT_1'})

# Mudar conexões de q_ID_SPACE para 'f': 'q_FLOAT_1'
transitionsID['q_ID_SPACE'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_ID_SPACE para 'v': 'q_VOID_1'
transitionsID['q_ID_SPACE'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_ID_SPACE para 'r': 'q_RETURN_1'
transitionsID['q_ID_SPACE'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_ID_SPACE para 'e': 'q_ELSE_1'
transitionsID['q_ID_SPACE'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de LINEBREAK
"""

# Adicionar conexões de q_ID_LINEBREAK para q_ID_1 com todas as letras do alfabeto
transitionsID['q_ID_LINEBREAK'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_ID_LINEBREAK para q_NUMBER_1 com todos os numeros
transitionsID['q_ID_LINEBREAK'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_ID_LINEBREAK para 'i': 'q_INT_1'
transitionsID['q_ID_LINEBREAK'].update({'i': 'q_INT_1'})

# Mudar conexões de q_ID_LINEBREAK para 'f': 'q_FLOAT_1'
transitionsID['q_ID_LINEBREAK'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_ID_LINEBREAK para 'v': 'q_VOID_1'
transitionsID['q_ID_LINEBREAK'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_ID_LINEBREAK para 'r': 'q_RETURN_1'
transitionsID['q_ID_LINEBREAK'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_ID_LINEBREAK para 'e': 'q_ELSE_1'
transitionsID['q_ID_LINEBREAK'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de LPAREN
"""

# Adicionar conexões de q_ID_LPAREN para q_ID_1 com todas as letras do alfabeto
transitionsID['q_ID_LPAREN'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_ID_LPAREN para q_NUMBER_1 com todos os numeros
transitionsID['q_ID_LPAREN'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_ID_LPAREN para 'i': 'q_INT_1'
transitionsID['q_ID_LPAREN'].update({'i': 'q_INT_1'})

# Mudar conexões de q_ID_LPAREN para 'f': 'q_FLOAT_1'
transitionsID['q_ID_LPAREN'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_ID_LPAREN para 'v': 'q_VOID_1'
transitionsID['q_ID_LPAREN'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_ID_LPAREN para 'r': 'q_RETURN_1'
transitionsID['q_ID_LPAREN'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_ID_LPAREN para 'e': 'q_ELSE_1'
transitionsID['q_ID_LPAREN'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de RPAREN
"""

# Adicionar conexões de q_ID_RPAREN para q_ID_1 com todas as letras do alfabeto
transitionsID['q_ID_RPAREN'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_ID_RPAREN para q_NUMBER_1 com todos os numeros
transitionsID['q_ID_RPAREN'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_ID_RPAREN para 'i': 'q_INT_1'
transitionsID['q_ID_RPAREN'].update({'i': 'q_INT_1'})

# Mudar conexões de q_ID_RPAREN para 'f': 'q_FLOAT_1'
transitionsID['q_ID_RPAREN'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_ID_RPAREN para 'v': 'q_VOID_1'
transitionsID['q_ID_RPAREN'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_ID_RPAREN para 'r': 'q_RETURN_1'
transitionsID['q_ID_RPAREN'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_ID_RPAREN para 'e': 'q_ELSE_1'
transitionsID['q_ID_RPAREN'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de COMMA
"""

# Adicionar conexões de q_ID_COMMA para q_ID_1 com todas as letras do alfabeto
transitionsID['q_ID_COMMA'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_ID_COMMA para q_NUMBER_1 com todos os numeros
transitionsID['q_ID_COMMA'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_ID_COMMA para 'i': 'q_INT_1'
transitionsID['q_ID_COMMA'].update({'i': 'q_INT_1'})

# Mudar conexões de q_ID_COMMA para 'f': 'q_FLOAT_1'
transitionsID['q_ID_COMMA'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_ID_COMMA para 'v': 'q_VOID_1'
transitionsID['q_ID_COMMA'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_ID_COMMA para 'r': 'q_RETURN_1'
transitionsID['q_ID_COMMA'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_ID_COMMA para 'e': 'q_ELSE_1'
transitionsID['q_ID_COMMA'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de PLUS
"""

# Adicionar conexões de q_ID_PLUS para q_ID_1 com todas as letras do alfabeto
transitionsID['q_ID_PLUS'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_ID_PLUS para q_NUMBER_1 com todos os numeros
transitionsID['q_ID_PLUS'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_ID_PLUS para 'i': 'q_INT_1'
transitionsID['q_ID_PLUS'].update({'i': 'q_INT_1'})

# Mudar conexões de q_ID_PLUS para 'f': 'q_FLOAT_1'
transitionsID['q_ID_PLUS'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_ID_PLUS para 'v': 'q_VOID_1'
transitionsID['q_ID_PLUS'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_ID_PLUS para 'r': 'q_RETURN_1'
transitionsID['q_ID_PLUS'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_ID_PLUS para 'e': 'q_ELSE_1'
transitionsID['q_ID_PLUS'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de MINUS
"""

# Adicionar conexões de q_ID_MINUS para q_ID_1 com todas as letras do alfabeto
transitionsID['q_ID_MINUS'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_ID_MINUS para q_NUMBER_1 com todos os numeros
transitionsID['q_ID_MINUS'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_ID_MINUS para 'i': 'q_INT_1'
transitionsID['q_ID_MINUS'].update({'i': 'q_INT_1'})

# Mudar conexões de q_ID_MINUS para 'f': 'q_FLOAT_1'
transitionsID['q_ID_MINUS'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_ID_MINUS para 'v': 'q_VOID_1'
transitionsID['q_ID_MINUS'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_ID_MINUS para 'r': 'q_RETURN_1'
transitionsID['q_ID_MINUS'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_ID_MINUS para 'e': 'q_ELSE_1'
transitionsID['q_ID_MINUS'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de DIVIDE
"""

# Adicionar conexões de q_ID_DIVIDE para q_ID_1 com todas as letras do alfabeto
transitionsID['q_ID_DIVIDE'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_ID_DIVIDE para q_NUMBER_1 com todos os numeros
transitionsID['q_ID_DIVIDE'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_ID_DIVIDE para 'i': 'q_INT_1'
transitionsID['q_ID_DIVIDE'].update({'i': 'q_INT_1'})

# Mudar conexões de q_ID_DIVIDE para 'f': 'q_FLOAT_1'
transitionsID['q_ID_DIVIDE'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_ID_DIVIDE para 'v': 'q_VOID_1'
transitionsID['q_ID_DIVIDE'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_ID_DIVIDE para 'r': 'q_RETURN_1'
transitionsID['q_ID_DIVIDE'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_ID_DIVIDE para 'e': 'q_ELSE_1'
transitionsID['q_ID_DIVIDE'].update({'e': 'q_ELSE_1'})

"""
    ID seguido de TIMES
"""

# Adicionar conexões de q_ID_TIMES para q_ID_1 com todas as letras do alfabeto
transitionsID['q_ID_TIMES'].update({letter: 'q_ID_1' for letter in alphabet})

# Adicionar conexões de q_ID_TIMES para q_NUMBER_1 com todos os numeros
transitionsID['q_ID_TIMES'].update({number: 'q_NUMBER_1' for number in numbers})

# Mudar conexões de q_ID_TIMES para 'i': 'q_INT_1'
transitionsID['q_ID_TIMES'].update({'i': 'q_INT_1'})

# Mudar conexões de q_ID_TIMES para 'f': 'q_FLOAT_1'
transitionsID['q_ID_TIMES'].update({'f': 'q_FLOAT_1'})

# Mudar conexões de q_ID_TIMES para 'v': 'q_VOID_1'
transitionsID['q_ID_TIMES'].update({'v': 'q_VOID_1'})

# Mudar conexões de q_ID_TIMES para 'r': 'q_RETURN_1'
transitionsID['q_ID_TIMES'].update({'r': 'q_RETURN_1'})

# Mudar conexões de q_ID_TIMES para 'e': 'q_ELSE_1'
transitionsID['q_ID_TIMES'].update({'e': 'q_ELSE_1'})

transitions = combine_transitions(
    transitionsInit,
    transitionsINT,
    transitionsFLOAT,
    transitionsVOID,
    transitionsRETURN,
    transitionsIF,
    transitionsELSE,
    transitionsLPAREN, 
    transitionsRPAREN,
    transitionsLBRACKETS,
    transitionsRBRACKETS,
    transitionsLBRACES,
    transitionsRBRACES,
    transitionsSEMICOLON,
    transitionsCOMMA,
    transitionsPLUS,
    transitionsMINUS,
    transitionsDIVIDE,
    transitionsTIMES,
    transitionsEQUALS,
    transitionsDIFFERENT,
    transitionsCOMMENT,
    transitionsNUMBER,
    transitionsID
    )

#print(transitions)

#
# TOKENS
#

tokens = ['INT',
          'FLOAT',
          'VOID',
          'RETURN',
          'IF',
          'ELSE',
          'LPAREN',
          'RPAREN',
          'LBRACKETS',
          'RBRACKETS',
          'LBRACES',
          'RBRACES',
          'SEMICOLON',
          'COMMA',
          'PLUS',
          'MINUS',
          'DIVIDE',
          'TIMES',
          'ATTRIBUTION',
          'EQUALS',
          'NUMBER',
          'ID'
          ]

#
# OUTPUTS
#

outputsInit = {
                'q0' : ''
                }

outputsINT = {
                'q_INT_1' : '',
                'q_INT_2' : '',
                'q_INT_3' : 'INT\n'
                }

outputsFLOAT = {
                'q_FLOAT_1' : '',
                'q_FLOAT_2' : '',
                'q_FLOAT_3' : '',
                'q_FLOAT_4' : '',
                'q_FLOAT_5' : 'FLOAT\n'
                }

outputsVOID = {
                'q_VOID_1' : '',
                'q_VOID_2' : '',
                'q_VOID_3' : '',
                'q_VOID_4' : 'VOID\n'
                }

outputsRETURN = {
                'q_RETURN_1' : '',
                'q_RETURN_2' : '',
                'q_RETURN_3' : '',
                'q_RETURN_4' : '',
                'q_RETURN_5' : '',
                'q_RETURN_6' : 'RETURN\n'
                }

outputsIF = {
                'q_IF_1' : 'IF\n'
                }

outputsELSE = {
                'q_ELSE_1' : '',
                'q_ELSE_2' : '',
                'q_ELSE_3' : '',
                'q_ELSE_4' : 'ELSE\n'
                }

outputsLPAREN = {
                'q_LPAREN' : 'LPAREN\n'
                }

outputsRPAREN = {
                'q_RPAREN' : 'RPAREN\n'
                }

outputsLBRACKETS = {
                'q_LBRACKETS' : 'LBRACKETS\n'
                }

outputsRBRACKETS = {
                'q_RBRACKETS' : 'RBRACKETS\n'
                }

outputsLBRACES = {
                'q_LBRACES' : 'LBRACES\n'
                }

outputsRBRACES = {
                'q_RBRACES' : 'RBRACES\n'
                }

outputsSEMICOLON = {
                'q_SEMICOLON' : 'SEMICOLON\n'
                }

outputsCOMMA = {
                'q_COMMA' : 'COMMA\n'
                }

outputsPLUS = {
                'q_PLUS' : 'PLUS\n'
                }

outputsMINUS = {
                'q_MINUS' : 'MINUS\n'
                }

outputsDIVIDE = {
                'q_DIVIDE' : 'DIVIDE\n'
                }

outputsTIMES = {
                'q_TIMES' : 'TIMES\n'
                }

outputsEQUALS = {
                'q_ATTRIBUTION_1' : '',
                'q_ATTRIBUTION_2' : 'ATTRIBUTION\n',
                'q_EQUALS_1' : 'EQUALS\n',
                'q_EQUALS_2' : ''
                }

outputsDIFFERENT = {
                'q_DIFFERENT_1' : '',
                'q_DIFFERENT_2' : 'DIFFERENT\n'
                }

outputsCOMMENT = {
                'q_COMMENT_1' : '',
                'q_COMMENT_2' : '',
                'q_COMMENT_3' : '',
                'q_DIVIDE_SPACE' : 'DIVIDE\n',
                'q_DIVIDE_LINEBREAK' : 'DIVIDE\n',
                'q_DIVIDE_LPAREN' : 'DIVIDE\nLPAREN\n',
                'q_DIVIDE_RPAREN' : 'DIVIDE\nRPAREN\n',
                'q_DIVIDE_LBRACKETS' : 'DIVIDE\nLBRACKETS\n',
                'q_DIVIDE_RBRACKETS' : 'DIVIDE\nRBRACKETS\n',
                'q_DIVIDE_LBRACES' : 'DIVIDE\nLBRACES\n',
                'q_DIVIDE_RBRACES' : 'DIVIDE\nRBRACES\n',
                'q_DIVIDE_SEMICOLON' : 'DIVIDE\nSEMICOLON\n',
                'q_DIVIDE_COMMA' : 'DIVIDE\nCOMMA\n',
                'q_DIVIDE_PLUS' : 'DIVIDE\nPLUS\n',
                'q_DIVIDE_MINUS' : 'DIVIDE\nMINUS\n',
                'q_DIVIDE_DIVIDE' : 'DIVIDE\nDIVIDE\n',
                'q_DIVIDE_TIMES' : 'DIVIDE\nTIMES\n',
                'q_DIVIDE_ID' : 'DIVIDE\nID\n'
                }

outputsNUMBER = {
                'q_NUMBER_1' : 'NUMBER\n',
                'q_NUMBER_2' : ''
                }

outputsID = {
                'q_ID_1' : 'ID\n',
                'q_ID_2' : '',
                'q_ID_SPACE' : 'ID\n',
                'q_ID_LINEBREAK' : 'ID\n',
                'q_ID_LPAREN' : 'ID\nLPAREN\n',
                'q_ID_RPAREN' : 'ID\nRPAREN\n',
                'q_ID_LBRACKETS' : 'ID\nLBRACKETS\n',
                'q_ID_RBRACKETS' : 'ID\nRBRACKETS\n',
                'q_ID_LBRACES' : 'ID\nLBRACES\n',
                'q_ID_RBRACES' : 'ID\nRBRACES\n',
                'q_ID_SEMICOLON' : 'ID\nSEMICOLON\n',
                'q_ID_COMMA' : 'ID\nCOMMA\n',
                'q_ID_PLUS' : 'ID\nPLUS\n',
                'q_ID_MINUS' : 'ID\nMINUS\n',
                'q_ID_DIVIDE' : 'ID\nDIVIDE\n',
                'q_ID_TIMES' : 'ID\nTIMES\n'
                }

outputs = outputsInit.copy()
outputs.update(outputsINT)
outputs.update(outputsFLOAT)
outputs.update(outputsVOID)
outputs.update(outputsRETURN)
outputs.update(outputsIF)
outputs.update(outputsELSE)
outputs.update(outputsLPAREN)
outputs.update(outputsLBRACKETS)
outputs.update(outputsRBRACKETS)
outputs.update(outputsRPAREN)
outputs.update(outputsLBRACES)
outputs.update(outputsRBRACES)
outputs.update(outputsSEMICOLON)
outputs.update(outputsCOMMA)
outputs.update(outputsPLUS)
outputs.update(outputsMINUS)
outputs.update(outputsDIVIDE)
outputs.update(outputsTIMES)
outputs.update(outputsEQUALS)
outputs.update(outputsDIFFERENT)
outputs.update(outputsCOMMENT)
outputs.update(outputsNUMBER)
outputs.update(outputsID)

#
# MOORE MACHINE
#

moore = Moore(states,
              fullList,
              tokens,
              transitions,
              'q0',
              outputs
              )

def moore_to_jflap(states, alphabet, tokens, transitions, initial_state, outputs, output_file):
    # Substitui '\n' por ' ' nos outputs sem modificar o dicionário original
    sanitized_outputs = {state: outputs.get(state, '').replace('\n', ' ') for state in states}

    # Cria a estrutura XML
    structure = ET.Element('structure')
    automaton_type = ET.SubElement(structure, 'type')
    automaton_type.text = 'moore'
    automaton = ET.SubElement(structure, 'automaton')

    # Mapeia os estados para IDs
    state_map = {state: str(i) for i, state in enumerate(states)}

    # Adiciona os estados ao XML
    for state in states:
        state_element = ET.SubElement(automaton, 'state', id=state_map[state], name=state)
        
        # Define posições X e Y fictícias
        x = ET.SubElement(state_element, 'x')
        y = ET.SubElement(state_element, 'y')
        x.text = str(100 + 150 * (int(state_map[state]) % 10))  # Posição X
        y.text = str(100 + 150 * (int(state_map[state]) // 10))  # Posição Y

        # Marca o estado inicial
        if state == initial_state:
            ET.SubElement(state_element, 'initial')

        # Adiciona o output do estado
        output = ET.SubElement(state_element, 'output')
        output.text = sanitized_outputs[state]  # Garante que nunca será None

    # Adiciona as transições ao XML
    for from_state, edges in transitions.items():
        if from_state not in state_map:
            print(f"Erro: Estado de origem '{from_state}' não encontrado em 'states'.")
            return  # Interrompe para evitar inconsistência no XML

        for symbol, to_state in edges.items():
            if to_state not in state_map:
                print(f"Erro: Estado de destino '{to_state}' não encontrado em 'states'.")
                return  # Interrompe para evitar inconsistência no XML

            transition = ET.SubElement(automaton, 'transition')
            from_element = ET.SubElement(transition, 'from')
            to_element = ET.SubElement(transition, 'to')
            read = ET.SubElement(transition, 'read')
            transout = ET.SubElement(transition, 'transout')

            from_element.text = state_map[from_state]
            to_element.text = state_map[to_state]
            read.text = symbol

            # Adiciona o output associado ao estado de destino
            transout.text = sanitized_outputs[to_state]

    # Escreve o XML no arquivo
    try:
        tree = ET.ElementTree(structure)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        #print(f"Arquivo '{output_file}' gerado com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar o arquivo XML: {e}")

def main():
    check_cm = False
    check_key = False

    if(len(sys.argv) < 2):
        raise TypeError(error_handler.newError(check_key, 'ERR-LEX-USE'))
    
    for idx, arg in enumerate(sys.argv):
        aux = arg.split('.')
        if aux[-1] == 'cm':
            check_cm = True
            idx_cm = idx

        if(arg == "-k"):
            check_key = True
    
    if check_key and len(sys.argv) < 3:
        raise TypeError(le.newError(checkKey, 'ERR-LEX-USE'))
    elif not check_cm:
      raise IOError(error_handler.newError(check_key, 'ERR-LEX-NOT-CM'))
    elif not os.path.exists(sys.argv[idx_cm]):
        raise IOError(error_handler.newError(check_key, 'ERR-LEX-FILE-NOT-EXISTS'))
    else:
        data = open(sys.argv[idx_cm])
        source_file = data.read()

        try:
            if not check_key:
                print("Definição da Máquina:")
                print(moore)
                print("Entrada:")
                print(source_file)
                print("Lista de Tokens:")
            
            print(moore.get_output_from_string(source_file).rstrip('\n'))

            moore_to_jflap(states, fullList, tokens, transitions, 'q0', outputs, 'jflap/moore_machine.jff')
        except Exception as e:
            error_msg = str(e)
    
            # Tentando encontrar o caractere que causou o erro na entrada
            for i, char in enumerate(source_file):
                try:
                    moore.get_output_from_string(source_file[:i+1])  # Tenta processar até o caractere atual
                except Exception:
                    # Encontramos a posição do erro
                    error_index = i
                    break
            else:
                error_index = None  # Caso não encontre
            
            if error_index is not None:
                # Encontrar a linha e coluna do erro
                line = source_file[:error_index].count('\n') + 1
                last_newline = source_file[:error_index].rfind('\n')
                column = (error_index - last_newline) if last_newline != -1 else error_index + 1
                raise IOError(error_handler.newError(check_key, 'ERR-LEX-INV-CHAR', line, column, valor=e))
            else:
                line, column = "Desconhecido", "Desconhecido"

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    except (ValueError, TypeError):
        print(e)