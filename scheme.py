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

    #print(syllables)
    
    return syllables

# Function to check the rhyme type (masculine or feminine)
def get_rhyme_type(word1, word2):
    syllables1 = break_into_syllables(word1)
    syllables2 = break_into_syllables(word2)
    #print(syllables1,syllables2)

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
def get_final_words(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return [line.split()[-1].strip(string.punctuation) for line in lines], lines

filename = "monk_tale.txt"
with open(filename, "r") as file:
    text = file.read()

final_words, lines = get_final_words(text)

rhyme_scheme = [(0, 2), (1, 3),(3,4),(4,6), (5, 7)]
num_stanzas = len(final_words) // 8
fem_num = masc_num = 0

results = []
comp=0
with open('output.txt', 'w') as f:
    line_num=0
    for stanza in range(num_stanzas):
        stanza_start = stanza * 8
        stanza_words = final_words[stanza_start:stanza_start + 8]
        stanza_lines = lines[stanza_start:stanza_start + 8]
        type_list = ["","","","","","","",""]
        
        for i, j in rhyme_scheme:
            word1, word2 = stanza_words[i], stanza_words[j]
            #print(word1,word2)
            rhyme_type = get_rhyme_type(word1, word2)
            if rhyme_type == "F":
                type_list[i]="F"
                type_list[j]="F"

                results.append(f"Feminine rhyme: {word1} and {word2}, lines {stanza_start + i}, {stanza_start+j}")
                results.append(stanza_lines[i])
                results.append(stanza_lines[j])

            elif rhyme_type == "M":
                if type_list[i]!="F":
                    type_list[i] = "M"
                if type_list[j]!="F":
                    type_list[j] = "M"
        
        for gender in type_list:
            if gender == "F":
                fem_num+=1
            elif gender == "M":
                masc_num+=1

for line in results:
    print(line)

print(f"Total lines: {len(final_words)}, Total feminine rhymes: {fem_num}, masculine rhymes: {masc_num}")
