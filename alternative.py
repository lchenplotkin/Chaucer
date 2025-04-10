import re

# Set of vowels for syllable detection
vowels = "aeiouy"

# Define transformation rules for rhyme normalization
#substitution_rules = [
 #   (r'(y|i)$', 'y'), # Normalize plural or variant forms ending with "ies" or "i"
#]

# Function to apply the substitutions to the word
def apply_substitutions(word):
    word = word.lower()  # Convert to lowercase for consistent comparison
    #for pattern, replacement in substitution_rules:
     #   word = re.sub(pattern, replacement, word)
    return word

# Function to extract the longest common suffix between two words
def get_longest_common_suffix(word1, word2):
    # Apply substitutions to normalize the words
    word1 = apply_substitutions(word1)
    word2 = apply_substitutions(word2)

    # Initialize the longest common suffix
    common_suffix = ""
    
    # Compare the words from the end towards the beginning
    min_len = min(len(word1), len(word2))
    for i in range(1, min_len+1):
        if word1[-i] == word2[-i]:
            common_suffix = word1[-i] + common_suffix
        else:
            break
    
    return common_suffix

# Function to count syllables in a word (based on vowels)
def count_syllables(word):
    word = word.lower()
    syllables = 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i-1] not in vowels:
            syllables += 1
    return syllables

# Function to detect if the rhyme is feminine (based on the syllable count of the common suffix)
def is_feminine_rhyme(word1, word2):
    # Get the longest common suffix
    common_suffix = get_longest_common_suffix(word1, word2)
    
    # If the common suffix has more than 1 syllable, consider it a feminine rhyme
    return count_syllables(common_suffix) > 1

# Example function to check rhymes in a text
def check_rhymes_in_text(text):
    final_words = get_final_words(text)  # Assume you have a function to get the final words from each line
    rhyme_results = []
    
    for i in range(0, len(final_words)-1, 2):
        word1, word2 = final_words[i], final_words[i+1]
        if is_feminine_rhyme(word1, word2):
            rhyme_results.append((word1, word2, 'Feminine'))
        else:
            rhyme_results.append((word1, word2, 'Masculine'))
    
    return rhyme_results

# Example function to extract final words from each line
def get_final_words(text):
    final_words = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip("-").strip()
        if line:
            words = line.split()
            final_words.append(words[-1])  # Only one word if it's a single-word line
    return final_words

# Example text (Middle English from The Canterbury Tales)
filename = "txt_tales/summoner_tale.txt"
with open(filename, "r") as file:
    text = file.read()

# Check rhymes in the text
rhyme_results = check_rhymes_in_text(text)

# Output the results for rhyme type
femi_count = 0
masc_count = 0
for word1, word2, rhyme_type in rhyme_results:
    print(f"{word1} - {word2} => {rhyme_type}")
    if rhyme_type == 'Feminine':
        femi_count += 1
    else:
        masc_count += 1

print(f"Total Feminine Rhymes: {femi_count}")
print(f"Total Masculine Rhymes: {masc_count}")

