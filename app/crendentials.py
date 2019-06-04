def calendar_month(args):
    import calendar
    return [calendar.month_name[i] for i in args]


def get_percents(categories, prices):
    percents = [x / sum(prices) * 100 for x in prices]
    z = [[i, j, k] for i, j, k in reversed(sorted(zip(percents, prices, categories), key=lambda pair: pair[0]))]
    data = [[z[i][2], z[i][1], round(z[i][0], 2)] for i in range(len(z))]

    if len(data) > 5:
        return data[:5]
    else:
        return data


def get_total(cards):
    return round(sum([card.price if card.kind else (-1) * card.price for card in cards]), 2)
