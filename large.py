

large = open('large.txt', 'w')

with open('words.txt') as words:
    for w in words:
        w2 = w.strip().lower()
        len_w2 = len(w2)
        if len_w2 > 6:
            print(w2, file=large)

large.close() 
