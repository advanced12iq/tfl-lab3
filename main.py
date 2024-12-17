from fuzz import Grammar

def main():
    grammar = Grammar()
    grammar.readGrammar()
    grammar.prepareForGeneration()
    grammar.generate()

if __name__ == "__main__":
    main()