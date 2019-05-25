import calendar
from app.charts import bp
from app.charts.forms import *
from app.graph import Graph
from flask import redirect, url_for, render_template
from flask_login import login_required, current_user


def _calendar_month(args):
    return [calendar.month_name[i] for i in args]


@bp.route('/graphics', methods=['GET', 'POST'])
@login_required
def graphics():
    forms = [DaysLineForm(), MonthCategoryForm(), CategoryForm(), MonthLineForm(), CategoryMonthForm()]

    forms_dict = {
        forms[0]: ('charts.graph_days_line', {
            'month': forms[0].month_days.data,
            'year': forms[0].year_days.data
        }),
        forms[1]: ('charts.graph_category_bar', {
            'month': forms[1].month_category.data,
            'year': forms[1].year_category.data
        }),
        forms[2]: ('charts.graph_month_hbar', {
            'category': forms[2].category.data,
            'year': forms[2].year.data
        }),
        forms[3]: ('charts.graph_month_line', {
            'year': forms[3].year_line.data
        }),
        forms[4]: ('charts.graph_category_month', {
            'category': forms[4].category.data,
            'month': forms[4].month.data,
            'year': forms[4].year_category.data
        })
    }

    for form in list(forms_dict.keys()):
        if form.validate_on_submit():
            return redirect(url_for(forms_dict[form][0], **forms_dict[form][1]))

    return render_template('graph.html',
                           form1=forms[0], form2=forms[1], form3=forms[2],
                           form4=forms[3], form5=forms[4])


@bp.route('/days/<month>/<year>', methods=['GET'])
@login_required
def graph_days_line(month, year):
    chart = Graph(current_user)
    filter_dict = {'month': int(month), 'year': year, 'payer': current_user}
    days, prices = chart.days(**filter_dict)
    return render_template('graph_days_line.html', days=days, prices=prices, month=_calendar_month([int(month)]))


@bp.route('/month/<year>', methods=['GET'])
@login_required
def graph_month_line(year):
    chart = Graph(current_user)
    month, prices = chart.month(year)
    month = _calendar_month(month)
    return render_template('graph_month_line.html', month=month, prices=prices)


@bp.route('/categories/<month>/<year>', methods=['GET'])
@login_required
def graph_category_bar(month, year):
    chart = Graph(current_user)
    categories, prices = chart.categories(int(month), year)
    return render_template('graph_categories_bar.html',
                           cat=categories, prices=prices,
                           month=_calendar_month([int(month)]))


@bp.route('/category/<category>/<year>', methods=['GET'])
@login_required
def graph_month_hbar(category, year):
    chart = Graph(current_user)
    month, prices = chart.category_per_month(category, year)
    month = _calendar_month(month)
    return render_template('graph_categories_hbar.html', month=month, prices=prices, category=category)


@bp.route('/<category>/<month>/<year>', methods=['GET'])
def graph_category_month(category, month, year):
    chart = Graph(current_user)
    filter_dict = {'category': category, 'month': month, 'year': year}
    days, prices = chart.category_per_day(**filter_dict)
    return render_template('graph_category_per_day.html', days=days, prices=prices, category=category)
