# Middle English Rhyme Detector

## Overview

This Python script detects and classifies masculine and feminine rhymes in Middle English poetry. It processes a text file, extracts final words from each line, and analyzes their rhyme patterns by comparing syllables. The program supports optional vowel substitution for historically rhyming vowels, eliminates final -e syllables in rhyme analysis, and provides results in both the terminal and a file.

---

## What the Program Does

1. **Text Input and Final Word Extraction**
   - The program reads a `.txt` file containing Middle English poetry.
   - It extracts the final word from each line, removing punctuation and whitespace.

2. **Normalization and Optional Vowel Substitution**
   - The program can normalize spelling by substituting historically rhyming vowels (e.g., *ou* and *ow*, *our* and *ur*) when enabled.
   - The substitution can be toggled on or off using a flag:
     ```python
     enable_vowel_substitution = True  # or False
     ```

3. **Final -e Elimination**
   - The program removes final unstressed "e" syllables (common in Middle English) during rhyme analysis to avoid false positives in feminine rhyme detection. This ensures that the presence of a final -e doesn't incorrectly classify a rhyme as feminine.
   - For example, words like *name* and *fame* might be eliminated from consideration as feminine rhymes if the final "e" is the only matching sound.

4. **Syllable Detection**
   - Each word is broken into syllables using a regular expression that identifies vowel and consonant clusters.
   - The program treats known vowel combinations (e.g., *ai*, *ou*) as single syllabic units.
   - Consonant blends (e.g., *sh*, *ch*) are also treated as part of the syllable.

5. **Rhyme Classification**
   - For every pair of final words (assumed to be rhyming couplets), the program compares the last syllables:
     - If the final syllables match, it checks the second-to-last syllables.
     - If both final and penultimate syllables match, the rhyme is classified as **feminine (F)**.
     - If only the final syllables match, the rhyme is classified as **masculine (M)**.
     - If the final syllables do not match, the program prompts the user to classify the rhyme manually.

6. **Output**
   - The program prints the results to the terminal, showing:
     - Word pairs
     - The rhyme classification (masculine or feminine)
     - Corresponding lines from the poem
   - It also writes the results to an `output.txt` file, which includes:
     - The rhyme type for each word pair
     - The lines from the poem that contain the rhyming words
   - A rhyme type dictionary is created for easy reference.

7. **User Interaction**
   - In cases where the rhyme is ambiguous, the program prompts the user to manually classify the rhyme type.
   - The user can provide input to determine whether the rhyme is masculine or feminine based on the context.

---

## How to Use

1. Prepare a Middle English poem in `.txt` format.
2. Set the filename for the input file:
   ```python
   filename = "your_poem.txt"
