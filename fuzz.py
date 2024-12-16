from collections import defaultdict, deque
import sys
import random
sys.setrecursionlimit(10000)


def isNT(symbol : str) -> bool:
    return not symbol[0].islower()


def getSetOFNTs(rule : list) -> set:
    return set([symbol for symbol in rule if isNT(symbol)])

class Grammar():

    def __init__(self):
        self.NT_To_Rules = defaultdict(list)
        self.rules = []
        self.allNTs = set([])
        self.terminals = set([])
        self.startingNT = None
        self.counter = 1


    def readGrammar(self, startingNT : str):
        lines = sys.stdin.readlines()

        for line in lines:
            line_splited = list(map(lambda r: r.replace(' ', ''), line.strip().split('->')))
            NT = line_splited[0]
            rightRule = list(map(lambda l : l.strip(), line_splited[1].split('|')))
            self.NT_To_Rules[NT] += list(map(self.parseRule, rightRule))

        self.updateGrammar()

        self.startingNT = startingNT


    def updateGrammar(self):
        self.rules = []
        for NT, rightRules in self.NT_To_Rules.items():
            for rightRule in rightRules:
                self.rules.append((NT, rightRule))
        self.allNTs = set(self.NT_To_Rules.keys())

        self.terminals = set([])
        for _, rightRule in self.rules:
            self.terminals = self.terminals.union(set([symbol for symbol in rightRule if not isNT(symbol)]))


    def parseRule(self, s : str) -> list:
        newList = []
        i = 0
        while i < len(s):
            if s[i] == '[':
                start = i
                while s[i] != ']':
                    i += 1
                newList.append(s[start:i+1])
            else:
                if i < len(s) - 1 and s[i+1].isnumeric():
                    newList.append(s[i:i+2])
                    i += 1
                else:
                    newList.append(s[i])
            i += 1
        
        return newList
    

    def HNFTransform(self):
        self.deleteLongRules()
        self.deleteChainRules()
        self.deleteNonGenerative()
        self.deleteNonReacheble()
        self.deleteAloneTerminals()


    def deleteLongRules(self):
        for NT in self.allNTs:
            self.deleteLongRulesRecursion(NT)
        self.updateGrammar()
    

    def deleteLongRulesRecursion(self, NT : str):
        for i, rightRule in enumerate(self.NT_To_Rules[NT]):
            if len(rightRule) > 2:
                newNT = f"[new_NT_{NT + str(self.counter)}]"
                self.counter += 1
                self.NT_To_Rules[newNT] = [rightRule[1:]]
                newRightRule = [rightRule[0], newNT]
                self.NT_To_Rules[NT][i] = newRightRule
                self.deleteLongRulesRecursion(newNT)


    def deleteChainRules(self):
        visited = set([])
        self.deleteChainRulesRecursion(self.startingNT, visited)
        self.updateGrammar()


    def deleteChainRulesRecursion(self, NT_root : str, visited : set):
        visited.add(NT_root)
        for rightRule in self.NT_To_Rules[NT_root]:
            for NT in getSetOFNTs(rightRule):
                if NT not in visited:
                    self.deleteChainRulesRecursion(NT, visited)
        newRules = []
        for rightRule in self.NT_To_Rules[NT_root]:
            if len(rightRule) == 1 and isNT(rightRule[0]):
                newRules += self.NT_To_Rules[rightRule[0]]
            else:
                newRules.append(rightRule)
        self.NT_To_Rules[NT_root] = newRules.copy()


    def deleteNonGenerative(self):
        isGenerating = defaultdict(bool)
        counter = defaultdict(int)
        concernedRule = defaultdict(list)
        Q = deque()
        allNTs = set([])
        for i, (NT1, rightRule) in enumerate(self.rules):
            count = getSetOFNTs(rightRule)
            allNTs = allNTs.union(count, set([NT1]))
            for NT2 in count:
                concernedRule[NT2] += [i]
            counter[i] += len(count)
            if len(count) == 0:
                isGenerating[NT1] = True
                Q.append(NT1)
        for NT in allNTs:
            if not isGenerating[NT]:
                isGenerating[NT] = False

        visited = set([NT for NT in Q])
        while Q:
            for i in range(len(Q)):
                element = Q.popleft()
                for rule in concernedRule[element]:
                    counter[rule] -= 1
                    if counter[rule] == 0:
                        isGenerating[self.rules[rule][0]] = True
                        if self.rules[rule][0] in visited:
                            continue
                        Q.append(self.rules[rule][0])
                        visited.add(self.rules[rule][0])
        newRules = set([])
        for NT, val in isGenerating.items():
            if not val:
                newRules = set.union(newRules, set(set(concernedRule[NT])))
        self.rules = [rule for i, rule in enumerate(self.rules) if i not in newRules]
        self.NT_To_Rules = defaultdict(list)
        for NT, rightRule in self.rules:
            self.NT_To_Rules[NT] += [rightRule]
        self.updateGrammar()


    def deleteNonReacheble(self):
        rule2rule = defaultdict(list)
        NT_To_RuleNumber = defaultdict(list)
        RuleNumber_To_NTs = defaultdict(set)
        for i, (NT, rightRule) in enumerate(self.rules):
            NT_To_RuleNumber[NT] += [i]
            RuleNumber_To_NTs[i] = getSetOFNTs(rightRule)
        for RuleNumber, NTs in RuleNumber_To_NTs.items():
            for NT in NTs:
                if NT_To_RuleNumber[NT]:
                    rule2rule[RuleNumber] += NT_To_RuleNumber[NT]
        
        visited = set([])
        for ruleNumber, (NT, _) in enumerate(self.rules):
            if NT == self.startingNT:
                self.deleteNonReachebleRecursion(ruleNumber, visited, rule2rule)

        self.rules = [rule for i, rule in enumerate(self.rules) if i in visited]
        self.NT_To_Rules = defaultdict(list)
        for NT, rightRule in self.rules:
            self.NT_To_Rules[NT] += [rightRule]
        self.updateGrammar()


    def deleteNonReachebleRecursion(self, ruleNumber : int, visited : set, rule2rule : defaultdict):
        visited.add(ruleNumber)
        for next in rule2rule[ruleNumber]:
            if next not in visited:
                self.deleteNonReachebleRecursion(next, visited, rule2rule)


    def deleteAloneTerminals(self):
        newRules= {}
        for i, (NT, rightRule) in enumerate(self.rules):
            count = getSetOFNTs(rightRule)
            if len(rightRule) == 2 and len(count) < 2:
                if not isNT(rightRule[0]):
                    if rightRule[0] not in newRules:
                        newRules[rightRule[0]] = f'[NT_{NT}_To_{rightRule[0]}]'
                    self.rules[i][1][0] = newRules[rightRule[0]]
                if not isNT(rightRule[1]):
                    if rightRule[1] not in newRules:
                        newRules[rightRule[1]] = f'[NT_{NT}_To_{rightRule[1]}]'
                    self.rules[i][1][1] = newRules[rightRule[1]]
        for key, val in newRules.items():
            self.rules.append((val, [key]))
        
        self.NT_To_Rules = defaultdict(list)
        for NT, rightRule in self.rules:
            self.NT_To_Rules[NT] += [rightRule]
        self.updateGrammar()

    def printGrammar(self):
        for NT, rightRule in self.rules:
            print(NT, '- >', "".join(rightRule))


def read(grammar):
    
    visited = set([])
    first = defaultdict(set)
    adj = defaultdict(list)
    for nonTerm, rule in grammar:
        adj[nonTerm].append(rule)
    # Создание множеств Last first ...
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
    # Матрицу биграмм делаю
    followNT = defaultdict(set)
    for _, rule in grammar:
        if len(rule) == 2:
            followNT[rule[0]].add(rule[1])
    
    bigramms = defaultdict(set)
    for key, gammas in last.items():
        for y1 in gammas:
            for y2 in follow[key]:
                bigramms[y1].add(y2)

    for key, gammas in preceding.items():
        for y1 in gammas:
            for y2 in first[key]:
                bigramms[y1].add(y2)

    for key, val in followNT.items():
        for A2 in val:
            for y1 in last[key]:
                for y2 in first[A2]:
                    bigramms[y1].add(y2)

    
    adj = defaultdict(list)
    ed = defaultdict(list)
    nTs = set([])
    for nT, rule in grammar:
        if len(rule) != 2:
            ed[nT].append(rule[0][0])
        else:
            adj[nT].append(rule)
        nTs.add(nT)          
    def cyk(grammar, ed, word):
        d= {nT : [[False for _ in range(len(word))] for _ in range(len(word))] for nT in nTs}
        for i in range(len(word)):
            for nT, rules in ed.items():
                for rule in rules:
                    if word[i] == rule:
                        d[nT][i][i]= True
        for m in range(1, len(word)):
            for i in range(len(word) - m):
                j = i + m
                for nT, rules in grammar.items():
                    answer = False
                    for rule in rules:
                        for k in range(i, j):
                            answer = answer or (d[rule[0]][i][k] and d[rule[1]][k+1][j])
                    d[nT][i][j] = answer
        return d['S'][0][len(word)-1]

    # Генерация 
    terminals = list(set([rule[0] for _, rule in grammar if len(rule) == 1]))
    terminals = ['a', 'b', 'c', 'd']
    starting_symbols = list(first['S'])
    res = []
    with open('tests_verify.txt', 'w') as tf:
        with open('tests.txt', 'w') as f:
            for i in range(100):
                cur = random.choice(starting_symbols)
                while bigramms[cur[-1]]:
                    r = random.random()
                    if r < 0.1:
                        cur += random.choice(terminals)
                    elif r < 0.25:
                        break
                    else:
                        cur += random.choice(list(bigramms[cur[-1]]))
                f.write(cur)
                f.write(" 1\n" if cyk(adj, ed, cur) else " 0\n")
                tf.write(cur + '\n')
                if cyk(adj, ed, cur):
                    res.append(i+1)
    print(res)

    

