import plotly.express as px
import plotly.graph_objects as go

from database import Couch


def _compare_prices_available_and_on_order():
    """Create graph to compare full prices for couches with 'доступно' and 'под заказ' statuses"""
    prices_available = Couch.get_prices_by_status('доступно')
    prices_on_order = Couch.get_prices_by_status('под заказ')

    fig = go.Figure(go.Histogram(x=prices_available, nbinsx=10, name='Доступные'))
    fig.add_trace(go.Histogram(x=prices_on_order, nbinsx=10, name='Под заказ'))

    fig.update_layout(
        title_text="Сравнение цен и количества для диванов со статусами 'доступно' и 'под заказ'",
        xaxis_title_text='Цена',
        yaxis_title_text='Количество',
    )

    fig.show()


def _show_top_10():
    """Create bar chart for top 10 vendor codes with the highest average price"""
    data = Couch.get_top_10()
    fig = px.bar(data, x='vendor_code', y='average', title='Топ 10 артикулов с самой высокой средней ценой')
    fig.update_layout(
        xaxis_title_text='Артикул',
        yaxis_title_text='Средняя цена',
    )
    fig.show()


def _compare_id_available_and_on_order():
    """Create pie chart for amount of couches with 'доступно' and 'под заказ' statuses (assuming that id is unique)"""
    data = [dictionary for dictionary in Couch.get_count_by_status() if dictionary['status'] in ['доступно', 'под заказ']]

    fig = px.pie(data, values='count', names='status',
                 title="Число уникальных ID для диванов со статусами 'доступно' и 'под заказ'",
                 labels={'count': 'Количество', 'status': 'Статус'}
                 )
    fig.show()


def show_graphs():
    _compare_prices_available_and_on_order()
    _show_top_10()
    _compare_id_available_and_on_order()


if __name__ == '__main__':
    show_graphs()
