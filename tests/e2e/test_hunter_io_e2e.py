import os

import pytest

from src.facade.hunterio_facade import HunterIOFacade
from src.facade.hunterio_facade_models import DomainSearchOptions


@pytest.fixture(scope="module")
def env_vars():
    os.environ.setdefault("HUNTER_IO_API_KEY", "test-api-key")
    os.environ.setdefault("HUNTER_IO_API_URL", "https://api.hunter.io/v2")


@pytest.fixture(scope="module")
def facade(env_vars):
    return HunterIOFacade()


def test_run_domain_search(facade):
    options = DomainSearchOptions(
        limit=5,
        offset=0,
    )

    domain = "blabla.com"
    company = "Bla Bla Inc."

    response = facade.domain_search(domain=domain, company=company, options=options)

    assert response.status == 'success'
    assert response.body is not None

    assert response.body.get('domain') == 'piedpiper.com'
    assert response.body.get('emails')[0].get('value') == 'richard@piedpiper.com'

    assert response.total_email_count == 1


def test_run_email_verifier(facade):
    email = "test@blabla.com"
    dummy_response_score = 99
    response = facade.email_verifier(email=email)

    assert response.status == 'success'

    assert response.body is not None

    assert response.body.get('status') == 'valid'
    assert response.body.get('score') == dummy_response_score
    assert response.body.get('smtp_server') is True


if __name__ == '__main__':
    pytest.main()
