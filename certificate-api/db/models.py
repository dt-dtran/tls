from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class CertificateModel(Base):
    __tablename__ = 'certificate'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(UUID(as_uuid=True), nullable=True)
    is_active = Column(Boolean, default=False)
    private_key = Column(LargeBinary, nullable=True)
    certificate_body = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Refactor to include Account Information
    # account_id = Column(UUID(as_uuid=True), ForeignKey("account_vo.account_id"), nullable=True)
    # account_info = relationship("AccountVO", back_populates="certificates")
    # account_info = relationship("AccountVO", uselist=False)

# class AccountVO(Base):
#     __tablename__ = 'account_vo'
#     account_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
#     first_name = Column(String)
#     last_name = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     certificates = relationship("Certificate", back_populates="account")
