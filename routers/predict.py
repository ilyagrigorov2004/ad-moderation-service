from fastapi import APIRouter, HTTPException, Depends
from schemas.predict import PredictRequest, PredictResponse
from services.moderation import ModerationService, BusinessLogicError
from repositories.ads import AdRepository

router = APIRouter()


def get_moderation_service() -> ModerationService:
    return ModerationService(AdRepository())


@router.post("/predict", response_model=PredictResponse, status_code=200)
async def predict(
    payload: PredictRequest,
    service: ModerationService = Depends(get_moderation_service)
):
    try:
        is_violation = await service.predict_violation(payload)
        return PredictResponse(is_violation=is_violation)
    except BusinessLogicError as e:
        # 500 Internal Server Error для ошибок бизнес-логики
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        # 500 для любых непредвиденных ошибок
        raise HTTPException(status_code=500, detail="Internal Server Error")