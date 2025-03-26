from django.shortcuts import render
import joblib as jb
import pandas as pd
import numpy as np
from ProductFeed.models import *
from sklearn.preprocessing import LabelEncoder


class MyRecSystem:
    def __init__(self):
        self.data = None

    def fit(self, X):
        self.data = X

    def predict(self, index_obj):
        assert (self.data is not None), "Сначала нужно вызвать метод fit"

        all_obj = []
        for i in range(len(self.data)):
            if i != index_obj:
                cur_dist = self.cos_dist(self.data[index_obj], self.data[i])
                all_obj.append([cur_dist, i])
        all_obj.sort()
        return all_obj

    def cos_dist(self, x, y) -> float:
        cosine_similarity = np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
        return cosine_similarity


def create_data_frame(feed_id):
    cur_feed = Clothes.objects.get(pk=feed_id)
    g = cur_feed.gender
    all_feed = Clothes.objects.exclude(pk=feed_id).filter(gender=g)

    all_fields = [field.name for field in Clothes._meta.get_fields(include_hidden=True)]
    all_fields.remove("title")
    all_fields.remove("photo")
    all_fields.remove("size")
    all_fields.remove("season")
    all_fields.remove("style")
    all_fields.remove("subcategory")
    all_fields.remove("brand")
    all_fields.remove("country")
    all_fields.remove("Clothes_size+")

    all_seasons = [s.__str__() for s in Seasons.objects.all()]
    all_styles = [s.__str__() for s in Styles.objects.all()]

    df = pd.DataFrame(columns=all_fields)

    for cl in all_feed:
        obj = {}
        for f in all_fields:
            if f[-1] != "+":
                v = getattr(cl, f)
                obj[f] = v
            else:
                new_f = f[f.index("_") + 1:]
                new_f = new_f[:-1]

                all_values = getattr(cl, new_f).all()
                value = []
                for elem in all_values:
                    value.append(elem.__str__())
                if new_f not in ["season", "style"]:
                    obj[f] = str(value[0])
                else:
                    if new_f == "season":
                        for s in all_seasons:
                            obj["season" + s] = int(s in value)
                    else:
                        for st in all_styles:
                            obj["style" + st] = int(st in value)
        new_df = pd.DataFrame([obj])
        df = pd.concat([df, new_df], ignore_index=True)
    df = df.drop(["Clothes_season+", "Clothes_style+"], axis=1)
    df = df.set_index("id")
    df["cost"] = df["cost"].astype(float)
    df["count_in_stock"] = df["count_in_stock"].astype(int)
    df["by_count"] = df["by_count"].astype(int)
    return df


def preprocessing(feed_id):
    df = create_data_frame(feed_id)

    # category_encoder = jb.load("category_encoder.joblib")
    # clothes_brand = jb.load("Clothes_brand+_encoder.joblib")
    # clothes_country = jb.load("Clothes_country+_encoder.joblib")
    # clothes_subcategory = jb.load("Clothes_subcategory+_encoder.joblib")
    # color_encoder = jb.load("color_encoder.joblib")
    # gender_encoder = jb.load("gender_encoder.joblib")
    # is_premium_encoder = jb.load("is_premium_encoder.joblib")

    for col in df.columns:
        if df[col].dtype == "object":
            encoder = LabelEncoder()
            encoder.fit(df[col])
            jb.dump(encoder, f"{col}_encoder.joblib")
            df[col] = encoder.transform(df[col])

    model = MyRecSystem()
    model.fit(df.to_numpy())
    # for col in df.columns:
    #     if df[col].dtype == "object":
    #         encoder = None
    #         if col == "Clothes_subcategory+":
    #             encoder = clothes_subcategory
    #         elif col == "Clothes_country+":
    #             encoder = clothes_country
    #         elif col == "Clothes_brand+":
    #             encoder = clothes_brand
    #         elif col == "category":
    #             encoder = category_encoder
    #         elif col == "color":
    #             encoder = color_encoder
    #         elif col == "is_premium":
    #             encoder = is_premium_encoder
    #         elif col == "gender":
    #             encoder = gender_encoder
    #
    #         df[col] = encoder.transform(df[col])
    # X = df.to_numpy()
    # model.fit(X)
    p = model.predict(feed_id)[:5]
    ans = [t[1] for t in p]
    return ans
