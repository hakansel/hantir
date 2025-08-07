from enum import Enum
from typing import Optional, List


def get_total_email_count(ok_body: dict = None) -> Optional[int]:
    if ok_body is None:
        return None

    if ok_body.get('meta', None) is None:
        return None

    return ok_body['meta'].get('results', None)


def get_comma_seperated(params_as_list: List[Enum] = None) -> Optional[str]:
    if params_as_list is None:
        return None

    return ','.join(str(_.value) for _ in params_as_list)
