from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4, UUID
from typing_extensions import Annotated
import json

# Shared properties
class CertificateBase(BaseModel):
    # account_id: Optional[UUID] = None
    is_active: Optional[bool] = False
    private_key: Optional[bytes] = None
    certificate_body: Optional[bytes] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Properties received on create
class CertificateCreate(CertificateBase):
    account_id: UUID

# Properties received on update
class CertificateUpdate(CertificateBase):
    is_active: bool
    account_id: Optional[UUID] = None

# Properties stored in DB
class CertificateDBBase(CertificateBase):
    id: int
    is_active: bool
    private_key: bytes
    certificate_body: bytes
    account_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
        }

# Properties to return to client
class CertificateOut(CertificateDBBase):
    pass

# Properties stored in DB
class CertificateInDB(CertificateDBBase):
    pass

# Shared properties
class AccountVOBase(BaseModel):
    account_id: UUID
    first_name: str
    last_name: str

# Properties stored in DB
class AccountVODBBase(AccountVOBase):
    account_id: UUID
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Properties stored in DB
class AccountVOInDB(AccountVODBBase):
    pass
