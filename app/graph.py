from app.models import Card


class Graph:
    def __init__(self, user):
        self.user = user
        self.cards = Card.query.filter_by(payer=user).all()

    def get_data_plot_days(self, month, year):
        data = {}
        for card in Card.query.filter_by(payer=self.user, month=month, year=year).all():
            if card.day not in data:
                data[card.day] = card.price
            else:
                data[card.day] += card.price
        sorted_list = list(data.items())
        sorted_list.sort(key=lambda x: x[0])
        days = [d[0] for d in sorted_list]
        prices = [d[1] for d in sorted_list]
        return days, prices

    def get_data_plot_cat(self, month):
        data = {}
        for card in Card.query.filter_by(payer=self.user, month=month).all():
            if card.category not in data:
                data[card.category] = card.price
            else:
                data[card.category] += card.price
        categories = [d[0] for d in data.items()]
        prices = [d[1] for d in data.items()]
        return categories, prices
