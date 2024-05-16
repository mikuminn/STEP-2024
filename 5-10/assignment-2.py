import bisect
import sys
from collections import Counter
from score_checker import calculate_score, read_words, WORDS_FILE


def find_anagrams(random_word, dictionary_file):
    """
    与えられた単語のアナグラムを辞書ファイルから探して返す
    
    Args:
        random_word (str): アナグラムを探したい単語
        dictionary_file (str): 辞書ファイルのパス
    
    Returns:
        list: アナグラムのリスト
    """
    random_word_counter = Counter(random_word.lower())
    
    anagrams = []
    
    # 辞書ファイルから単語を読み込む
    with open(dictionary_file) as f:
        for word in f:
            word = word.strip().lower()
            word_counter = Counter(word)
            if all(count <= random_word_counter[char] for char, count in word_counter.items()):
                anagrams.append(word)
    
    return anagrams

def find_max_score_anagrams(word, anagrams):
    """
    アナグラムの中から最大スコアの単語を見つける
    
    Args:
        word (str): 元の単語
        anagrams (list): アナグラムのリスト
    
    Returns:
        list: 最大スコアのアナグラム
    """
    max_score = 0
    max_score_anagrams = []
    
    for anagram in anagrams:
        score = calculate_score(anagram)
        if score > max_score:
            max_score = score
            max_score_anagrams = [anagram]
        elif score == max_score:
            max_score_anagrams.append(anagram)
    
    return max_score_anagrams

    
def main(data_file):
    answer_file = f"{data_file.split('.')[0]}_answer.txt"
    valid_words = read_words(WORDS_FILE)
    data_words = read_words(data_file)
    
    with open(answer_file, "w") as f:
        for word in data_words:
            anagrams = find_anagrams(word, WORDS_FILE)
            max_score_anagrams = find_max_score_anagrams(word, anagrams)
            if max_score_anagrams:
                max_score = calculate_score(max_score_anagrams[0])
                f.write(f"{max_score_anagrams[0]}\n")
            else:
                f.write("No valid anagram found.\n")
    
    print(f"Output written to {answer_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 assignment-2.py data_file")
        exit(1)
    main(sys.argv[1])