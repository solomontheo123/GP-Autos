from enum import StrEnum


class ListingStatus(StrEnum):
    ACTIVE = "active"
    RESERVED = "reserved"
    SOLD = "sold"
    INACTIVE = "inactive"


class OrderStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PaymentStatus(StrEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
