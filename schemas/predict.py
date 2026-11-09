from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    seller_id: int
    is_verified_seller: bool
    item_id: int
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    category: int
    images_qty: int = Field(..., ge=0)


class PredictResponse(BaseModel):
    is_violation: bool