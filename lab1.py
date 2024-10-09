import pandas as pd
import math

# Символи з пробілом і без
chars_with_space = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
chars_without_space = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

# Читання та обробка тексту
input_text = open('lab1.txt', encoding='utf-8').read().replace('n', '').replace('\n', ' ').lower()

# Фільтрація тексту (без пробілів)
filtered_text = ''.join(symbol for symbol in input_text if symbol in chars_without_space and symbol.isalpha())

# Фільтрація тексту (з пробілами)
filtered_text_with_space = ''.join(symbol for symbol in input_text if symbol in chars_with_space and symbol.isalpha() or symbol.isspace())

# Функція для підрахунку кількості та частоти символів
def calculate_char_count_and_freq(txt: str, charset: str):
    count_dict = {}
    for char in txt:
        count_dict[char] = count_dict.get(char, 0) + 1
    
    freq_dict = {}
    for char in count_dict:
        freq_dict[char] = round(count_dict[char] / len(txt), 5)
    
    return count_dict, freq_dict

# Підрахунок для тексту без пробілів
count_no_space, freq_no_space = calculate_char_count_and_freq(filtered_text, chars_without_space)
df_char_freq_no_space = pd.DataFrame({
    'Char': freq_no_space.keys(),
    'Count': [count_no_space[c] for c in freq_no_space.keys()],
    'Freq': freq_no_space.values()
}).sort_values(by='Freq', ascending=False)

print(df_char_freq_no_space)
df_char_freq_no_space.to_excel("CharFreq_no_space.xlsx")

# Підрахунок для тексту з пробілами
count_with_space, freq_with_space = calculate_char_count_and_freq(filtered_text_with_space, chars_with_space)
df_char_freq_with_space = pd.DataFrame({
    'Char': freq_with_space.keys(),
    'Count': [count_with_space[c] for c in freq_with_space.keys()],
    'Freq': freq_with_space.values()
}).sort_values(by='Freq', ascending=False)

print(df_char_freq_with_space)
df_char_freq_with_space.to_excel("CharFreq_with_space.xlsx")

# Функція для підрахунку біграм
def calculate_bigram_count_and_freq(txt: str, charset: str, overlap: bool):
    bigram_count = {}
    bigram_freq = {}

    step = 1 if overlap else 2
    for i in range(0, len(txt) - 1, step):
        bigram = txt[i] + txt[i + 1]
        bigram_count[bigram] = bigram_count.get(bigram, 0) + 1

    total_bigrams = len(txt) - 1 if overlap else len(txt) // 2
    for bigram in bigram_count:
        bigram_freq[bigram] = round(bigram_count[bigram] / total_bigrams, 5)

    return bigram_count, bigram_freq

# Функція для створення таблиці біграм
def create_bigram_df(charset: str, bigram_freq: dict, save_as_excel: bool = False, filename: str = 'bigram'):
    sorted_charset = sorted(charset)
    bigram_df = pd.DataFrame(index=sorted_charset, columns=sorted_charset)

    for bg in bigram_freq:
        x = sorted_charset.index(bg[0])
        y = sorted_charset.index(bg[1])
        bigram_df.iloc[x, y] = bigram_freq[bg]

    if " " in bigram_df.index:
        bigram_df = bigram_df.rename(index={" ": "space"}, columns={" ": "space"})

    if save_as_excel:
        bigram_df.to_excel(f"{filename}.xlsx")

    return bigram_df

# Пересічні біграми без пробілів
bigram_count_overlap, bigram_freq_overlap = calculate_bigram_count_and_freq(filtered_text, chars_without_space, True)
bigram_df_overlap = create_bigram_df(chars_without_space, bigram_freq_overlap, True, 'overlap_bigram')
print(bigram_df_overlap)

# Пересічні біграми з пробілами
bigram_count_overlap_space, bigram_freq_overlap_space = calculate_bigram_count_and_freq(filtered_text_with_space, chars_with_space, True)
bigram_df_overlap_space = create_bigram_df(chars_with_space, bigram_freq_overlap_space, True, 'overlap_bigram_with_space')
print(bigram_df_overlap_space)

# Непересічні біграми без пробілів
bigram_count_nonoverlap, bigram_freq_nonoverlap = calculate_bigram_count_and_freq(filtered_text, chars_without_space, False)
bigram_df_nonoverlap = create_bigram_df(chars_without_space, bigram_freq_nonoverlap, True, 'nonoverlap_bigram')
print(bigram_df_nonoverlap)

# Непересічні біграми з пробілами
bigram_count_nonoverlap_space, bigram_freq_nonoverlap_space = calculate_bigram_count_and_freq(filtered_text_with_space, chars_with_space, False)
bigram_df_nonoverlap_space = create_bigram_df(chars_with_space, bigram_freq_nonoverlap_space, True, 'nonoverlap_bigram_with_space')
print(bigram_df_nonoverlap_space)

# Функція для обчислення ентропії H1 (монограми)
def compute_h1_entropy(freq_dict):
    return -sum(freq * math.log2(freq) for freq in freq_dict.values())

# Обчислення H1
h1_no_space = compute_h1_entropy(freq_no_space)
h1_with_space = compute_h1_entropy(freq_with_space)
print(f"Ентропія H1 для тексту без пробілів: {h1_no_space}")
print(f"Ентропія H1 для тексту з пробілами: {h1_with_space}")

# Функція для обчислення ентропії H2 (біграми)
def compute_h2_entropy(bigram_freq):
    return -sum(freq * math.log2(freq) for freq in bigram_freq.values() if freq > 0) / 2


# Обчислення H2
h2_overlap = compute_h2_entropy(bigram_freq_overlap)
h2_overlap_space = compute_h2_entropy(bigram_freq_overlap_space)

h2_nonoverlap = compute_h2_entropy(bigram_freq_nonoverlap)
h2_nonoverlap_space = compute_h2_entropy(bigram_freq_nonoverlap_space)

print(f"Ентропія H2 для пересічних біграм (без пробілів): {h2_overlap}")
print(f"Ентропія H2 для пересічних біграм (з пробілами): {h2_overlap_space}")
print(f"Ентропія H2 для непересічних біграм (без пробілів): {h2_nonoverlap}")
print(f"Ентропія H2 для непересічних біграм (з пробілами): {h2_nonoverlap_space}")

# Функція для обчислення надлишковості
def compute_redundancy(h, charset):
    h0 = math.log2(len(charset))
    return 1 - (h / h0)

# Обчислення надлишковості
redundancy_h1 = compute_redundancy(h1_no_space, chars_without_space)
redundancy_h1_space = compute_redundancy(h1_with_space, chars_with_space)

redundancy_h2_overlap = compute_redundancy(h2_overlap, chars_without_space)
redundancy_h2_overlap_space = compute_redundancy(h2_overlap_space, chars_with_space)

redundancy_h2_nonoverlap = compute_redundancy(h2_nonoverlap, chars_without_space)
redundancy_h2_nonoverlap_space = compute_redundancy(h2_nonoverlap_space, chars_with_space)

print(f"Надлишковість H1 (без пробілів): {redundancy_h1}")
print(f"Надлишковість H1 (з пробілами): {redundancy_h1_space}")
print(f"Надлишковість H2 пересічні (без пробілів): {redundancy_h2_overlap}")
print(f"Надлишковість H2 пересічні (з пробілами): {redundancy_h2_overlap_space}")
print(f"Надлишковість H2 непересічні (без пробілів): {redundancy_h2_nonoverlap}")
print(f"Надлишковість H2 непересічні (з пробілами): {redundancy_h2_nonoverlap_space}")
