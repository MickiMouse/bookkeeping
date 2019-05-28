def calendar_month(args):
    import calendar
    return [calendar.month_name[i] for i in args]


def get_percents(categories, prices):
    percents = [x / sum(prices) * 100 for x in prices]
    z = [j for i, j in sorted(zip(percents, categories), key=lambda pair: pair[0])]
    percents.sort()
    percents.reverse()
    z.reverse()
    data = ['{} {}%'.format(z[i], round(percents[i], 2)).split(' ') for i in range(len(percents))]

    if len(data) > 5:
        return data[:5]
    else:
        return data


def get_total(cards):
    return round(sum([card.price if card.kind else (-1) * card.price for card in cards]), 2)
