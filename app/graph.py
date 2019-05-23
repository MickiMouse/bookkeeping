from app.models import Card


class Graph:
    def __init__(self, user):
        self.user = user
        self.cards = Card.query.filter_by(payer=user).all()
        self.data = {}

    def transform_data(self, idx_key):
        sorted_list = list(self.data.items())
        sorted_list.sort(key=lambda x: x[idx_key])
        first_array = [d[0] for d in sorted_list]
        second_array = [d[1] for d in sorted_list]
        return first_array, second_array

    def days(self, **kwargs):
        for card in Card.query.filter_by(**kwargs).all():
            if card.day not in self.data:
                self.data[card.day] = card.price
            else:
                self.data[card.day] += card.price
        return self.transform_data(0)

    def month(self, year):
        for card in Card.query.filter_by(payer=self.user, year=year).all():
            if card.month not in self.data:
                self.data[card.month] = card.price
            else:
                self.data[card.month] += card.price
        return self.transform_data(0)

    def categories(self, month, year):
        for card in Card.query.filter_by(payer=self.user, month=month, year=year).all():
            if card.category not in self.data:
                self.data[card.category] = card.price
            else:
                self.data[card.category] += card.price
        return self.transform_data(1)

    def category_per_month(self, category, year):
        for card in Card.query.filter_by(payer=self.user, category=category, year=year).all():
            if card.month not in self.data:
                self.data[card.month] = card.price
            else:
                self.data[card.month] += card.price
        return self.transform_data(0)

    def category_per_day(self, category, month, year):
        for card in Card.query.filter_by(payer=self.user, category=category, month=month, year=year).all():
            if card.day not in self.data:
                self.data[card.day] = card.price
            else:
                self.data[card.day] += card.price
        return self.transform_data(0)

    def get_all_categories(self):
        categories, expenses = [], []
        for card in Card.query.filter_by(payer=self.user):
            if card.category not in self.data:
                self.data[card.category] = card.price
            else:
                self.data[card.category] += card.price

        for elem in list(self.data.items()):
            categories.append(elem[0])
            expenses.append(elem[1])

        return categories, expenses
