import re
import string

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
        word = re.sub(r'(au|aw)$', 'aw', word)
        word = re.sub(r'(ow|ough)$', 'ow', word)
        word = re.sub(r'(ough|uff)$', 'uff', word)
        word = re.sub(r'(ance|aunce|aunse)$', 'ance', word)
        word = re.sub(r'(ys|is|es|ous)$', 'is', word)
        word = re.sub(r'([aeiou])w?r$', r'\1ur', word)
    
    return word

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

# Function to determine rhyme type: Masculine or Feminine
def get_rhyme_type(word1, word2):
    # Use standardized rhyme forms for comparison
    form1 = standardize_rhyme_form(word1, allow_vowel_substitution=ALLOW_VOWEL_SUBSTITUTION)
    form2 = standardize_rhyme_form(word2, allow_vowel_substitution=ALLOW_VOWEL_SUBSTITUTION)

    syllables1 = break_into_syllables(form1)
    syllables2 = break_into_syllables(form2)

    if len(syllables1) == 1 or len(syllables2) == 1:
        return "M"

    last_syllable1 = syllables1[-1]
    last_syllable2 = syllables2[-1]

    if last_syllable1 == last_syllable2:
        if len(syllables1) > 1 and len(syllables2) > 1:
            penult1 = syllables1[-2]
            penult2 = syllables2[-2]
            if last_syllable1 != "e" and penult1 == penult2:
                print(penult1,penult2)
                print(last_syllable1,last_syllable2)
                return "F"
            elif penult1==penult2:
                if last_syllable1 == "e":
                    if len(syllables1)>2 and len(syllables2)>2:
                        if syllables1[-3] == syllables2[-3]:
                            return "F"
                else:
                    return "F"
        return "M"
    else:
        # Manual check fallback
        user = input(f"Check manually: {word1}, {word2} → {syllables1}, {syllables2}: ")
        return user

# Function to extract final words of each line in a poem
lines = []
lines_ammended = []

def get_final_words(text):
    global lines
    lines = text.split('\n')
    final_words = []

    for line in lines:
        original_line = line
        line = line.strip(" -").strip()
        if line:
            lines_ammended.append(original_line)
            words = line.split()
            final_word = words[-1].strip(string.punctuation + "-")
            final_words.append(final_word)
    return final_words

# Load Middle English text file
filename = "pardoner.txt"
with open(filename, "r") as file:
    text = file.read()

# Extract final words from each line
final_words = get_final_words(text)

# Detect rhymes in couplets
couplet_rhymes = []
for i in range(0, len(final_words)-1, 2):
    rhyme_type = get_rhyme_type(final_words[i], final_words[i+1])
    couplet_rhymes.append((final_words[i], final_words[i+1], rhyme_type))

# Output results
type_dict = {}
fem_num = 0
masc_num = 0
i = 1

with open('output.txt', 'w') as f:
    for word1, word2, rhyme in couplet_rhymes:
        if rhyme == 'F':
            print(f"Words: {word1} and {word2}, {i}")
            print(lines_ammended[i-1:i+1])
            print(f"Words: {word1} and {word2}, {i}", file=f)
            print(lines_ammended[i-1:i+1], file=f)
            fem_num += 1
        elif rhyme == "M":
            masc_num += 1
        type_dict[i] = rhyme
        i += 2

    print(f"\nTotal lines: {i-2}, Masculine rhymes: {masc_num}, Feminine rhymes: {fem_num}")
    print(f"Total lines: {i-2}, Masculine rhymes: {masc_num}, Feminine rhymes: {fem_num}", file=f)

