import logging
import os
from enum import Enum
from http import HTTPStatus, HTTPMethod
from urllib.parse import urlencode

import requests

from src.facade.hunter_io_helper import get_total_email_count
from src.facade.hunterio_facade_models import Response, DomainSearchOptions

logger = logging.getLogger(__name__)


class ImplementedEndpoint(Enum):
    DOMAIN_SEARCH = '/domain-search'
    EMAIL_VERIFIER = '/email-verifier'


class HunterIOFacade(object):

    def __init__(self):
        super().__init__()
        api_key = os.environ.get("HUNTER_IO_API_KEY", None)
        self.base_api_url = os.environ.get("HUNTER_IO_API_URL", "https://api.hunter.io/v2")
        self.headers = {
            'content-type': 'application/json',
            'X-API-KEY': api_key,
        }
        self.timeout = 10

    def domain_search(self,
                      domain: str,
                      company: str,
                      options: DomainSearchOptions = None) -> Response:
        options = options or DomainSearchOptions()
        try:
            resp = self._do_request(
                method=HTTPMethod.GET,
                path=ImplementedEndpoint.DOMAIN_SEARCH.value,
                query_params={
                    "domain": domain,
                    "company": company,
                    **options.build_as_params()
                }
            )
        except Exception as exception:
            err = f"Facade could not complete request caused by {exception}"
            logger.error(err, exc_info=True)
            return Response(status='error', error=err)

        if resp.status_code == HTTPStatus.OK.value:
            ok_body = resp.json()
            return Response(
                status='success',
                body=ok_body.get('data'),
                total_email_count=get_total_email_count(ok_body),
            )

        return self._handle_generic_error_response(resp)

    def email_verifier(self, email: str) -> Response:
        self.timeout = 30  # allow to complete https://hunter.io/api-documentation/v2#email-verifier
        try:
            resp = self._do_request(
                method=HTTPMethod.GET,
                path=ImplementedEndpoint.EMAIL_VERIFIER.value,
                query_params={
                    "email": email,
                }
            )
        except Exception as exception:
            err = f"Facade could not complete request caused by {exception}"
            logger.error(err, exc_info=True)
            return Response(status='error', error=err)

        if resp.status_code == HTTPStatus.OK.value:
            ok_body = resp.json()
            return Response(
                status='success',
                body=ok_body.get('data'),
            )

        smtp_server_error = 222
        if resp.status_code in [HTTPStatus.ACCEPTED.value,
                                HTTPStatus.UNAVAILABLE_FOR_LEGAL_REASONS.value,
                                smtp_server_error]:
            return Response(status='error', error=resp.json().get('details'))

        return self._handle_generic_error_response(resp)

    def _do_request(self,
                    method: HTTPMethod,
                    path: str,
                    query_params: dict = None,
                    request_body: dict = None) -> requests.Response:
        url = self._prepare_url(path, query_params)
        return requests.request(
            method=method.value,
            url=url,
            json=request_body,
            headers=self.headers,
            timeout=self.timeout, )

    def _prepare_url(self, path: str, query_params: dict) -> str:
        base_url = f'{self.base_api_url}/{path}'

        if query_params is None or len(query_params) == 0:
            return base_url

        filtered_params = {key: vall for key, vall in query_params.items() if vall is not None}
        return f'{base_url}?{urlencode(filtered_params)}'

    def _handle_generic_error_response(self, resp: requests.Response) -> Response:
        if resp.status_code == [HTTPStatus.TOO_MANY_REQUESTS.value,
                                HTTPStatus.NOT_FOUND.value,
                                HTTPStatus.FORBIDDEN.value,
                                HTTPStatus.UNAUTHORIZED.value,
                                HTTPStatus.BAD_REQUEST.value,
                                HTTPStatus.UNAVAILABLE_FOR_LEGAL_REASONS.value, ] \
                or str(resp.status_code).startswith('5'):
            return Response(status='error', error=resp.json().get('details'))

        err = f'Unknown status code {resp.status_code}'
        logger.warning(f'Facade faced with undocumented status code {resp.status_code}')
        return Response(status='error', error=err)
