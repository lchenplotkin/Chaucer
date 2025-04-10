import re
import string
import csv
import os
import matplotlib.pyplot as plt

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

    if allow_vowel_substitution:
        word = re.sub(r'(ai|ay|ei|ey)$', 'ay', word)
        word = re.sub(r'(ow|ough)$', 'ow', word)
        word = re.sub(r'(ough|uff)$', 'uff', word)
        word = re.sub(r'(ys|is|es|ous)$', 'is', word)
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

    # Fix syllabification for cases like 'insufficient'
    # Ensure splits for complex words like 'cient', 'sufficient', etc.
    syllables = [s.replace("ci", "ci_").replace("ient", "ie_nt") for s in syllables]
    syllables = [s.replace("_", "") for s in syllables]

    return syllables

# List of common Middle English feminine rhyme endings
feminine_endings = [
    "oun", "inge", "ynge", "ioun", "cioun", "able", "ible", "inesse", 
    "itye", "ence", "aunce", "ance", "eede", "hede", "ine", "ous", "is", "ure", "oyed"
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

    # Masculine if one of the words is monosyllabic
    if len(syllables1) == 1 or len(syllables2) == 1:
        return "M"

    # Early exit if the words match a known feminine ending
    if ends_in_common_feminine(word1.lower(), word2.lower()):
        return "F"

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
            if penult1 == penult2:
                return "F"
            else:
                if strip_to_vowels(penult1) == strip_to_vowels(penult2):
                    return "F"
        return "M"

    # If last syllables differ, try matching just vowels
    elif strip_to_vowels(last1) == strip_to_vowels(last2):
        if len(syllables1) >= 2 and len(syllables2) >= 2:
            penult1 = syllables1[-2]
            penult2 = syllables2[-2]
            if strip_to_vowels(penult1) == strip_to_vowels(penult2):
                return "F"
        return "M"

    # Not a clear match, fallback to manual check
    else:
        #user = input(f"{word1},{word2},{syllables1},{syllables2}")
        return "E"

# Function to extract the final words of each line in the text, removing punctuation
lines = []
lines_ammended = []
def get_final_words(text):
    global lines
    lines = text.split('\n')
    final_words = []
    for line in lines:
        og_line = line
        line = line.strip("-")
        line = line.strip()
        if line:  # Only process non-empty lines
            lines_ammended.append(og_line)
            words = line.split()
            # Remove punctuation from the final word
            final_word = words[-1].strip(string.punctuation).strip("-")
            final_words.append(final_word)  # Add the cleaned word to the list
    return final_words

# Function to process files in a directory
def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r") as file:
                text = file.read()

            # Extract final words from the text
            final_words = get_final_words(text)

            # Check the rhyme type for each couplet (pair of lines)
            couplet_rhymes = []
            for i in range(0, len(final_words)-1, 2):
                rhyme_type = get_rhyme_type(final_words[i], final_words[i+1])
                couplet_rhymes.append((i+1, final_words[i], final_words[i+1], rhyme_type))

            # Write the results to a CSV file
            csv_filename = f"{filename.split('/')[-1].split('.')[0]}_rhymes.csv"
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Line Number', 'Word 1', 'Word 2', 'Rhyme Type'])
                for line_num, word1, word2, rhyme in couplet_rhymes:
                    writer.writerow([line_num, word1, word2, rhyme])

            # Optional: Plot the feminine rhymes (if desired)
            feminine_rhyme_lines = [line_num for line_num, word1, word2, rhyme in couplet_rhymes if rhyme == 'F']
            plt.scatter(feminine_rhyme_lines, [1] * len(feminine_rhyme_lines), label=f"{filename} Feminine Rhymes")
    
    # Show the plot for all files
    plt.xlabel('Line Number')
    plt.ylabel('Feminine Rhymes (Constant)')
    plt.title('Feminine Rhymes Across Files')
    plt.legend()
    plt.show()

# Directory path containing the text files
directory_path = "txt_tales"  # Replace with your directory path
process_directory(directory_path)

