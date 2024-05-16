from collections import Counter
import bisect

"""
課題1. 与えられた文字列のAnagramを辞書ファイルから探して返すプログラムを作る
    1. 自分で何個かテストケースを作って、プログラムが動くか確認
"""

def find_anagrams(random_word, dictionary_file):
    """
    与えられた単語のアナグラムを辞書ファイルから探して返す

    Args:
        random_word (str): アナグラムを探したい単語
        dictionary_file (str): 辞書ファイルのパス

    Returns:
        list: アナグラムのリスト
    """
    sorted_random_word = ''.join(sorted(random_word.lower()))

    # 辞書ファイルから単語を読み込む
    with open(dictionary_file) as f:
        dictionary = [word.strip().lower() for word in f.readlines()]

    new_dictionary = []
    for word in dictionary:
        sorted_word = ''.join(sorted(word))
        new_dictionary.append((sorted_word, word))

    # リストを一番目の要素(ソートされた単語)でソート
    new_dictionary.sort(key=lambda x: x[0])

    anagrams = []
    # 36行目が少しわかりづらい
    # https://www.google.com/url?sa=j&url=https%3A%2F%2Fdocs.python.org%2Fja%2F3%2Flibrary%2Fbisect.html&uct=1705057231&usg=KoZlBsGHfkKHKzYXmrjoopUDvbQ.&opi=76390225&source=meet
    # 一つ目だけで比較するように明示する -> key specifies a key function of one argument that is used to extract a comparison key from each element in the array. To support searching complex records, the key function is not applied to the x value.
    # 関数？いまいち、どうやって明示するかわからなかったからあとでもうちょっと見る
    # ハッシュテーブルを使うともっと早くなる
    idx = bisect.bisect_left(new_dictionary, (sorted_random_word, ''))
    if idx < len(new_dictionary) and new_dictionary[idx][0] == sorted_random_word:
        # 見つかった位置から、アナグラムのリストを作成
        while idx < len(new_dictionary) and new_dictionary[idx][0] == sorted_random_word:
            anagrams.append(new_dictionary[idx][1])
            idx += 1

    return anagrams

dictionary_file = "dictionary.txt"

# テストケース1 (簡単なケース)
word1 = "item"
anagrams1 = find_anagrams(word1, dictionary_file)
print(f"単語 '{word1}' のアナグラム:")
print(anagrams1)

# テストケース2 (複数のアナグラムがある場合)
word2 = "listen"
anagrams2 = find_anagrams(word2, dictionary_file)
print(f"\n単語 '{word2}' のアナグラム:")
print(anagrams2)

# テストケース3 (アナグラムが見つからない場合)
word3 = "hello"
anagrams3 = find_anagrams(word3, dictionary_file)
print(f"\n単語 '{word3}' のアナグラム:")
print(anagrams3)

# テストケース4 (短い単語の場合)
word4 = "a"
anagrams4 = find_anagrams(word4, dictionary_file)
print(f"\n単語 '{word4}' のアナグラム:")
print(anagrams4)

# テストケース5 (長い単語の場合)
word5 = "electroencephalographically"
anagrams5 = find_anagrams(word5, dictionary_file)
print(f"\n単語 '{word5}' のアナグラム:")
print(anagrams5)

# テストケース6 (空の文字列が与えられた場合)
word6 = ""
anagrams6 = find_anagrams(word6, dictionary_file)
print(f"\n単語 '{word6}' のアナグラム:")
print(anagrams6)