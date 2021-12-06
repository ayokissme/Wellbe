import operator
import os
from collections import OrderedDict
from sklearn.linear_model import LinearRegression
import pandas as pd
import Levenshtein as lev


class ProductsSearching:
    def __init__(self, user_request):
        self.user_request = user_request
        # print(8 * '-' + self.user_request + 8 * '-', end='\n')

    def return_products(self):
        best_products = self.get_best_products()
        if best_products is None:
            return None
        else:
            products_list = list(best_products.items())
            result = []
            categories = []
            brands = []
            for product in products_list:
                product_info = df.loc[product[0]]
                product_category = []
                prod_shape = product_info.shape

                """ Вывод продуктов с одинаковыми именами """
                if prod_shape[0] > 1 and len(prod_shape) > 1:
                    # print(prod_shape)
                    continue

                try:
                    product_category = product_info['category'].replace(', ', '_').split(',')
                    [categories.append(e.replace('_', ', ')) for e in product_category if e.replace('_', ', ') not in categories]
                    product_category = [e.replace('_', ', ') for e in product_category]
                except Exception:
                    pass
                try:
                    brand = product_info['brand']
                    if brand not in brands:
                        brands.append(brand)
                except Exception:
                    pass

                result.append({
                    'name': product[0],
                    'price': product_info['price'],
                    'rating': product_info['rating'],
                    'reviews': product_info['reviews_count'],
                    'link': product_info['link'],
                    'category': product_category,
                    'brand': product_info['brand'],
                })
            return result, categories, brands

    @staticmethod
    def is_digit(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def get_best_products(self):
        df_info = self.__filter_database()

        if df_info is False:
            return None
        else:
            filtered_df = df_info.drop(['brand', 'category', 'size_type', 'link', 'stock_status'], axis=1)
            products = OrderedDict()
            for product in filtered_df.index:
                prod = filtered_df.loc[product, :]
                try:
                    prod = prod.to_frame().T
                except Exception:
                    pass
                products[product] = reg.predict(prod.drop(['reviews_count'], axis=1))[0][0]
            return dict(sorted(products.items(), key=operator.itemgetter(1), reverse=True))

    def __filter_database(self):
        product_info = self.__get_product_info()
        if product_info is False:
            return False
        else:
            return df.loc[df[product_info[1]].str.contains(product_info[0], na=False)]

    def __get_product_info(self):
        names_ratio = self.get_names(df.index)
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
                # ratios_dict = {
                #     names_ratio[0]: lev.ratio(self.user_request.lower(), names_ratio[0].lower()),
                #     categories_ratio[0]: lev.ratio(self.user_request.lower(), categories_ratio[0].lower())
                # }

                # a = self.calculate_category_ratio(self.user_request, categories=ratios_dict)
                # print(a, '-' * 8)
                # print(ratios_dict)
                print(names_ratio, categories_ratio)

                if names_ratio[1] >= categories_ratio[1]:
                    return names_ratio[0], names_ratio[-1]
                else:
                    return categories_ratio[0], 'category'

    def get_names(self, column):
        user_request = self.user_request
        ratios = {}
        brands_name_dict = {}
        categories_name_dict = {}
        for cell_name in column:
            if type(cell_name) is float:
                continue

            cell_split = cell_name.replace(', ', '').strip().split(',')

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
                return df.loc[max_ratio]['brand'], ratios[max_ratio], True, 'brand'

            elif max_ratio in categories_name_dict:
                ratio_dict = self.calculate_category_ratio(user_request=user_request, categories=df.loc[max_ratio]['category'].split(','))
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
    def calculate_category_ratio(
            user_request,
            ratios=None,
            categories=pd.read_csv(os.path.join(os.path.dirname(__file__), 'iherb_categories.csv'),
                                   index_col='category').index,
            product_name=None,
            coefficient=2):
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

            # if a == 1:
            #     print(new_ratios)
            if len(new_ratios) != 0 and new_ratios[category] <= coefficient * len(split_request):
                max_ratio = max(new_ratios, key=new_ratios.get)
                ratios[name_strip] = new_ratios[max_ratio]
        return ratios

    @staticmethod
    def get_brands(user_request):
        brand_df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'iherb_brands.csv'), index_col='brand').index
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


dirname = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(dirname, 'products.csv'), index_col='name')

train_data = df.drop(['brand', 'category', 'size_type', 'link', 'stock_status'], axis=1)

X = pd.DataFrame(train_data.drop(['reviews_count'], axis=1))
y = pd.DataFrame(train_data['reviews_count'])

reg = LinearRegression().fit(X, y)
