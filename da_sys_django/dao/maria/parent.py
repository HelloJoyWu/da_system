import logging

from django.db import connections

logger = logging.getLogger(__name__)


def get_owner_currency_combo() -> dict:
    """
    c2o: Display currency to owner; find all the owners who have the currency
    o4ssid: Owner's account to ssid
    display_currency2n: Display currency to the real name; ex, 'VND' will get 'VND,VND(K)'
    Note:
        1. Display currency only replace '(*)'; ex, 'VND(K)' to 'VND', and 'MMK(100)' to 'MMK'
    """

    result = {'c2o': {}, 'o4ssid': {}, 'display_currency2n': {}}
    stmt = r"SELECT plo.account, plo.ssid, REGEXP_REPLACE(plp.currency, '(.*)([(].*[)])', '\\1') dsp_cur, "
    stmt += '  GROUP_CONCAT(DISTINCT plp.currency) cur_name '
    stmt += 'FROM cypress.parent_list plp '
    stmt += 'JOIN cypress.parent_list plo ON plp.owner = plo.ssid AND plo.istestss = 0 '
    stmt += 'WHERE plp.istestss = 0 '
    stmt += 'GROUP BY plo.ssid, dsp_cur'

    with connections['maria_read'].cursor() as cursor:
        cursor.execute(stmt)
        combos = cursor.fetchall()

    for _acc, ossid, dsp_cur, currencys in combos:
        acc = _acc.decode('utf-8')
        result['c2o'].setdefault(dsp_cur, []).append(acc)
        result['o4ssid'][acc] = ossid
        if dsp_cur in result['display_currency2n'].keys():
            if len(currencys) > len(result['display_currency2n'][dsp_cur]):
                result['display_currency2n'][dsp_cur] = currencys
        else:
            result['display_currency2n'][dsp_cur] = currencys

    return result
