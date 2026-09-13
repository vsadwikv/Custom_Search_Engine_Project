import json

with open("dataCrawler.json", "r", encoding="utf-8") as file:
    data = json.load(file)

invertedIndex = {}

for documentId, document in enumerate(data):
    word_counts = document["word_counts"]

    for word in word_counts:
        if word in invertedIndex:
            invertedIndex[word].append(documentId)
        else:
            invertedIndex[word] = [documentId]

query = input("Enter the search query: ").lower()
queryTokens = query.split()

if not queryTokens:
    print("Please enter a search query.")
else:
    if queryTokens[0] in invertedIndex:
        matchingDocuments = set(invertedIndex[queryTokens[0]])

        for word in queryTokens[1:]:
            if word in invertedIndex:
                matchingDocuments = matchingDocuments & set(
                    invertedIndex[word])
            else:
                matchingDocuments = set()
                break
    else:
        matchingDocuments = set()

    if matchingDocuments:
        for documentId in matchingDocuments:
            document = data[documentId]

            print(document["title"])
            print(document["url"])
    else:
        print("No Results Found!")
