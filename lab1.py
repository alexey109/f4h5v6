import re
import time

start_time = time.time()

shift = "дюмях"
alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"  # [chr(i) for i in range(1072, 1072+32)]
dict = alphabet
reg_ex = re.compile('[^а-яА-Я ]')
text_shift = 500


# 1)
# создание словаря с заданным правилом
for chr in list(shift):
    dict = dict.replace(chr, '')
dict = shift + dict

# получаем текст и оставляем только символы из алфавита
file = open("v i mir.txt", "r", encoding="utf-8")
text_orig = re.sub('[^а-я ]', '', file.read().lower())
print("Пример оригинала      : ", text_orig[text_shift: text_shift+100])

# кодирование текста
text_encoded = ''.join([dict[alphabet.find(c)] if c != ' ' else ' ' for c in text_orig[:20000]])
print("Пример кодированного  : ", text_encoded[text_shift: text_shift+100])


# 2,3)
# подсчет частоты символов
amount_orig = {c: 0 for c in alphabet + ' '}
amount_encoded = {c: 0 for c in alphabet + ' '}
for c in text_orig:
    amount_orig[c] += 1
for c in text_encoded:
    amount_encoded[c] += 1
del amount_orig[' ']
del amount_encoded[' ']
amount_orig = {k: v for k, v in sorted(amount_orig.items(), key=lambda x:x[1], reverse=True)}
amount_encoded = {k: v for k, v in sorted(amount_encoded.items(), key=lambda x:x[1], reverse=True)}

# 4)
print('\nЧастота в оригнале (20)    :', ', '.join([f"{k}: {v}" for k,v in list(amount_orig.items())[:10]]))
print('Частота в кодированном (20):',  ', '.join([f"{k}: {v}" for k,v in list(amount_encoded.items())[:10]]))

# декодирование текста
orig_sort = ''.join(amount_orig.keys())
encoded_sort = ''.join(amount_encoded.keys())
text_decoded = ''.join([orig_sort[encoded_sort.find(c)] if c != ' ' else ' ' for c in text_encoded])
print("Пример декодированного: ", text_decoded[text_shift: text_shift+100])


# вывод текстов в фаил
fclear = open("orig.txt", "w+", encoding="utf-8")
fclear.write(text_orig)
fcode = open("encoded.txt", "w+", encoding="utf-8")
fcode.write(text_encoded)


# 5)
def count_birgrams(text):
    bigrams = {}
    text_no_space = text.replace(' ', '')
    for i in range(0, len(text_no_space), 2):
       bigram = text_no_space[i: i+2]
       try:
           bigrams[bigram] += 1
       except:
           bigrams[bigram] = 1
    return bigrams

# 6)
bigrams_orig = count_birgrams(text_orig)
print("Частота биграмм ориганла (10): ", ', '.join([f"{k}: {v}" for k, v in list(bigrams_orig.items())[:10]]))
bigrams_encoded = count_birgrams(text_encoded)
print("Частота биграмм кодиров. (10): ", ', '.join([f"{k}: {v}" for k, v in list(bigrams_encoded.items())[:10]]))

# 7)
bigrams_orig_sort = sorted(bigrams_orig.items(), key=lambda x:x[1])
print("Топ5 биграмм ориганла: ", ', '.join([f"{k}: {v}" for k, v in bigrams_orig_sort[-5:]]))
bigrams_encoded_sort =  sorted(bigrams_encoded.items(), key=lambda x:x[1])
print("Топ5 биграмм кодиров.: ", ', '.join([f"{k}: {v}" for k, v in bigrams_encoded_sort[-5:]]))


print("--- %s seconds ---" % (time.time() - start_time))