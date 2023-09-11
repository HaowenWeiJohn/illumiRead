import Levenshtein

# Define a QWERTY keyboard layout
keyboard_layout = {
    'q': 'qwertasdfgzxcvb',
    'w': 'wqazsxedcrfvtg',
    'e': 'ewrsdfcxzaq',
    'r': 'retdfvgbwsxcza',
    't': 'tryfhvngbqawexzs',
    'y': 'ytughnjmklop',
    'u': 'uyihjkolmnp',
    'i': 'iuojklnmp',
    'o': 'oiplkjmn',
    'p': 'po;lkmn',
    'a': 'aqszwx',
    's': 'swedcxzaq',
    'd': 'deasrfcxz',
    'f': 'frtgvdxc',
    'g': 'gtyhbfxv',
    'h': 'hyujnbgv',
    'j': 'jhuikmn',
    'k': 'kjilmon',
    'l': 'lkop',
    'z': 'zaxs',
    'x': 'xzcd',
    'c': 'cxv',
    'v': 'vbc',
    'b': 'bnv',
    'n': 'nm',
    'm': 'mn',
}

# Function to get neighboring keys on the QWERTY keyboard
def get_neighboring_keys(key):
    return keyboard_layout.get(key, key)

# Function to correct a misspelled word
def correct_spelling(word):
    suggestions = []

    # Generate possible corrections based on keyboard layout
    for char in word:
        neighbors = get_neighboring_keys(char)
        for neighbor in neighbors:
            suggestion = word.replace(char, neighbor, 1)
            suggestions.append(suggestion)

    # Calculate Levenshtein distances between the suggestions and the original word
    distances = [Levenshtein.distance(word, suggestion) for suggestion in suggestions]

    # Choose the suggestion with the smallest Levenshtein distance
    min_distance_index = distances.index(min(distances))
    corrected_word = suggestions[min_distance_index]

    return corrected_word

# Example usage
misspelled_word = "hwllo"
corrected_word = correct_spelling(misspelled_word)
print(f"Original word: {misspelled_word}")
print(f"Corrected word: {corrected_word}")