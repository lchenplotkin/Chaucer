import re
import string
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

# Toggle for vowel substitution normalization
ALLOW_VOWEL_SUBSTITUTION = True

# Set of vowels used in syllabification
vowels = "aeiouy"

# Function to standardize word endings for rhyme comparison in Middle English
def standardize_rhyme_form(word, allow_vowel_substitution=True):
    word = word.lower()

    # Common Middle English rhyme normalization
    word = re.sub(r'(en|yn|in|on|un)$', 'en', word)
    word = re.sub(r'(ie|i|y)$', 'y', word)
    word = re.sub(r'(our|or|ur|er)$', 'ur', word)

    #word = re.sub(r'(enence|inence)$', 'enence', word)

    if allow_vowel_substitution:
        word = re.sub(r'(ai|ay|ei|ey)$', 'ay', word)
        word = re.sub(r'([aeiou])w?r$', r'\1ur', word)
    
    return word

# Function to strip consonants and return only vowels from a word
def strip_to_vowels(text):
    return ''.join([char for char in text if char in vowels])

# Function to break a word into syllables
def break_into_syllables(word):
    word = word.lower()

    # Treat common vowel combinations as units
    word = word.replace("ou", "ou_").replace("ai", "ai_").replace("ei", "ei_")
    word = word.replace("au", "au_").replace("ea", "ea_").replace("ie", "ie_")
    word = word.replace("oo", "oo_")

    # Treat common consonant blends as units
    for blend in ["sh", "ch", "st", "cl", "fl", "gl", "bl", "wh", "gh", "th", "ll"]:
        word = word.replace(blend, blend + "_")

    # Find syllables using vowel clusters
    syllables = re.findall(r'[^aeiouy]*[aeiouy]+(?:[^aeiouy]*|$)', word)

    # Restore replaced placeholders
    syllables = [s.replace("_", "") for s in syllables]


    return syllables

# List of common Middle English feminine rhyme endings

feminine_endings = [
    "ioun", "itye","able",'ables','elrye', "ible", "nesse", "ibles","aunce", "oyed","enesse", "nence","obles"
]


# Function to check if two words end with a common feminine ending
def ends_in_common_feminine(word1, word2):
    for ending in feminine_endings:
        if word1.endswith(ending) and word2.endswith(ending):
            return True
    return False

# Function to determine rhyme type: Masculine or Feminine
def get_rhyme_type(word1, word2):
    form1 = standardize_rhyme_form(word1, allow_vowel_substitution=ALLOW_VOWEL_SUBSTITUTION)
    form2 = standardize_rhyme_form(word2, allow_vowel_substitution=ALLOW_VOWEL_SUBSTITUTION)

    syllables1 = break_into_syllables(word1)
    syllables2 = break_into_syllables(word2)

    # Early exit if the words match a known feminine ending
    if ends_in_common_feminine(word1.lower(), word2.lower()):
        return "F"

    # Masculine if one of the words is monosyllabic
    if len(syllables1) == 1 or len(syllables2) == 1:
        return "M"

    last1 = syllables1[-1]
    last2 = syllables2[-1]

    # If the full last syllables match, check for feminine rhyme
    if last1 == last2:
        if last1 == 'e':
            syllables1.pop(-1)
            syllables2.pop(-1)
        if len(syllables1) >= 2 and len(syllables2) >= 2:
            penult1 = syllables1[-2]
            penult2 = syllables2[-2]
            if strip_to_vowels(penult1) == strip_to_vowels(penult2):
                return "F"
        return "M"

    # If last syllables differ, try matching just vowels
    elif strip_to_vowels(last1) == strip_to_vowels(last2):
        if len(syllables1) >= 2 and len(syllables2) >= 2:
            penult1 = syllables1[-2]
            penult2 = syllables2[-2]
            if penult1 == penult2:
                return "F"
        return "M"

    # Not a clear match, return error
    else:
        #if word1.endswith("oun") and word2.endswith("oun"):
          #  return "M"
        #it = input(f"{word1} and {word2}")
        #if it == "":
        return "E"

# Function to extract the final words of each line in the text, removing punctuation
lines = []
def get_final_words(text):
    global lines
    lines = text.split('\n')
    final_words = []
    for line in lines:
        line = line.strip("-")
        line = line.strip()
        if line:  # Only process non-empty lines
            words = line.split()
            # Remove punctuation from the final word

            final_word = words[-1].strip(string.punctuation).strip("-")
            final_words.append(final_word)
    return final_words

# Function to identify the regions of consecutive feminine rhymes above a threshold percentage
def find_longest_feminine_regions(rhyme_types, threshold=0.5):
    longest_regions = []
    current_start = None
    current_fem_count = 0
    total_count = 0
    
    for i, rhyme in enumerate(rhyme_types):
        if rhyme == 'F':
            if current_start is None:
                current_start = i
            current_fem_count += 1
        elif current_start is not None:
            # We hit a non-feminine rhyme or the end of the list
            total_count = i - current_start
            if current_fem_count / total_count >= threshold:
                longest_regions.append((current_start + 1, i))  # Start and end line numbers
            current_start = None
            current_fem_count = 0
    
    # Check if we ended on a region
    if current_start is not None:
        total_count = len(rhyme_types) - current_start
        if current_fem_count / total_count >= threshold:
            longest_regions.append((current_start + 1, len(rhyme_types)))

    return sorted(longest_regions, key=lambda x: (x[1] - x[0]), reverse=True)[:3]

# Function to process a directory of text files and plot the results
def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, "r") as file:
                text = file.read()

            final_words = get_final_words(text)
            if len(final_words)>0:

                # Check the rhyme type for each couplet (pair of lines)
                rhyme_types = []
                for i in range(0, len(final_words) - 1, 2):
                    rhyme_type = get_rhyme_type(final_words[i], final_words[i + 1])
                    rhyme_types.append(rhyme_type)
 #                   if rhyme_type == "F":
#                        print(final_words[i:i+2])

                # Count occurrences of masculine, feminine, and error rhymes
                mascu_count = rhyme_types.count('M')
                femi_count = rhyme_types.count('F')
                error_count = rhyme_types.count('E')

                # Print rhyme statistics
                print(f"Statistics for {filename}:")
                print(f"Total Lines: {len(final_words)}")
                print(f"Feminine Rhymes: {femi_count}, ({(femi_count / len(final_words)) * 100:.2f}%)")
                print(f"Masculine Rhymes: {mascu_count}, ({(mascu_count / len(final_words)) * 100:.2f}%)")
                print(f"Errors: {error_count}, ({(error_count / len(final_words)) * 100:.2f}%)")
                print()

                # Save results to CSV
                csv_filename = 'csvs/' + filename.replace('.txt', '_rhyme_report.csv')
                with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(['Line Start', 'Line End', 'Rhyme Type', 'Words'])
                    for i, rhyme in enumerate(rhyme_types):
                        writer.writerow([i * 2 + 1, (i * 2) + 2, rhyme, final_words[i*2] + ' / ' + final_words[i*2+1]])

                # Plot the rhyme types
                x = np.arange(1, len(rhyme_types) * 2, 2)
                y = [1 if rhyme == 'F' else 0 for rhyme in rhyme_types]
                plt.figure(figsize=(10, 6))
                plt.scatter(x, y, color='red', label='Feminine Rhyme', s=1)
                plt.xlabel('Line Number')
                plt.ylabel('Rhyme Type (1 = Feminine, 0 = Masculine)')
                plt.title(f'Rhyme Analysis for {filename}')
                plt.savefig(f"plots/{filename.replace('.txt', '_rhyme_plot.png')}")
                plt.close()

            ## Find regions of high density feminine rhyme
            #thresholds = [0.5, 0.7, 0.9]
            #for threshold in thresholds:
             #   print(f"Longest feminine rhyme regions for {filename} (threshold: {threshold * 100}%):")
              #  longest_regions = find_longest_feminine_regions(rhyme_types, threshold)
               # for region in longest_regions:
                #    print(f"Start Line: {region[0]}, End Line: {region[1]}")

# Process a directory of text files
process_directory('./txt_tales')  # Replace with actual directory path
