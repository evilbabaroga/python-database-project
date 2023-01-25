def replace_all(old, new, word):
    while word.find(old) != -1:
        word = word.replace(old, new)
    return word

def upper_first_letter(word):
    if len(word) == 0:
        return word
    if len(word) == 1:
        return word[0].upper()
    return word[0].upper() + word[1:]

def clean_company_name(name: str):
    """
    Clean the name of a company to a specified format.

    params: name: str - name of the company
    return: str - cleaned name
    """
    if name.find(",") != -1:
        name = name.replace(name[name.find(","):], "")
    while name.find("(") != -1:
        name = name.replace(name[name.find("("):name.find(")") + 1], " ")

    # name = replace_all("'", "", name)
    name = replace_all("\"", "", name)

    legal_entities = ["LIMITED", "LTD", "LTD.", "PARTNERSHIP", "HOLDINGS", "TRUST"]
    name = ' '.join(name.split()[:-2] + list(filter(lambda word: word.upper() not in legal_entities, name.split()[-2:])))

    # Strip clears trailing spaces if they exist
    name = name.capitalize().strip()
    # Cleans extra spaces inbetween words
    name = ' '.join(name.split())

    name = ' '.join(['-'.join(map(upper_first_letter, name.split(' ')[0].split('-')))] + replace_all("-", " ", " ".join(name.split(' ')[1:])).split())
    name = ' '.join((map(lambda x: ''.join(list(map(upper_first_letter, x[:-1])) + [upper_first_letter(x[-1]) if x[-1].upper() != 'S' else x[-1]]), list(map(lambda word: word.split("'"), name.split())))))
    name = ' '.join(map(upper_first_letter, name.split()))
    name = '.'.join(map(upper_first_letter, name.split('.')))
    name = ' '.join(map(lambda word: word.upper() if word.find("&") != -1 else word, name.split()))

    return name
