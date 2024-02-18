from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
import base64
import datetime
from sqlalchemy.orm.state import InstanceState
from fastapi.encoders import jsonable_encoder
import logging
import requests
import os
from uuid import UUID

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# cryptography
## create RSA Private Key Object
def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key

## Serialize PK ---BEGIN PRIVATE KEY--- ---END PRIVATE KEY---
def serialize_private_key(private_key):
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return private_key_bytes.decode('utf-8')

## Generate certificate
def generate_certificate_from_private_key(private_key, account_id):
    subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Colorado"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Denver"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "TranCodes"),
    x509.NameAttribute(NameOID.COMMON_NAME, f"trancodes.com/{account_id}"),
])
    cert = x509.CertificateBuilder().subject_name(
    subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]),
        critical=False,
    ).sign(private_key, hashes.SHA256())

    serialized_cert = cert.public_bytes(encoding=serialization.Encoding.PEM,)

    return serialized_cert.decode('utf-8')

# Serialization
## Decode from DB (binary to string(remove ---))
def serialize_byte(obj):
    string = base64.b64encode(obj).decode('utf-8')
    return string

def serialize_datetime(obj):
   return obj.isoformat()

def remove_non_serializable_attributes(obj):
    if isinstance(obj, dict):
        return {
            key: remove_non_serializable_attributes(value)
            for key, value in obj.items()
            if not isinstance(value, InstanceState)
        }
    elif isinstance(obj, list):
        return [remove_non_serializable_attributes(item) for item in obj]
    elif isinstance(obj, bytes):
        return serialize_byte(obj)
    elif isinstance(obj, UUID):
       return str(obj)
    elif isinstance(obj, type(datetime)):
       return serialize_datetime(obj)
    else:
        return jsonable_encoder(obj)

# httpbin:
def send_message_httpbin(method, obj, info):
    httpbin_url = os.getenv("POST_URL")

    try:
        payload = remove_non_serializable_attributes(obj.__dict__)
        logger.info(f"[POST] payload: {payload}")
        response = requests.post(httpbin_url, json=payload)
        response.raise_for_status()
        print(f"Method: {method}, Info: {info}")
        logger.info(f"HTTPBin [{method}] {info} response: {response.json()}")
    except requests.RequestException as e:
        logger.error(f"Error sending [{method}]{info} request to httpbin: {e}")
