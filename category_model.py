import json


class CategoryModel:
    title = ""
    subCategories = {}
    regularExpression = []

    def to_json(self, y: dict):
        self.title = y.get("title")
        self.subCategories = {}
        self.regularExpression = y.get("regularExpression")
        for subCategory in y["subCategories"]:
            self.subCategories[subCategory] = 0

    def __str__(self):
        return f'CategoryModel( title: {self.title} ,Regular expression: {self.regularExpression} ,subCategories: {self.subCategories.__str__()})'
        # return "CategoryModel(""title: " + self.title + ', Regular expression: ' + self.regularExpression + ", subCategories: " + self.subCategories.__str__()


file = open('category.json', "r",encoding='utf-8')

y: dict = json.loads(file.read())

categories = []
for currentCategory in y.get('categories'):
    category = CategoryModel()
    category.to_json(currentCategory)
    categories.append(category)

file.close()
# res = []
# src = 'this word is a big word man how many words are there?'
# sub = 'word'
# pos = 'this word is a big word man how many words are there?'.find(sub)
# while pos != -1:
#     res.append(pos)
#     pos = src.find(sub, pos + 1)
# print(res)
# print(pos)