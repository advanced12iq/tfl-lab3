from fuzz import Grammar

def main():
    grammar = Grammar()
    grammar.readGrammar(startingNT='S')
    grammar.prepareForGeneration()
    grammar.generate()

if __name__ == "__main__":
    main()