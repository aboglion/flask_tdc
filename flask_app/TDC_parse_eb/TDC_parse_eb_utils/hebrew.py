def fix_if_reversed(sentence):
    sentence=sentence.strip()
    reversed=False
    hebrew_letters = "'אבגדהוזחטיכלמנסעפצקרשתןךםףץ"
    non_final_letters = ['מ', 'נ', 'צ', 'פ', 'כ']
    final_letters = ['"',"'",'ם', 'ן', 'ץ', 'ף', 'ך']
    words = sentence.split()
    for word in words:
        # בדיקה אם המילה מסתיימת באות לא סופית
        if any(word.endswith(letter) for letter in non_final_letters):
            reversed= True
        if not reversed:
        # בדוק אם המילה מתחילה באות סופית
            if any((letter in word[:-1]) for letter in final_letters):
                reversed= True
    if reversed:
            reversed_sentence = ""
            for word in words:
                if word[0] in hebrew_letters:reversed_sentence=word[::-1]+" "+reversed_sentence
                else:reversed_sentence =word+" "+reversed_sentence
            return reversed_sentence
    return sentence 
