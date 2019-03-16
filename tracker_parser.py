from bs4 import BeautifulSoup
from pprint import pprint
import json
from lxml import etree

tracker = 'Трекер.html'

def first_parser(tracker):
    """
    Функция, которая парсит html-файл при помощи костылей и выдает два вида массивов с категориями
    :param tracker: html-файл страницы торрента
    :return: subcats - массив разложенных в словари категорий и подкатегорий, labels_text - массив подкатегорий
    """
    delimiter = '---'
    work_str = ''
    titles = []
    subcats = {}
    categories_object = {}


    # открываем на чтение html-файл
    with open(tracker, 'r') as t:
        soup = BeautifulSoup(t.read(), 'lxml')
        select = soup.find('select', {'id': 'fs-main'})

        # получаем список разделов
        select_text = select.findAll('optgroup')
        dirt_text = [str(tag)[:49] for tag in select_text]
        for i in dirt_text:
            begin = i.find('" ') + 2
            end = i.find('">')
            i = i[begin:end]
            titles.append(i)
        with open('titles_list.json', 'w', encoding='utf-8') as f:
            json.dump(titles, f, ensure_ascii=False, indent=2)

        # извлекаем весь текст из категорий и раскладываем по массивам внутри массива
        labels = select.find_all('optgroup', {'label': re.compile('\w{4,}')})
        labels_text = [l.text for l in labels]
        # Текст категорий сохраняем в JSON
        with open('categories_list.json', 'w', encoding='utf-8') as f:
            json.dump(labels_text, f, ensure_ascii=False, indent=2)

        # для каждого массима получаю название категории, которое является первым элементом массива
        for label in labels_text:
            name = label.split('\xa0\n')[0].replace('\n', '')
            cts = label.split('\xa0\n')[1:]
            # создаем копию списка категорий
            copy_cts = cts
            # из копии списка категорий добавляем в словарь категории, которые не содержат подкатегорий или
            # обрезаем подкатегории и добавляем без них
            try:
                for c in copy_cts:
                    if not c.startswith(' |- '):
                        i = copy_cts.index(c)
                        copy_cts = copy_cts[:i]
                        pure_copy_cts = [i.replace(' |- ', '') for i in copy_cts]
                        subcats[name.replace(' |- ', '')] = pure_copy_cts
            except:
                pass

            # оставляем в списке категорий подкатегории, раскладываем их и добавляем в словарь категорий
            for c in cts:
                if not c.startswith(' |- '):
                    # склеиваем строку из обрезанного списка категорий, добавляя метку перед названиями подкатегорий
                    position = cts.index(c)
                    work_cts = cts[position:]
                    for w in work_cts:
                        if not w.startswith(' |- '):
                            work_str += delimiter + str(w)
                        else:
                            work_str += str(w)

                # разбиваем строку на подкатегории по метке
                cat_clusters = work_str.split('---')
                sort_clusters = []

                # сортируем подкатегории
                for cluster in cat_clusters:
                    if cluster in sort_clusters:
                        pass
                    if cluster == '':
                        pass
                    sort_clusters.append(cluster)

                # раскладываем подкатегории в словарь
                for cluster in sort_clusters:
                    if cluster == '':
                        sort_clusters.remove(cluster)
                    subcat_name = cluster.split(' |- ')[0]
                    subcat_subcat = cluster.split(' |- ')[1:]
                    if subcat_name == '' and subcat_subcat == '':
                        pass
                    elif subcat_name == '':
                        pass
                    elif subcat_name in subcats:
                        pass
                    else:
                        subcats[subcat_name] = subcat_subcat
        # сохраняем разложенные подкатегории в JSON
        with open('categories_dict.json', 'w', encoding='utf-8') as f:
            json.dump(subcats, f, ensure_ascii=False, indent=2)

    return subcats, labels_text

first_parser(tracker)









