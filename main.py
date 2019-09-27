import json
import operator
from pprint import pprint
import xml.etree.ElementTree as ET

tree = ET.parse('newsafr.xml')
root = tree.getroot()

with open('newsafr.json', encoding='utf-8') as file:
    json_data = json.load(file)

def collect_word_in_news_json(data):
    """
    Собираем слова из новостей JSON в список
    :return:
    """
    words_collection = []
    top_words = []
    for news in data['rss']['channel']['items']:
        words_collection = news['description'].split()
        for word in words_collection:
            if len(word) > 5:
                top_words.append(word.lower())
    top_words.sort()
    return top_words

def collect_word_in_news_xml(root):
    """
    Собираем слова из новостей XML в список
    :return:
    """
    news_text_list = []
    xml_items = root.findall('channel/item')
    for item in xml_items:
        news_text_list += item.find('description').text.split()
    top_words = []
    for word in news_text_list:
        if len(word) > 5:
            top_words.append(word.lower())
    top_words.sort()
    return top_words

def which_word_is_more_frequency(top_words):
    """
    Определяем какое слово самое частое
    :param top_words:
    :return: top_10
    """
    count = 1
    top_words_dict = {}
    checkword = top_words[0]
    for word in top_words:
        if word == checkword:
            count += 1
            top_words_dict[word] = count
        else:
            checkword = word
            count = 1
    top_words_dict_sorted = sorted(top_words_dict.items(), key=operator.itemgetter(1), reverse=True)
    return top_words_dict_sorted

def print_10_words(top_words_dict):
    """
    Печать 10 самых часто используемых слов
    :param top_words_dict:
    :return:
    """
    print("Печать 10 самых часто используемых слов в новостях в порядке убывания")
    count = 0
    while count != 10:
        pprint(top_words_dict[count])
        count += 1

print("Работаем с файлом JSON")
top_words = collect_word_in_news_json(json_data)
top_words_dict = which_word_is_more_frequency(top_words)
print_10_words(top_words_dict)

print("Работаем с файлом XML")
top_words2 = collect_word_in_news_xml(root)
top_words_dict2 = which_word_is_more_frequency(top_words2)
print_10_words(top_words_dict2)


