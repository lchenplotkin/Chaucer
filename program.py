import re
import string
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

ALLOW_VOWEL_SUBSTITUTION = True
vowels = "aeiouy"

# Standardize word endings for rhyme comparison in Middle English
def standardize_rhyme_form(word):
    word = word.lower()
    word = re.sub(r'(en|yn|in|on|un)$', 'en', word)
    word = re.sub(r'(ie|i|y)$', 'y', word)
    word = re.sub(r'(our|or|ur|er)$', 'ur', word)
    if ALLOW_VOWEL_SUBSTITUTION:
        word = re.sub(r'(ai|ay|ei|ey)$', 'ay', word)
        word = re.sub(r'([aeiou])w?r$', r'\1ur', word)
    return word

# Strip consonants and return only vowels from a word
def strip_to_vowels(text):
    return ''.join(char for char in text if char in vowels)

# Break word into syllables
def break_into_syllables(word):
    word = word.lower()
    for pair in ["ou", "ai", "ei", "au", "ea", "ie", "oo"]:
        word = word.replace(pair, pair + "_")
    for blend in ["sh", "ch", "st", "cl", "fl", "gl", "bl", "wh", "gh", "th", "ll"]:
        word = word.replace(blend, blend + "_")
    syllables = re.findall(r'[^aeiouy]*[aeiouy]+(?:[^aeiouy]*|$)', word)
    return [s.replace("_", "") for s in syllables]

# Check for common feminine rhyme endings
def ends_in_common_feminine(word1, word2):
    feminine_endings = ["ioun", "itye", "able", "ables", "elrye", "ible", "nesse", "ibles", "aunce", "oyed", "enesse", "nence", "obles"]
    return any(word1.endswith(ending) and word2.endswith(ending) for ending in feminine_endings)

# Determine rhyme type: Masculine or Feminine
def get_rhyme_type(word1, word2):
    form1, form2 = standardize_rhyme_form(word1), standardize_rhyme_form(word2)
    syllables1, syllables2 = break_into_syllables(word1), break_into_syllables(word2)

    if ends_in_common_feminine(word1, word2): return "F"
    if len(syllables1) == 1 or len(syllables2) == 1: return "M"

    last1, last2 = syllables1[-1], syllables2[-1]
    if last1 == last2:
        if last1 == 'e':
            syllables1.pop(-1)
            syllables2.pop(-1)
        if len(syllables1) >= 2 and len(syllables2) >= 2:
            penult1, penult2 = syllables1[-2], syllables2[-2]
            if strip_to_vowels(penult1) == strip_to_vowels(penult2): return "F"
        return "M"

    if strip_to_vowels(last1) == strip_to_vowels(last2):
        if len(syllables1) >= 2 and len(syllables2) >= 2:
            penult1, penult2 = syllables1[-2], syllables2[-2]
            if penult1 == penult2: return "F"
        return "M"
    return "E"

# Extract final words of each line, removing punctuation
def get_final_words(text):
    final_words = []
    for line in text.split('\n'):
        line = line.strip("-").strip()
        if line:
            final_word = line.split()[-1].strip(string.punctuation).strip("-")
            final_words.append(final_word)
    return final_words

# Identify regions of consecutive feminine rhymes above a threshold
def find_longest_feminine_regions(rhyme_types, threshold=0.5):
    longest_regions, current_start, current_fem_count, total_count = [], None, 0, 0
    for i, rhyme in enumerate(rhyme_types):
        if rhyme == 'F':
            if current_start is None: current_start = i
            current_fem_count += 1
        elif current_start is not None:
            total_count = i - current_start
            if current_fem_count / total_count >= threshold:
                longest_regions.append((current_start + 1, i))
            current_start, current_fem_count = None, 0
    if current_start is not None:
        total_count = len(rhyme_types) - current_start
        if current_fem_count / total_count >= threshold:
            longest_regions.append((current_start + 1, len(rhyme_types)))
    return sorted(longest_regions, key=lambda x: (x[1] - x[0]), reverse=True)[:3]

# Process a directory of text files and plot the results
def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            with open(os.path.join(directory_path, filename), "r") as file:
                text = file.read()

            final_words = get_final_words(text)
            if final_words:
                rhyme_types = [get_rhyme_type(final_words[i], final_words[i + 1]) for i in range(0, len(final_words) - 1, 2)]

                mascu_count, femi_count, error_count = rhyme_types.count('M'), rhyme_types.count('F'), rhyme_types.count('E')
                print(f"Statistics for {filename}:")
                print(f"Total Lines: {len(final_words)}")
                print(f"Feminine Rhymes: {femi_count}, ({(femi_count / len(final_words)) * 100:.2f}%)")
                print(f"Masculine Rhymes: {mascu_count}, ({(mascu_count / len(final_words)) * 100:.2f}%)")
                print(f"Errors: {error_count}, ({(error_count / len(final_words)) * 100:.2f}%)\n")

                csv_filename = f'csvs/{filename.replace(".txt", "_rhyme_report.csv")}'
                with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(['Line Start', 'Line End', 'Rhyme Type', 'Words'])
                    for i, rhyme in enumerate(rhyme_types):
                        writer.writerow([i * 2 + 1, (i * 2) + 2, rhyme, f'{final_words[i*2]} / {final_words[i*2+1]}'])

                x = np.arange(1, len(rhyme_types) * 2, 2)
                y = [1 if rhyme == 'F' else 0 for rhyme in rhyme_types]
                plt.figure(figsize=(10, 6))
                plt.scatter(x, y, color='red', label='Feminine Rhyme', s=1)
                plt.xlabel('Line Number')
                plt.ylabel('Rhyme Type (1 = Feminine, 0 = Masculine)')
                plt.title(f'Rhyme Analysis for {filename}')
                plt.savefig(f"plots/{filename.replace('.txt', '_rhyme_plot.png')}")
                plt.close()

# Process directory of text files
process_directory('./txt_tales')
