from django import template
from datetime import datetime, date, time
from django.utils.translation import gettext as _

register = template.Library()


@register.filter
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"


@register.filter
def translate_time(value):
    """
    Перевод времени в строковое значение
    """
    if isinstance(value, (datetime, time)):
        return value.strftime('%H:%M')   #Форматирование времени
    else:
        return '-'


@register.filter
def translate_date(value):
    """
    Перевод даты в строковое значение
    """
    if isinstance(value, (datetime, date)):
        return value.strftime('%d.%m.%Y')      #Форматирование даты
    else:
        return '-'


@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Проверка принадлежности пользователя к указанной группе
    """
    return user.groups.filter(name=group_name).exists()


@register.filter('translate')
def translate(value):
    """
    Перевод переданного значения
    """
    return _(value)


@register.filter(name='in_range')
def in_range(query_list):
    """
    Возвращает диапазон от 0 до длины переданного списка
    """
    return range(len(query_list))


@register.filter
def formatting_date(value: str):
    """
    Форматирование строчной даты
    """
    months = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня',
        7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря',
    }

    year, months, day = value.split('-')

    for k, v in months.items():
        if int(months) == k:
            months = v
            break

    clean_date = f'{day} {months} {year} r.'
    return clean_date


@register.filter
def formatting_time(value: str):
    """
    Форматирование времени строчного формата
    """
    clean_time = f'{value[:3]}'
    return clean_time