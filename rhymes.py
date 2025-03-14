import re
import string

# Function to break a word into syllables, considering vowel combinations and consonant blends
vowels = "aeiouy"
def break_into_syllables(word):
    vowels = "aeiouy"
    
    # Treat combinations as single syllables (vowel combinations and consonant blends)
    word = word.lower()
    
    # Replace common vowel combinations with placeholders to treat them as single syllables
    word = word.replace("ou", "ou_")  # Treat "ou" as a single syllable unit (e.g., flour)
    word = word.replace("ai", "ai_")  # Treat "ai" as a single syllable unit
    word = word.replace("ei", "ei_")  # Treat "ei" as a single syllable unit
    word = word.replace("au", "au_")  # Treat "au" as a single syllable unit
    word = word.replace("ea", "ea_")  # Treat "ea" as a single syllable unit (e.g., "bread")
    word = word.replace("ie", "ie_")  # Treat "ie" as a single syllable unit
    word = word.replace("oo", "oo_")  # Treat "oo" as a single syllable unit
    
    # Consonant blends that should be treated as part of the syllable
    word = word.replace("sh", "sh_")  # Treat "sh" as a single unit
    word = word.replace("ch", "ch_")  # Treat "ch" as a single unit
    word = word.replace("st", "st_")  # Treat "st" as a single unit
    word = word.replace("cl", "cl_")  # Treat "cl" as a single unit
    word = word.replace("fl", "fl_")  # Treat "fl" as a single unit
    word = word.replace("gl", "gl_")  # Treat "gl" as a single unit
    word = word.replace("bl", "bl_")  # Treat "bl" as a single unit
    word = word.replace("wh", "wh_")  # Treat "wh" as a single unit
    word = word.replace("gh", "gh_")  # Treat "gh" as a single unit
    word = word.replace("th", "th_")  # Treat "th" as a single unit
    
    # Now split based on vowels and consonant clusters
    syllables = re.findall(r'[^aeiouy]*[aeiouy]+(?:[^aeiouy]*|$)', word)
    
    # Replace the placeholders back to their original form
    syllables = [syllable.replace("ou_", "ou").replace("ai_", "ai").replace("ei_", "ei")
                 .replace("au_", "au").replace("ea_", "ea").replace("ie_", "ie")
                 .replace("oo_", "oo").replace("sh_", "sh").replace("ch_", "ch")
                 .replace("st_", "st").replace("cl_", "cl").replace("fl_", "fl")
                 .replace("gl_", "gl").replace("bl_", "bl").replace("wh_", "wh")
                 .replace("gh_", "gh").replace("th_", "th") for syllable in syllables]

    print(syllables)
    
    return syllables

# Function to check the rhyme type (masculine or feminine)
def get_rhyme_type(word1, word2):
    syllables1 = break_into_syllables(word1)
    syllables2 = break_into_syllables(word2)

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
def get_final_words(text):
    global lines
    lines = text.split('\n')
    final_words = []
    for line in lines:
        line = line.strip("-")
        #line = line.strip("-")
        line = line.strip()
        if line:  # Only process non-empty lines
            words = line.split()
            # Remove punctuation from the final word
            final_word = words[-1].strip(string.punctuation).strip("-")
            final_words.append(final_word)  # Add the cleaned word to the list
    return final_words

# Example text (Middle English from The Canterbury Tales)
filename = "wob_tale.txt"
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
        print(lines[i-1:i+1])
        print(f"Words: {word1} and {word2}, {i}", file = f)
        print(lines[i-1:i+1], file = f)
        fem_num+=1
    if rhyme == "M":
        masc_num+=1
    type_dict[i] = rhyme
    
    i+=2

print(f"number of lines: {i-2}, number of masculine rhymes: {masc_num}, number of feminine rhymes: {fem_num}")
print(f"number of lines: {i-2}, number of masculine rhymes: {masc_num}, number of feminine rhymes: {fem_num}", file = f)


#print(type_dict)
