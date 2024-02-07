from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
import base64
import datetime

# Decode from DB (binary to string(remove ---))
def decode_db(binary):
    string = base64.b64encode(binary).decode('utf-8')
    return string

# create RSA Private Key Object
def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key

# Serialize PK ---BEGIN PRIVATE KEY--- ---END PRIVATE KEY---
def serialize_private_key(private_key):
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return private_key_bytes

# Generate certificate
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

    return serialized_cert
