import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.otp import OTP
from app.services.email_service import EmailService
from app.core.exceptions import CustomError


class OTPService:

    @staticmethod
    def generate_otp(db: Session, user_id: str, email: str):
        otp_code = str(random.randint(100000, 999999))

        otp_obj = OTP(
            user_id=user_id,
            otp=otp_code,
            expires_at=datetime.utcnow() + timedelta(minutes=5),
        )

        db.add(otp_obj)
        db.commit()

        EmailService.send_otp_email(email, otp_code)

    @staticmethod
    def verify_otp(db: Session, user_id: str, otp: str):
        record = (
            db.query(OTP)
            .filter(OTP.user_id == user_id, OTP.otp == otp, OTP.is_used == False)
            .first()
        )

        if not record:
            raise CustomError("Invalid OTP", 400)

        if record.expires_at < datetime.utcnow():
            raise CustomError("OTP expired", 400)

        record.is_used = True
        db.commit()
