import re
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from urllib.parse import parse_qs, urljoin, urlparse

from database import Couch

URL = 'https://azbykamebeli.ru/'
VENDOR_REGEX = re.compile(r'Артикул: (\d+)')
PRICE_REGEX = re.compile(r'[^\d.]')

couch_test_data = """<div class="items-list__item d-flex align-items-end flex-column with-wrap">
<div class="stickers-block">
</div>
<div class="item__image">
<meta content="https://azbykamebeli.ru/upload/uf/698/6983d5a860b0c71e655554ef09697739.jpg?resize=w[384]h[237]f[t]fc[ffffff]" itemprop="image"/>
<a href="/catalog/0000057/940152/?offerId=1058883"><img alt="АРГО-1" class="item__picture img-fluid" src="/upload/uf/698/6983d5a860b0c71e655554ef09697739.jpg?resize=w[384]h[237]f[t]fc[ffffff]"/>
</a>
</div>
<div class="item__description">
<div class="d-flex justify-content-between">
<small class="text-muted f-XS">Артикул: 095068</small>
<small class="f-XS d-inline-block badge badge-pill badge-success">доступно</small>
</div>
<div class="item__title h4"><a href="/catalog/0000057/940152/?offerId=1058883"><span itemprop="name">АРГО-1</span></a></div>
<p class="f-S mb-0 text-truncate" itemprop="description">диван</p>
<p class="f-S mb-0 mt-1 text-truncate">спец категория</p>
<p class="f-S mb-0 mt-1 text-truncate">ORION TERRA</p>
</div>
<div class="item__footer mt-auto" itemprop="offers" itemscope="" itemtype="http://schema.org/Offer">
<meta content="21990" itemprop="price"/>
<meta content="RUB" itemprop="priceCurrency"/>
<div class="row no-gutters">
<div class="col-12">
<div class="price">
<div class="online-price">21 990 ₽</div>
</div>
<div class="favorite pull-right" data-placement="top" data-toggle="tooltip" title="Добавить в избранное">
<a class="js-favorite" data-action="add2favorites" data-cid="095068" data-id="940152" data-offer="1058883" data-price="21990" href="#"><i class="fa"></i></a>
</div>
</div>
</div>
</div>
<div class="item__footer_buy mt-auto" itemprop="offers" itemscope="" itemtype="http://schema.org/Offer">
<div class="row no-gutters">
<div class="d-flex flex-row mt-1 w-100 installment_halva">
<img class="img-fluid installment_halva__logo" src="/img/inparts/mini-logo.svg"> <span class="font-weight-bold">по 5 498 ₽</span>
</img></div>
<div class="mt-1">
<small>1 832.50 ₽/мес. в рассрочку на год </small>
</div>
<div class="btn btn-info btn-block buyoneclick mt-1" data-action="add2basket" data-cid="095068" data-id="1058883" data-name="АРГО-1" data-pid="940152" data-price="21990" data-section="Диваны прямые" data-stock-id="1" data-utm-campaign="buyoneclick_section">
<span>Купить в 1 клик</span>
</div>
<div class="btn btn-info btn-block buyininstallments mt-1" data-action="add2basket" data-cid="095068" data-id="1058883" data-is-installment="true" data-name="АРГО-1" data-pid="940152" data-price="21990" data-section="Диваны прямые" data-stock-id="1" data-utm-campaign="buyininstallments_section">
<span>РАССРОЧКА 0-0-12</span>
</div>
</div>
</div>
<div class="items-list__item-wrap">
<div class="stickers-block">
</div>
<div class="item__image">
<a href="/catalog/0000057/940152/?offerId=1058883"><img alt="АРГО-1" class="item__picture img-fluid" src="/upload/uf/698/6983d5a860b0c71e655554ef09697739.jpg?resize=w[384]h[237]f[t]fc[ffffff]"/>
</a>
</div>
<div class="item__description">
<div class="d-flex justify-content-between">
<small class="text-muted f-XS">Артикул: 095068</small>
<small class="f-XS d-inline-block badge badge-pill badge-success">доступно</small>
</div>
<div class="item__title h4"><a href="/catalog/0000057/940152/?offerId=1058883">АРГО-1</a></div>
<p class="f-S mb-0">диван</p>
<p class="f-S mb-0 mt-1">спец категория</p>
<p class="f-S mb-0 mt-1">ORION TERRA</p>
</div>
<div class="item__description">
<div class="product__properties">
<div class="h2">Характеристики</div>
<div class="product__properties-list">
<div class="m-b-1 h3">Размеры (в мм)</div>
<dl>
<dt><span>Глубина</span></dt>
<dd>900</dd>
</dl>
<dl>
<dt><span>Ширина</span></dt>
<dd>900</dd>
</dl>
<dl>
<dt><span>Высота</span></dt>
<dd>900</dd>
</dl>
<dl>
<dt><span>Длина</span></dt>
<dd>2230</dd>
</dl>
</div>
</div>
</div>
<div class="item__footer mt-auto">
<div class="row no-gutters">
<div class="col-12">
<div class="price">
<div class="online-price">21 990 ₽</div>
</div>
<div class="favorite pull-right" data-placement="top" data-toggle="tooltip" title="Добавить в избранное">
<a class="js-favorite" data-action="add2favorites" data-cid="095068" data-id="940152" data-offer="1058883" data-price="21990" href="#"><i class="fa"></i></a>
</div>
</div>
</div>
</div>
<div class="item__footer_buy mt-auto" itemprop="offers" itemscope="" itemtype="http://schema.org/Offer">
<div class="row no-gutters">
<div class="d-flex flex-row mt-1 w-100 installment_halva">
<img class="img-fluid installment_halva__logo" src="/img/inparts/mini-logo.svg"> <span class="font-weight-bold">по 5 498 ₽</span>
</img></div>
<div class="mt-1">
<small>1 832.50 ₽/мес. в рассрочку на год </small>
</div>
<div class="btn btn-info btn-block buyoneclick mt-1" data-action="add2basket" data-cid="095068" data-id="1058883" data-name="АРГО-1" data-pid="940152" data-price="21990" data-section="Диваны прямые" data-stock-id="1" data-utm-campaign="buyoneclick_section">
<span>Купить в 1 клик</span>
</div>
<div class="btn btn-info btn-block buyininstallments mt-1" data-action="add2basket" data-cid="095068" data-id="1058883" data-is-installment="true" data-name="АРГО-1" data-pid="940152" data-price="21990" data-section="Диваны прямые" data-stock-id="1" data-utm-campaign="buyininstallments_section">
<span>РАССРОЧКА 0-0-12</span>
</div>
</div>
</div>
</div>
</div>"""


def _get_soup(url):
    """Returns soup for the provided url"""
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')


def _get_absolute_href(link):
    """Returns absolute URL for the link"""
    return urljoin(URL, link['href'])


def _get_first_couch_url():
    """Locates link with 'Диваны прямые' as it's text and returns it's absolute href"""
    # return 'https://azbykamebeli.ru/catalog/0000057/'
    soup = _get_soup(URL)
    links = soup.find_all('a', text='Диваны прямые')
    if len(links) == 0:
        print('Unable to find the first link')
        return None
    return _get_absolute_href(links[0])


def _parse_couch_data(couch_data: Tag) -> Couch:
    """Parses one couch data div into StraightCouch instance"""
    vendor_code_item = couch_data.find_next('small')
    vendor_code = VENDOR_REGEX.search(vendor_code_item.text).group(1)

    status_item = vendor_code_item.find_next('small')
    status = status_item.text

    name_and_id_item = status_item.find_next('div', {'class': ['item__title']})

    name = name_and_id_item.text
    id_item = name_and_id_item.find_next('a')
    href = _get_absolute_href(id_item)
    parsed_href = urlparse(href)
    id = parse_qs(parsed_href.query)['offerId'][0]

    price_item_container = id_item.find_next('div', class_='price')
    full_price_item = price_item_container.find('a')
    discount_price_item = price_item_container.find('div').text

    discount_price = Decimal(re.sub(PRICE_REGEX, '', discount_price_item)).real
    if full_price_item:
        full_price = Decimal(re.sub(PRICE_REGEX, '', full_price_item.text)).real
    else:
        full_price = discount_price
        discount_price = None

    return Couch(name=name, vendor_code=vendor_code, discount_price=discount_price, full_price=full_price, status=status, scraped_id=id)


def scrape():
    """Parse data and save it into db"""
    page = 1
    print('Getting first page')

    next_page = _get_first_couch_url()

    while next_page:
        print(f'Parsing page {page}')

        soup = _get_soup(next_page)
        page += 1
        # soup = BeautifulSoup(couch_test_data, "html.parser")

        couch_divs = soup.find_all('div', class_='items-list__item')

        couch_list = [_parse_couch_data(div) for div in couch_divs]

        Couch.bulk_save(couch_list)

        next_page_item = soup.find('a', class_='page-link next')

        if next_page_item is None:
            break

        next_page = _get_absolute_href(next_page_item)


if __name__ == "__main__":
    scrape()
