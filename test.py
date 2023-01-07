from main import *


def top_test(words):
    print('Test of getting a word content is being done.....')
    if test_get_word_content(words):
        print('Test of getting a word content completed!')
    else:
        print('Test of getting a word content failed!')
        return False
    print('Test of getting a word is being done.....')
    if test_get_word(words):
        print('Test of getting a word completed!')
    else:
        print('Test of getting a word failed!')
        return False
    print('Test of getting a hom tags is being done.....')
    if test_get_hom_tags(words):
        print('Test of getting a hom tags completed!')
    else:
        print('Test of getting a hom tags failed!')
        return False


def test_get_word_content(words):
    for word in words:
        try:
            soup = get_soup(word)
            if soup is None:
                print(f'Test failed: word {word} was not found')
                return False
            try:
                word_content = get_word_contents(soup)
            except AttributeError:
                print(f'Test failed on word {word}')
                return False
        except UnboundLocalError:
            print(f'Test failed on word {word}')
            print('Test failed: did not manage to get soup')
            return False
    return True


def test_get_word(words):
    for word in words:
        soup = get_soup(word)
        word_content = get_word_contents(soup)
        try:
            get_word(word_content)
            print(get_word(word_content))
        except IndexError:
            print(f'Test failed on word {word}: word_contents is empty')
            return False
        except AttributeError:
            print(f'Test failed on word {word}: did not manage to get word')
            return False
    return True


def test_get_hom_tags(words):
    for word in words:
        soup = get_soup(word)
        word_contents = get_word_contents(soup)
        try:
            hom_tags = get_hom_tags(word_contents)
            hom_tags_number = sum(1 for _ in hom_tags)
            expected_number = hom_tags_expected[words.index(f'{word}')]
            if hom_tags_number != expected_number:
                print(f'Test failed on word {word}: expected {expected_number}, got {hom_tags_number}')
                return False
        except AttributeError:
            print(f'Test failed on word {word}')
            return False
    return True


if __name__ == '__main__':
    words_ = ['obituary', 'i', 'love', 'black', 'oxen', 'playing', 'trees', 'to', 'prompt',
              'something', 'went', 'more', 'fodgel', 'go', 'is',
              'be', 'come across', 'went away', 'charity shop',
              'teddy bear', 'long face', 'never mind', 'elevator']
    hom_tags_expected = [1, 2, 13, 10, 1, 1, 1, 25, 4, 8, 1, 10, 1, 33, 1, 16, 2, 2, 1, 1, 1, 2, 1]
    sense_tags_expected = [2, 13, 10, 1, 2, 1, 25, 5, 8, 1, 10, 1, 33, 1, 16, 2, 2, 1, 1, 1, 2, 1]
    top_test(words_)
