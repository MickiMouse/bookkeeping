from app.models import Card


class CardResponse:
    def __init__(self, user, **kwargs):
        self.user = user
        self.cards = Card.query.filter_by(payer=self.user, **kwargs).all()
        self.data = {}

    def transform_data(self, idx_key):
        sorted_list = list(self.data.items())
        sorted_list.sort(key=lambda x: x[idx_key])
        xAxis = [d[0] for d in sorted_list]
        yAxis = [d[1] for d in sorted_list]
        return xAxis, yAxis

    def get_cards(self, key):
        for card in self.cards:
            attr = getattr(card, key)
            if attr not in self.data and not card.kind:
                self.data[attr] = card.price
            elif not card.kind:
                self.data[attr] += card.price
        return self.transform_data(0)

    def get_expenses_month(self, **kwargs):
        months = range(1, 13)
        for month in months:
            cards = Card.query.filter_by(payer=self.user, month=month, **kwargs).all()
            if len(cards) == 0:
                self.data[month] = 0
            else:
                for card in cards:
                    if card.month not in self.data:
                        self.data[card.month] = card.price
                    else:
                        self.data[card.month] += card.price
        return self.transform_data(0)
