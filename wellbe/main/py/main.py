from searching_algorithm import ProductsSearching
import pandas as pd
import os

# ProductsSearching('комплекс витаминов для мужчин')
# ProductsSearching('муsdagadfgfsAAGDHFSGтамины')
p =ProductsSearching('витамины для детей').return_products()
print()
for e in p:
    if e['name'] == "YumV's,бузина,витамины C и D,тройная защита,ягодный вкус,25 мкг (1000 МЕ),60 жевательных мармеладок":
        print(e)
    if e['name'] == "Natural Factors,Big Friends,жевательный витамин D3,ягодный вкус,10 мкг,250 жевательных таблеток":
        print(e)
        # for key, value in e.items():
        #     print(key, "__ : __", value)
# ProductsSearching('мультивитамины для детей')
#
# ProductsSearching('Pure Essence')
# ProductsSearching('витамины для женщин')

# df.set_index('name', inplace=True)
# print(df.loc['Zhou Nutrition,K2 + D3,клубника,60 жевательных таблеток']['category'].split('\n'))


# def create_csv():
#     df = pd.read_csv('wellbe/main/py/data/products.csv')['brand']
#     arr = []
#     for e in df:
#         e = e.strip()
#         if e not in arr:
#             arr.append(e.replace(' ', ' '))
#     a = pd.DataFrame(columns=['brand'], data=arr)
#     a.to_csv('iherb_brands.csv')
#     print(a)


# user_request = 'комплекс витаминов для мужчин'
# new_cat = ['MegaFood,комплекс витаминов и микроэлементов для женщин старше 55 лет,для приема один раз в день,120 таблеток',
#               'MegaFood,Multi for Men 40+,комплекс витаминов и микроэлементов для мужчин старше 40 лет,60 таблеток',
#               'Emerald Laboratories,коферментный мультивитаминный комплекс для мужчин старше 45 лет для приема 1 раз в день,60 вегетарианских капсул',
#               'MegaFood,Multi for Men 55+,комплекс витаминов и микроэлементов для мужчин старше 55 лет,120 таблеток',
#               'MegaFood,комплекс витаминов и микроэлементов для мужчин,120 таблеток']
# split_request = user_request.lower().split()
# ratios = {}
# product_name = None
# for a in new_cat:
#     categories = a.split(',')
#     if ratios is None:
#         ratios = {}
#
#     # ----------------------------------------------
#
#     split_request = user_request.lower().split()
#     for category in categories:
#         new_ratios = {}
#         for name in split_request:
#             category_words = category.split()
#             if product_name is None:
#                 strip_category = category.strip()
#             else:
#                 strip_category = product_name
#             for word in category_words:
#                 category_ratio = lev.ratio(name, word.lower())
#                 if category_ratio > 0.7:
#                     if category_ratio >= 0.85:
#                         category_ratio = 2 * category_ratio
#                     if strip_category in new_ratios.keys():
#                         new_ratios[category] += category_ratio
#                     else:
#                         new_ratios[category] = category_ratio
#         if len(new_ratios) != 0:
#             max_ratio = max(new_ratios, key=new_ratios.get)
#             ratios[a] = new_ratios[max_ratio]
# print(ratios)
# a = dict(sorted(ratios.items(), key=operator.itemgetter(1), reverse=True))
#
# print(8 * '-' + user_request + 8 * '-', end='\n')
# print()
# for key, value in a.items():
#     print(key, '=' * 5 + '>', value)
