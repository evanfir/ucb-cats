"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    list_of_acceptable_strings = [item for item in paragraphs if select(item)]
    if k >= len(list_of_acceptable_strings):
        return ''
    else:
        return list_of_acceptable_strings[k]

    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    from utils import remove_punctuation
    def select(sentense):
        list_of_words = sentense.split()
        for word in list_of_words:
            word = remove_punctuation(word).lower()
            if word in topic:
                return True
        return False
    return select

    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    shorter_list_len = min(len(typed_words), len(reference_words))
    longer_list_len = max(len(typed_words), len(reference_words))
    incorrect_words = 0
    for index in range(shorter_list_len):
        if typed_words[index] != reference_words[index]:
            incorrect_words += 1
    incorrect_words += abs(longer_list_len - shorter_list_len)
    if incorrect_words >= longer_list_len:
        return 0.0
    # else:
        # return ((longer_list_len - incorrect_words)/min(shorter_list_len, longer_list_len)) * 100
    elif len(typed_words) <= len(reference_words):
        return ((longer_list_len - incorrect_words)/shorter_list_len) * 100
    else:
        return ((longer_list_len - incorrect_words)/longer_list_len) * 100
 
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    num_of_words = len(typed) / 5
    return num_of_words * 60 / elapsed
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    score_list = list()
    if user_word in valid_words:
        return user_word
    else:
        for index in range(len(valid_words)):
            score_list += [diff_function(user_word, valid_words[index], limit)]

        if min(score_list) <= limit:
            return valid_words[score_list.index(min(score_list))]
        else:
            return user_word
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    # assert False, 'Remove this line'
    shorter_length = min(len(start), len(goal))
    num_of_diff = abs(len(start) - len(goal))
    if num_of_diff > limit:
        return num_of_diff
    def number_of_swap(iteration = 0, num_of_diff = 0):
        if iteration >= shorter_length:
            return num_of_diff
        if start[iteration] != goal[iteration]:
            num_of_diff += 1
        if num_of_diff > limit:
            return num_of_diff
        
        
        return number_of_swap(iteration = iteration + 1, num_of_diff = num_of_diff)

    
    return number_of_swap(num_of_diff = num_of_diff)
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    if abs(len(start) - len(goal)) > limit: # Fill in the condition
        # BEGIN
        return abs(len(start) - len(goal))
        # END
    elif start == goal:
        start = ""
        goal = ""
        return 0
    elif start == "" or goal == "":
        # print("EMPTY: START:", start, "GOAL:", goal)
        return max(len(goal), len(start))
    
    elif start[0] == goal[0]: # Feel free to remove or add additional cases
        # BEGIN
        # print("FIRST ==")
        return edit_diff(start[1:], goal[1:], limit)
        # END
    elif limit == 0:
        return 1
    else:
        add_diff = 1+ edit_diff(start, goal[1:], limit - 1)  # Fill in these lines
        remove_diff = 1 + edit_diff(start[1:], goal, limit - 1) 
        substitute_diff = 1 + edit_diff(start[1:], goal[1:], limit - 1) 
        # BEGIN
        number_of_changes = min(add_diff, remove_diff, substitute_diff) #-limit
        return number_of_changes
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    num_of_correct = 0
    for i in range(min(len(typed), len(prompt))):
        if typed[i] == prompt[i]:
            num_of_correct += 1
        elif typed[i] != prompt[i]:
            break
    progress = num_of_correct / len(prompt)
    progress = user_progress(id, progress)
    send(progress)
    return get_progress(progress)
    # END PROBLEM 8

def user_progress(id, progress):
    return {'id': id, 'progress': progress}

def get_id(progress):
    return progress['id']

def get_progress(progress):
    return progress['progress']

def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    """
    >>> p0 = [word_time('START', 0), word_time('What', 0.2), word_time('great', 0.4), word_time('luck', 0.8)]
    >>> p1 = [word_time('START', 0), word_time('What', 0.6), word_time('great', 0.8), word_time('luck', 1.19)]
    >>> fastest_words([p0, p1])
    [['What', 'great'], ['great', 'luck']]
    >>> fastest_words([p0, p1], 0.1)  # with a large margin, both typed "luck" the fastest
    [['What', 'great', 'luck'], ['great', 'luck']]
    >>> p2 = [word_time('START', 0), word_time('What', 0.2), word_time('great', 0.3), word_time('luck', 0.6)]
    >>> fastest_words([p0, p1, p2])
    [['What'], [], ['What', 'great', 'luck']]
    """
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    abs_times = list()
    output_list = list()
    for player in word_times:
        player_times = list()
        output_list.append(list())
        for i in range(n_words):
            player_times += [elapsed_time(player[i + 1]) - elapsed_time(player[i])]
        abs_times += [player_times]
    # print(abs_times)
    sorted_by_words = list()
    for i in range(n_words):
        sorted_by_words.append([word_time[i] for word_time in abs_times])
    # print(sorted_by_words)
        min_time = min(sorted_by_words[i])
        for player_num in range(n_players):
            if sorted_by_words[i][player_num] <= (min_time + margin):
                sorted_by_words[i][player_num] = 1
            else:
                sorted_by_words[i][player_num] = 0
    
    for word_pos in range(n_words):
        for player_num in range(n_players):
            if sorted_by_words[word_pos][player_num] == 1:
                output_list[player_num].append(word(word_times[player_num][word_pos + 1]))
    # print(output_list)
    return output_list
    # END PROBLEM 9




def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)