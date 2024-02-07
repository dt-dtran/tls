from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.engine import SessionLocal, engine
from db import models
from schemas import *
from pydantic import UUID4
import logging
from typing import List
from utils import *

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# sample account_id="6268a212-f4e5-4b44-994c-973fd4b4daa0"

@app.get("/")
def read_root():
    return {"Service": "Certificate Endpoint"}

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    logger.info("Entering db_session_middleware")

    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
        logger.info("Exiting db_session_middleware")
    return response

# Dependency
def get_db(request: Request):
    logger.info("[GET] DB session")
    return request.state.db

@app.post("/certificates/", response_model=CertificateOut)
def create_certificate(db: Session = Depends(get_db), account_id=UUID4):
    logger.info(f"[POST] cert for account_id: {account_id}")

    privateKey = generate_private_key()
    logger.info(f"[POST] generate for private_key: {privateKey}")

    serialPrivateKey = serialize_private_key(privateKey)
    logger.info(f"[POST] cert for private_serial_key: {serialPrivateKey}")

    certificate_body= generate_certificate_from_private_key(privateKey, account_id)
    logger.info(f"[POST] cert for cert_body: {certificate_body}")

    db_item = models.CertificateModel(
        account_id=account_id,
        private_key=serialPrivateKey,
        certificate_body=certificate_body,
    )
    logger.info(f"[POST] cert: {db_item}")

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    if account_id is None:
        logger.warning("Account not found")
        raise HTTPException(status_code=404, detail="Account not found")
    logger.info("Certificate created successfully")
    return db_item

@app.get("/certificates/", response_model=List[CertificateOut])
def get_certificates(db: Session = Depends(get_db)):
    try:
        logger.info("[GET] certs")
        response = db.query(models.CertificateModel).all()

        return response
    except Exception as e:
        return {"error": e}

@app.get("/certificates/{certificate_id}", response_model=CertificateOut)
def get_certificate_by_id(db: Session = Depends(get_db), certificate_id=int):
    try:
        logger.info("[GET] cert by ID")
        response = db.query(models.CertificateModel).filter(models.CertificateModel.id == certificate_id).first()
        db_data_dict = response.__dict__ if response else None

        logger.info(f"[GET]cert - id dump {db_data_dict}")
        return response
    except Exception as e:
         return {"error": e}
@app.get("/certificates/{account_id}/", response_model=List[CertificateOut])
def get_certificates_by_account(db: Session = Depends(get_db), account_id=UUID4):
    try:
        if account_id is None:
            logger.warning("Account not found")
            raise HTTPException(status_code=404, detail="Account not found")

        logger.info(f"[GET] certs by accountID: {account_id}")
        response = db.query(models.CertificateModel).filter(models.CertificateModel.account_id == account_id).all()

        return response
    except Exception as e:
        logger.error(f"Error retrieving certificates: {e}")
        return {"error": e}

@app.patch("/certificates/{certificate_id}/deactivate/")
def deactivate_certificate(db: Session = Depends(get_db), certificate_id=int):
    try:
        logger.info(f"[PATCH] cert deactivate {certificate_id} Start")

        db_item = db.query(models.CertificateModel).get(certificate_id)

        if db_item is None:
            raise HTTPException(status_code=404, detail="Certificate ID not found")

        update_dict = db_item.__dict__ if db_item else None

        for key, value in update_dict.items():
            if key == "is_active":
                setattr(db_item, key, False)
            else:
                setattr(db_item, key, value)

        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return db_item

    except Exception as e:
        logger.error(f"Error deactivating certificate: {e}")
        return {"error": str(e)}

@app.patch("/certificate/{certificate_id}/activate/")
def activate_certificate(db: Session = Depends(get_db), certificate_id=int):
    try:
        logger.info(f"[PATCH] cert activate {certificate_id}")

        db_item = db.query(models.CertificateModel).get(certificate_id)

        if db_item is None:
            raise HTTPException(status_code=404, detail="Certificate ID not found")

        update_dict = db_item.__dict__ if db_item else None

        for key, value in update_dict.items():
            if key == "is_active":
                setattr(db_item, key, True)
            else:
                setattr(db_item, key, value)

        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return db_item

    except Exception as e:
        logger.error(f"Error deactivating certificate: {e}")
        return {"error": str(e)}
