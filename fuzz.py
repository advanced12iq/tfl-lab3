from collections import defaultdict, deque
import string
import sys
sys.setrecursionlimit(10000)

def get_brackets(l):
    newList = []
    for s in l:
        i = 0
        while i < len(s):
            if s[i] == '[':
                first = i
                while s[i] != ']':
                    i += 1
                newList.append(s[first:i+1])
            else:
                newList.append(s[i])
            i += 1
    
    return newList


def read(lines):
    rules = []
    nonTerms = defaultdict(list)
    for rule in lines:
        rules.append(list(map(lambda r: r.strip().split(), rule.strip().split('- >'))))
    for rule in rules:
        nonTerms[rule[0][0]] += [get_brackets(rule[1])]
    

    def delete_long_rules(root):
        counter = 1
        for i in range(len(nonTerms[root])):
            rule = nonTerms[root][i]
            if len(rule) > 2:
                new_node = root + str(counter)
                nonTerms[new_node] = [rule[1:]]
                new_rules = [rule[0], new_node]
                nonTerms[root][i] = [new_rules]
                delete_long_rules(new_node)
                counter += 1
                
    for nonTerm in list(nonTerms.keys()):
        delete_long_rules(nonTerm)

    isEpsilon = defaultdict(bool)
    concernedRules = defaultdict(list)
    counter = defaultdict(int)
    Q = deque()

    grammar = [(s, l) for s in nonTerms.keys() for l in nonTerms[s]]

    print(grammar)
    

    print(nonTerms)
    
    
    # def find_generative_element(node):
    #     visited.add(node)
    #     for verticies in nonTerms[node]:
    #         for vertex in verticies:
    #             if vertex[0].islower():
    #                 continue
    #             if vertex not in visited:
    #                 find_generative_element(vertex)


    # max_element = (0, 0)

    # for key in nonTerms.keys():
    #     visited = set([])
    #     find_generative_element(key)
    #     if len(visited) > max_element[0]:
    #         max_element=(len(visited), key)        
    
    # generative_element = max_element[1]
