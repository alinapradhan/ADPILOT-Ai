from fastapi import Header

from core.errors import AuthorizationError
from data.synthetic_provider_data import SYNTHETIC_AUTHZ


def get_current_user_id(x_user_id: str = Header(default="user-1")) -> str:
    return x_user_id


def authorize_scope(*, user_id: str, client_id: str, account_id: str) -> None:
    accounts = SYNTHETIC_AUTHZ.get(user_id, {}).get(client_id)
    if not accounts or account_id not in accounts:
        raise AuthorizationError()
