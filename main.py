from fuzz import read, Grammar

def main():
    grammar = Grammar()
    grammar.readGrammar('S')
    grammar.HNFTransform()
    grammar.printGrammar()
    read(grammar.rules)

if __name__ == "__main__":
    main()