from uuid import UUID

from pydantic import BaseModel


class PaymentInitializeRequest(BaseModel):
    order_id: UUID


class PaymentInitializeResponse(BaseModel):
    authorization_url: str
    reference: str


class PaymentVerifyResponse(BaseModel):
    order_id: UUID
    order_status: str
    payment_status: str
