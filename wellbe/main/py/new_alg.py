import mysql.connector
import operator
import os
from collections import OrderedDict
from sklearn.linear_model import LinearRegression
import pandas as pd
import Levenshtein as lev


class ProductsSearching:
    def __init__(self, user_request):
        print(8 * '-' + user_request + 8 * '-', end='\n')

        self.user_request = user_request

    def get_product_info(self):
        # names_ratio = self.get_names(df.index)
        names_ratio = self.get_names()
        categories_ratio = self.get_categories(self.user_request)
        if names_ratio[2] is False and categories_ratio[2] is False:
            brands_ratio = self.get_brands(self.user_request)
            if brands_ratio[2] is False:
                return False
            else:
                return brands_ratio[0], 'brand'
        else:
            if names_ratio[2] is True and categories_ratio[2] is False:
                return names_ratio[0], names_ratio[-1]
            elif names_ratio[2] is False and categories_ratio[2] is True:
                return categories_ratio[0], 'category'
            else:
                # print(names_ratio, categories_ratio)

                if names_ratio[1] >= categories_ratio[1]:
                    return names_ratio[0], names_ratio[-1]
                else:
                    return categories_ratio[0], 'category'

    def get_names(self):
        global df
        column = df['name']
        user_request = self.user_request
        ratios = {}
        brands_name_dict = {}
        categories_name_dict = {}

        for cell_name in column:

            if type(cell_name) is float:
                continue

            cell_split = cell_name.strip().split(', ')
            # cell_split = cell_name.replace(', ', '').strip().split(',')

            brand = cell_split[0]
            brand_ratio = lev.ratio(brand.lower(), user_request.lower())
            if brand_ratio > 0.68:
                if brand_ratio >= 0.9:
                    ratios[brand] = len(user_request.split())
                else:
                    ratios[brand] = brand_ratio
                brands_name_dict[brand] = cell_name

            categories = cell_split[1::]
            categories_name_dict = self.calculate_category_ratio(user_request=user_request, ratios=ratios, categories=categories, product_name=cell_name)
            ratios |= categories_name_dict
        try:
            max_ratio = max(ratios, key=ratios.get)
            if max_ratio in brands_name_dict:
                return df.loc[df['name'] == max_ratio]['brand'].item(), ratios[max_ratio], True, 'brand'

            elif max_ratio in categories_name_dict:
                ratio_dict = self.calculate_category_ratio(user_request=user_request, categories=df.loc[df['name'] == max_ratio]['category'].item().split(','))
                max_cat_ratio = max(ratio_dict, key=ratio_dict.get)
                return max_cat_ratio, ratios[max_ratio], True, 'category'
            else:
                return '', 0, False
        except ValueError:
            return '', 0, False

    def get_categories(self, user_request):
        request_split = user_request.split()
        for word in request_split:
            if 0.85 <= lev.ratio('витамин', word.lower()) <= 1:
                user_request = self.__change_vitamin_letter(user_request).lower()
                break

        ratios = {}
        ratios = self.calculate_category_ratio(user_request=user_request, ratios=ratios, coefficient=3)
        try:
            max_ratio = max(ratios, key=ratios.get)
            if 0 <= ratios[max_ratio] < len(request_split):
                return max_ratio, ratios[max_ratio], False
            return max_ratio, ratios[max_ratio], True
        except ValueError:
            return '', 0, False

    @staticmethod
    def calculate_category_ratio(user_request,
                                 ratios=None,
                                 categories=None,
                                 product_name=None,
                                 coefficient=2):

        if categories is None:
            categories = pd.read_csv(os.path.join(os.path.dirname(__file__), 'iherb_categories.csv'), index_col='category').index

        if ratios is None:
            ratios = {}
        split_request = user_request.lower().split()
        name_strip = ''
        for category in categories:
            new_ratios = {}
            for name in split_request:
                category_words = category.split()
                if product_name is None:
                    name_strip = category.strip()
                else:
                    name_strip = product_name.strip()
                for word in category_words:
                    category_ratio = lev.ratio(name, word.lower())
                    if category_ratio > 0.65:
                        if category_ratio >= 0.9:
                            category_ratio = coefficient * category_ratio
                        if category in new_ratios.keys():
                            new_ratios[category] += category_ratio
                        else:
                            new_ratios[category] = category_ratio

            if len(new_ratios) != 0 and new_ratios[category] <= coefficient * len(split_request):
                max_ratio = max(new_ratios, key=new_ratios.get)
                ratios[name_strip] = new_ratios[max_ratio]
        return ratios

    @staticmethod
    def get_brands(user_request):
        global df
        # brand_df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'iherb_brands.csv'), index_col='brand').index
        brand_df = df['brand']
        ratios = {}
        for brand in brand_df:
            brand_ratio = lev.ratio(user_request.lower(), brand.lower())
            ratios[brand] = brand_ratio
        try:
            max_ratio = max(ratios, key=ratios.get)
            if 0 <= ratios[max_ratio] < 0.45:
                return max_ratio, ratios[max_ratio], False
            return max_ratio, ratios[max_ratio], True
        except ValueError:
            return '', 0, False

    @staticmethod
    def __change_vitamin_letter(user_request):
        vitamin_word = ''
        for word in user_request.split():
            if 0.8 <= lev.ratio('витамин', word) <= 1:
                vitamin_word = word
        user_request = user_request.replace(vitamin_word, '_____').upper().replace('Ц', 'С').replace('C', 'С').replace('A', 'А') \
            .replace('E', 'Е').replace('K', 'К').replace('В', 'B').replace('Д', 'D').replace('_____', vitamin_word)
        return user_request


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="2002",
)

try:
    with db.cursor(buffered=True) as cursor:
        cursor.execute('use wellbe;')
        df = pd.read_sql('select * from product', db, index_col='id')

        cursor.execute('select id from product')
        product_id = [e[0] for e in cursor.fetchall()]
        for new_id in product_id:
            cursor.execute(f'select name from category where product_id = {new_id}')
            categories2 = set([e[0] for e in cursor.fetchall()])
            df = df.assign(category=','.join(categories2))
            df.loc[new_id, 'name'] = df.loc[new_id, 'name'].strip()
        cursor.close()
except Exception as e:
    print(e)


def calculate_linear_regression():
    global df
    new_df = df.drop(['brand', 'category', 'size_type', 'link', 'stock_status', 'rating', 'name', 'Y'], axis=1)

    with db.cursor() as cur:
        for prod_id in new_df.index:
            prod = new_df.loc[prod_id, :]
            try:
                prod = prod.to_frame().T
            except Exception:
                pass
            cur.execute(f'update product set Y = {reg.predict(prod.drop(["reviews_count"], axis=1))[0][0]} where id = {prod_id};')
            db.commit()
        cur.close()


train_data = df.drop(['brand', 'category', 'size_type', 'link', 'stock_status', 'rating', 'name', 'Y'], axis=1)

X = pd.DataFrame(train_data.drop(['reviews_count'], axis=1))
y = pd.DataFrame(train_data['reviews_count'])

reg = LinearRegression().fit(X, y)
# calculate_linear_regression()
