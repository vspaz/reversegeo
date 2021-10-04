_EUROPE = {
    'AD',
    'AL',
    'AT',
    'BA',
    'BE',
    'BG',
    'BY',
    'CH',
    'CZ',
    'DE',
    'DK',
    'EE',
    'ES',
    'FI',
    'FO',
    'FR',
    'GB',
    'GG',
    'GI',
    'GR',
    'HR',
    'HU',
    'IE',
    'IM',
    'IS',
    'IT',
    'JE',
    'LI',
    'LT',
    'LU',
    'LV',
    'MC',
    'MD',
    'ME',
    'MK',
    'MT',
    'NL',
    'NO',
    'PL',
    'PT',
    'RO',
    'RS',
    'RU',
    'SE',
    'SI',
    'SJ',
    'SK',
    'SM',
    'UA',
}


def get_european_country_and_city(resp):
    short_country_name = ''
    city = ''
    address_components = resp.get('results')[0].get('address_components')
    for component in address_components:
        types = component['types']
        if 'country' in types:
            if component['short_name'] in _EUROPE:
                short_country_name = component['short_name']
        elif 'locality' in types:
            city = component['short_name']

    return short_country_name, city
