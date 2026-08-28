"""
COMP1730 Lab Solutions: Dictionaries
Exercises 1-4
"""

# ============================================================
# Exercise 1: Removing Dictionary Entries
# ============================================================

# --- Task 1: Remove a key without modifying the original dictionary ---
def allbut_key(a_dict, key):
    """Return a new dictionary containing all key-value pairs of a_dict
    except the one with the given key. a_dict is not modified."""
    new_dict = a_dict.copy()
    new_dict.pop(key, None)  # None avoids KeyError if key isn't present
    return new_dict


# --- Task 2: Remove keys in place ---
def remove_keys_in_place(a_dict, keys_to_remove):
    """Modify a_dict in place, removing every key in keys_to_remove.
    Returns nothing."""
    for key in keys_to_remove:
        a_dict.pop(key, None)


# --- Task 3: Removing dictionary entries while iterating ---
def remove_inactive_students(student_dict):
    """Modify student_dict in place, removing every student whose
    status is 'inactive'. Returns nothing."""
    # Can't remove keys while iterating over the dict itself, so we
    # collect the keys to remove first, then remove them afterwards.
    inactive_ids = [sid for sid, status in student_dict.items()
                    if status == "inactive"]
    for sid in inactive_ids:
        del student_dict[sid]


# Reflection answers (as comments):
#
# 1. What error occurs when a dictionary is modified while it is being
#    iterated over?
#    A `RuntimeError: dictionary changed size during iteration`.
#
# 2. Why does this happen?
#    Python's dict iterator walks the dictionary's internal structure in
#    a fixed sequence. If the dictionary's size changes (a key is added
#    or removed) while that walk is in progress, the iterator's internal
#    bookkeeping becomes invalid/out of sync with the dict, so Python
#    raises an error rather than risk skipping entries or crashing.
#    (Note: changing the *value* of an existing key is fine -- it's only
#    adding/removing keys, which changes the dict's size, that breaks
#    iteration.)
#
# 3. How can you safely remove multiple items from a dictionary?
#    Don't mutate the dictionary while looping over it directly. Instead:
#      (a) first build a separate list of the keys you want to remove
#          (e.g. with a list comprehension over dict.items()), then loop
#          over that list afterwards and call `del`/`pop` on the dict, or
#      (b) iterate over a copy of the keys/items, e.g.
#          `for key in list(a_dict.keys()):`, removing from the
#          original dict as you go.


# ============================================================
# Exercise 2: Inverting a Dictionary
# ============================================================

def invert_dictionary(dictionary):
    """Return a new dictionary inverse_dictionary such that
    inverse_dictionary[x] == y whenever dictionary[y] == x.
    Every value in `dictionary` must be unique, otherwise the inversion
    is ambiguous and an AssertionError is raised."""
    inverse_dictionary = {}
    for key, value in dictionary.items():
        assert value not in inverse_dictionary, \
            f"Cannot invert: value {value!r} maps from more than one key"
        inverse_dictionary[value] = key
    return inverse_dictionary


def invert_dictionary_non_unique(dictionary):
    """Return a new dictionary that maps each value in `dictionary` to
    the SET of keys that mapped to it in the original dictionary."""
    inverse_dictionary = {}
    for key, value in dictionary.items():
        if value not in inverse_dictionary:
            inverse_dictionary[value] = set()
        inverse_dictionary[value].add(key)
    return inverse_dictionary


# ============================================================
# Exercise 3: Wordplay
# ============================================================

def read_words(filename):
    """Read a wordlist file (one word per line) into a list of words."""
    with open(filename) as f:
        words = [line.strip() for line in f if line.strip()]
    return words


# --- Task 1 ---
def most_frequent_word_lengths(word_list, top_n):
    """Return a list of the top_n most frequent word lengths in the
    word list, in descending order of frequency."""
    length_counts = {}
    for word in word_list:
        length = len(word)
        length_counts[length] = length_counts.get(length, 0) + 1

    # Build (count, length) pairs so that sorting compares counts first.
    pairs = [(count, length) for length, count in length_counts.items()]
    pairs.sort(reverse=True)  # descending by count (then by length)

    return [length for count, length in pairs[:top_n]]


# --- Task 2 ---
def first_three_consecutive_double_letters(word_list):
    """Return the first word in word_list that contains three
    consecutive double letters (e.g. 'commttee' -> 'mm','tt','tt'... );
    a single interrupting letter, as in 'committee', disqualifies it.
    Returns None if no such word exists."""
    for word in word_list:
        i = 0
        run = 0  # number of consecutive double-letter pairs seen
        while i < len(word) - 1:
            if word[i] == word[i + 1]:
                run += 1
                if run == 3:
                    return word
                i += 2  # skip past this double letter, continue checking
            else:
                run = 0
                i += 1
    return None


# --- Task 3a ---
def most_frequent_bigrams(word_list, top_n):
    """Return the top_n most frequent bi-grams (pairs of consecutive
    letters) across all words in word_list, in descending order."""
    bigram_counts = {}
    for word in word_list:
        for i in range(len(word) - 1):
            bigram = word[i:i + 2]
            bigram_counts[bigram] = bigram_counts.get(bigram, 0) + 1

    pairs = [(count, bigram) for bigram, count in bigram_counts.items()]
    pairs.sort(reverse=True)

    return [bigram for count, bigram in pairs[:top_n]]


# --- Task 3b ---
def non_present_bigrams(word_list):
    """Return a set of all two-letter bi-grams (from the 26-letter
    English alphabet) that never appear in word_list."""
    import string
    all_bigrams = {a + b for a in string.ascii_lowercase
                   for b in string.ascii_lowercase}

    present_bigrams = set()
    for word in word_list:
        for i in range(len(word) - 1):
            present_bigrams.add(word[i:i + 2])

    return all_bigrams - present_bigrams


# ============================================================
# Exercise 4: Permutation
# ============================================================

def closed_sets(permutation):
    """Return a list of sets representing all the closed sets of the
    given permutation (a dict mapping each element to the element it's
    permuted to)."""
    visited = set()
    result = []

    for start in permutation:
        if start in visited:
            continue
        # Follow the cycle starting at `start` until we return to it.
        cycle = set()
        current = start
        while current not in cycle:
            cycle.add(current)
            visited.add(current)
            current = permutation[current]
        result.append(cycle)

    return result


# ============================================================
# Quick self-tests / demonstration
# ============================================================
if __name__ == "__main__":
    # Exercise 1
    student = {"name": "Sam", "age": 20, "grade": "HD", "city": "Canberra"}
    new_student = allbut_key(student, "age")
    print("Ex1 Task1:", new_student, "| original untouched:", student)

    remove_keys_in_place(student, ["age", "city"])
    print("Ex1 Task2:", student)

    students = {"u1234567": "active", "u1234568": "inactive",
                "u1234569": "active", "u1234570": "inactive"}
    remove_inactive_students(students)
    print("Ex1 Task3:", students)

    # Exercise 2
    def histogram(s):
        h = {}
        for c in s:
            h[c] = h.get(c, 0) + 1
        return h

    hist = histogram("mississippi")
    print("Ex2 histogram:", hist)
    print("Ex2 invert_dictionary_non_unique:", invert_dictionary_non_unique(hist))
    try:
        invert_dictionary(hist)
    except AssertionError as e:
        print("Ex2 invert_dictionary correctly raised:", e)

    unique_dict = {"a": 1, "b": 2, "c": 3}
    print("Ex2 invert_dictionary (unique):", invert_dictionary(unique_dict))

    # Exercise 3 (using a tiny sample word list instead of wordlist.txt)
    sample_words = ["a", "an", "and", "band", "hand", "committee", "commttee"]
    print("Ex3 Task1:", most_frequent_word_lengths(sample_words, 2))
    print("Ex3 Task2:", first_three_consecutive_double_letters(sample_words))
    print("Ex3 Task3a:", most_frequent_bigrams(sample_words, 3))
    non_present = non_present_bigrams(sample_words)
    print("Ex3 Task3b: number of missing bigrams:", len(non_present))

    # Exercise 4
    p1 = {'alice': 'carol', 'bob': 'bob', 'carol': 'eve',
          'dave': 'dave', 'eve': 'alice'}
    p2 = {'alice': 'bob', 'bob': 'carol', 'carol': 'dave',
          'dave': 'eve', 'eve': 'alice'}
    print("Ex4 p1 closed sets:", closed_sets(p1))
    print("Ex4 p2 closed sets:", closed_sets(p2))