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

    syllables1 = break_into_syllables(word1)
    syllables2 = break_into_syllables(word2)
    print(syllables1,syllables2)

    if len(syllables1) == 1 or len(syllables2) == 1:
        return "M"
    
    last_syllable1 = syllables1[-1]
    last_syllable2 = syllables2[-1]

    
    if last_syllable1 == last_syllable2:
        # For feminine rhyme, there should be an additional matching syllable before the last one
        if len(syllables1) > 1 and len(syllables2) > 1:
            syllables1 = syllables1[:-1]
            syllables2 = syllables2[:-1]
            if last_syllable1 == "e" and last_syllable2 == "e" and len(syllables1) > 1 and len(syllables2) >1:
                syllables1 = syllables1[:-1]
                syllables2 = syllables2[:-1]
            if syllables1[-1] == syllables2[-1]:
                return "F"
            elif last_syllable1!="e" and set(syllables1[-1]).intersection(set(vowels)) == set(syllables2[-1]).intersection(set(vowels)):
                user = input(f"{word1},{word2},{syllables1},{syllables2}")
                return user
            else:
                return "M"
        else:
            return "M"
    else:
        user = input(f"{word1},{word2},{syllables1},{syllables2}")
        return user
    return "No Rhyme"

    return "WHAT"
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
        #line = line.strip("-")
        line = line.strip()
        if line:  # Only process non-empty lines
            lines_ammended.append(og_line)
            words = line.split()
            # Remove punctuation from the final word
            final_word = words[-1].strip(string.punctuation).strip("-")
            final_words.append(final_word)  # Add the cleaned word to the list
    return final_words

# Example text (Middle English from The Canterbury Tales)
filename = "pardoner.txt"
with open(filename, "r") as file:
    text = file.read()

# Extract final words from the text
final_words = get_final_words(text)

# Check the rhyme type for each couplet (pair of lines)
couplet_rhymes = []
for i in range(0, len(final_words)-1, 2):
    rhyme_type = get_rhyme_type(final_words[i], final_words[i+1])
    couplet_rhymes.append((final_words[i], final_words[i+1], rhyme_type))

# Print the results for each couplet
type_dict = {}
i=1
fem_num = 0
masc_num = 0
f = open('output.txt', 'w')
#print('something', file = f)
for word1, word2, rhyme in couplet_rhymes:
    if rhyme == 'F':
        print(f"Words: {word1} and {word2}, {i}")
        print(lines_ammended[i-1:i+1])
        print(f"Words: {word1} and {word2}, {i}", file = f)
        print(lines_ammended[i-1:i+1], file = f)
        fem_num+=1
    if rhyme == "M":
        masc_num+=1
    type_dict[i] = rhyme
    
    i+=2

print(f"number of lines: {i-2}, number of masculine rhymes: {masc_num}, number of feminine rhymes: {fem_num}")
print(f"number of lines: {i-2}, number of masculine rhymes: {masc_num}, number of feminine rhymes: {fem_num}", file = f)


#print(type_dict)
