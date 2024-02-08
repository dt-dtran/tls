from schemas import *
from uuid import uuid4
from utils import *
from db.models import *
import datetime
from fastapi import Response


# client = TestClient(app)

# sample account_id="6268a212-f4e5-4b44-994c-973fd4b4daa0"

account_id = str(uuid4())
privateKey = generate_private_key()
private_key = serialize_private_key(privateKey)
certificate_body = generate_certificate_from_private_key(privateKey, account_id)
created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

def test_create_certs():
    update = CertificateModel(
            id=1,
            account_id=account_id,
            is_active=False,
            private_key=private_key,
            certificate_body=certificate_body,
            created_at=created_at,
            updated_at=created_at
        )
    assert update
