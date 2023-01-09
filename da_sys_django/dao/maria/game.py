import logging
from typing import Tuple

from django.db import connections

logger = logging.getLogger(__name__)


def get_code_name_searchers() -> Tuple[dict, dict, dict]:

    code2name = dict()
    name2code = dict()
    code2name_en = dict()
    stmt = 'SELECT game_code, game_name_en, game_name_tw FROM MaReport.game_info WHERE status = 1'

    with connections['maria_read'].cursor() as cursor:
        cursor.execute(stmt)
        infos = cursor.fetchall()

    for gcode, gname_en, gname in infos:
        code2name[gcode] = gname
        name2code[gname] = gcode
        code2name_en[gcode] = gname_en

    return code2name, name2code, code2name_en
