import re
import pandas as pd
import json
import itertools

def augmentation_negation(list_negation, re_fetch, line):
    lista = []

    if re.search(re_fetch, line[0]) != None and re.search(re_fetch, line[1]) != None:
        possibilities_negation = re.findall(re_fetch, line[0])
        number_of_words = len(possibilities_negation)
        if number_of_words == 1:
            lista.append(line)
            lista.append((re.sub(re_fetch, r'NÃO_\1', line[0]), re.sub(re_fetch, r'NÃO_\1', line[1])))
        else:
            words = []
            for index, word in enumerate(possibilities_negation):
                if index == number_of_words:
                    break
                words.append(r'\b' + word[0] + r'\b')
                possibilities_negation[index] = [word[0]]
                possibilities_negation[index].append('NÃO_' + word[0])

            permutations = itertools.product(*possibilities_negation)
            indexes_of_word = itertools.cycle([0, 1])
            for word in permutations:
                sentence_gr = line[0]
                sentence_gi = line[1]
                for i in range(number_of_words):
                    sentence_gr = re.sub(words[i], word[i], sentence_gr)
                    sentence_gi = re.sub(words[i], word[i], sentence_gi)
                    
                lista.append((sentence_gr, sentence_gi))
                
    if lista != []:
        return lista
    else:
        return line

df_negation = pd.read_csv('negacao.csv', header=None)

list_negation = df_negation.values.tolist()

fetching_expression = "("

for neg in list_negation:
    word = neg[0].split('_')[1]
    fetching_expression += r"(\b" + word.upper() + r"\b)|"

fetching_expression = fetching_expression[:-1]
fetching_expression += ")"
re_fetch = r"" + fetching_expression

teste_frases = [('WEINTRAUB CONVIDAR JAIR BOLSONARO IR CASA', 'WEINTRAUB&FAMOSO CONVIDAR JAIR_BOLSONARO&FAMOSO IR CASA'), ('WEINTRAUB SAIR', 'WEINTRAUB&FAMOSO SAIR'),
                ('JOHN LENNON IR CASA', 'JOHN_LENNON&FAMOSO IR CASA'), ('HARRY POTTER CONVERSAR HITLER', 'HARRY_POTTER&FAMOSO CONVERSAR HITLER&FAMOSO'),
                ('OPA', 'OPA'), ('EU NOTAR ALI NEGAR BOM', 'EU NOTAR ALI NEGAR BOM')]
                

for i in teste_frases:
    print(augmentation_negation(list_negation, re_fetch, i), '\n')

