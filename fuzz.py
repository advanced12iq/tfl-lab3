from collections import defaultdict, deque
import sys
sys.setrecursionlimit(10000)

def get_brackets(s):
    newList = []
    i = 0
    while i < len(s):
        if s[i] == '[':
            start = i
            while s[i] != ']':
                i += 1
            newList.append(s[start:i+1])
        else:
            if i < len(s) - 1 and s[i].isnumeric():
                newList.append(s[i:i+2])
            else:
                newList.append(s[i])
        i += 1
    
    return newList


def read(lines):
    rules = []
    nonTerms = defaultdict(list)
    for rule in lines:
        rules.append(list(map(lambda r: r.replace(' ', ''), rule.strip().split('- >'))))
    for rule in rules:
        nonTerms[rule[0]] += [get_brackets(rule[1])]
    

    def delete_long_rules(root):
        counter = 1
        for i in range(len(nonTerms[root])):
            rule = nonTerms[root][i]
            if len(rule) > 2:
                new_node = root + str(counter)
                nonTerms[new_node] = [rule[1:]]
                new_rules = [rule[0], new_node]
                nonTerms[root][i] = new_rules
                delete_long_rules(new_node)
                counter += 1
                
    for nonTerm in list(nonTerms.keys()):
        delete_long_rules(nonTerm)

    grammar = [(s, l) for s in nonTerms.keys() for l in nonTerms[s]]

    # delete chain rules

    pairs = []
    for nonTerm in list(nonTerms.keys()):
        pairs.append((nonTerm, nonTerm))
    

    new_rules = []
    for nonTerm, rule in grammar:
        if len(rule) == 1 and not rule[0][0].islower():
            for i in range(len(pairs)):
                if pairs[i][1] == nonTerm:
                    pairs.append((pairs[i][0], nonTerm))
        else:
            new_rules.append((nonTerm, rule))
    
    for pair in pairs:
        if pair[0] == pair[1]:
            continue
        new_rules += [(pair[0], rule) for rule in new_rules if rule[0] == pair[0]]

    grammar = new_rules
    isGenerating = defaultdict(bool)
    counter = defaultdict(int)
    concernedRule = defaultdict(list)
    Q = deque()
    allnonTerms = set([])
    for i, (nonTerm, rule) in enumerate(grammar):
        count = set([nT for nT in rule if not nT[0].islower()])
        allnonTerms = allnonTerms.union(count, set([nonTerm]))
        for nT in count:
            concernedRule[nT] += [i]
        counter[i] += len(count)
        if len(count) == 0:
            isGenerating[nonTerm] = True
            Q.append(nonTerm)
    for nT in allnonTerms:
        if not isGenerating[nT]:
            isGenerating[nT] = False

    visited = set([el for el in Q])
    while Q:
        for i in range(len(Q)):
            element = Q.popleft()
            for rule in concernedRule[element]:
                counter[rule] -= 1
                if counter[rule] == 0:
                    isGenerating[grammar[rule][0]] = True
                    if grammar[rule][0] in visited:
                        continue
                    Q.append(grammar[rule][0])
                    visited.add(grammar[rule][0])
    new_rules = set([])
    for key, val in isGenerating.items():
        if not val:
            new_rules = set.union(new_rules, set(set(concernedRule[key])))

    grammar = [rule for i, rule in enumerate(grammar) if i not in new_rules]


    adj = defaultdict(list)
    leads_to = defaultdict(set)
    rule2rule = defaultdict(list)
    for i, (nonTerm, rule) in enumerate(grammar):
        adj[nonTerm] += [i]
        leads_to[i] = set([nT for nT in rule if not nT[0].islower()])
    for key, value in leads_to.items():
        for nT in value:
            if adj[nT]: rule2rule[key] += adj[nT]
    visited = set([])
    def dfs(root):
        visited.add(root)
        for next in rule2rule[root]:
            if next not in visited:
                dfs(next)
    for i, (nonTerm, _) in enumerate(grammar):
        if nonTerm == 'S':
            dfs(i)
    grammar = [rule for i, rule in enumerate(grammar) if i in visited]

    new_rules= {}
    for i, (nonTerm, rule) in enumerate(grammar):
        count = set([nT for nT in rule if not nT[0].islower()])
        if len(rule) - len(count) > 0:
            if rule[0][0].islower():
                if rule[0] not in new_rules:
                    new_rules[rule[0]] = f'[NT{nonTerm}To{rule[0]}]'
                grammar[i][1][0] = new_rules[rule[0]]
            if rule[1][0].islower():
                if rule[1] not in new_rules:
                    new_rules[rule[1]] = f'[NT{nonTerm}To{rule[1]}]'
                grammar[i][1][1] = new_rules[rule[1]]
    for key, val in new_rules.items():
        grammar.append((val, [key]))
    
    def print_grammar():
        for nonTerm, rule in grammar:
            print(nonTerm, '- >', "".join(rule))

    visited = set([])
    first = defaultdict(set)
    adj = defaultdict(list)
    for nonTerm, rule in grammar:
        adj[nonTerm].append(rule)
    
    def dfs(nonTerm, first, f=0):
        visited.add(nonTerm)
        for rule in adj[nonTerm]:
            if rule[f][0].islower():
                first[nonTerm].add(rule[f][0])
            else:
                if rule[f] not in visited:
                    dfs(rule[f], first, f)
                first[nonTerm] = first[nonTerm].union(first[rule[f]])

    for nonTerm, rule in grammar:
        if nonTerm not in visited:
            dfs(nonTerm, first)
    visited = set([])
    last = defaultdict(set)
    for nonTerm, rule in grammar:
        if nonTerm not in visited:
            dfs(nonTerm, last, -1)

    follow = defaultdict(set)
    changed= True
    while changed:
        changed=False
        for (nonTerm, rule) in grammar:
            if len(rule) > 1:
                if follow[rule[0]].union(first[rule[1]]) != follow[rule[0]]:
                    changed=True
                follow[rule[0]] = follow[rule[0]].union(first[rule[1]])
    preceding = defaultdict(set)
    changed=True
    while changed:
        changed=False
        for (nonTerm, rule) in grammar:
            if len(rule) > 1:
                if preceding[rule[1]].union(last[rule[0]]) != preceding[rule[1]]:
                    changed=True
                preceding[rule[1]] = preceding[rule[1]].union(last[rule[0]])
    print(first)
    print(last)
    print(follow)
    print(preceding)
    print_grammar()