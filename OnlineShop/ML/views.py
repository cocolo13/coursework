from django.shortcuts import render
import joblib as jb
import pandas as pd
import numpy as np
from ProductFeed.models import *
from sklearn.preprocessing import LabelEncoder


class MyRecSystem:
    def __init__(self):
        self.data = None
        self.vector = None

    def fit(self, X):
        self.data = X

    def predict(self, index_obj):
        assert (self.data is not None), "Сначала нужно вызвать метод fit"
        for j in range(len(self.data)):
            if self.data[j][3] == index_obj:
                self.vector = self.data[j]
        all_obj = []
        for i in range(len(self.data)):
            if self.data[i][3] != index_obj:
                cur_dist = self.cos_dist(np.delete(self.vector, 3), np.delete(self.data[i], 3))
                all_obj.append([cur_dist, self.data[i][3]])
        all_obj.sort()
        return all_obj

    def cos_dist(self, x, y) -> float:
        cosine_similarity = np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
        return cosine_similarity


def create_data_frame(feed_id):
    cur_feed = Clothes.objects.get(pk=feed_id)
    gender = cur_feed.gender
    not_needed_pks = Clothes.objects.exclude(gender=gender).values_list('pk', flat=True)
    all_feed = Clothes.objects.all()
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
    all_fields.remove("gender")
    all_fields.remove("count_in_stock")
    all_fields.remove("Baskets_feeds+")
    all_fields.remove("baskets")

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
    df["cost"] = df["cost"].astype(float)
    df["by_count"] = df["by_count"].astype(int)
    for index, row in df.iterrows():
        if row["id"] in not_needed_pks and row["id"] != feed_id:
            df.drop(index, inplace=True)
    return df


def preprocessing(feed_id):
    df = create_data_frame(feed_id)
    for col in df.columns:
        if df[col].dtype == "object" and col != "id":
            encoder = LabelEncoder()
            encoder.fit(df[col])
            df[col] = encoder.transform(df[col])
    model = MyRecSystem()
    model.fit(df.to_numpy())
    p = model.predict(feed_id)[:5]
    ans = [t[1] for t in p]
    return ans
