from collections import defaultdict

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
    print(rules)
    
    print(nonTerms)

