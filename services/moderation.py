from schemas.predict import PredictRequest
from repositories.ads import AdRepository


class BusinessLogicError(Exception):
    """Исключение для ошибок на уровне бизнес-логики."""
    pass


class ModerationService:
    def __init__(self, repository: AdRepository):
        self.repository = repository

    async def predict_violation(self, data: PredictRequest) -> bool:
        # Эмуляция возможной ошибки бизнес-логики (например, при сбое внешнего ML-сервиса)
        if data.item_id == 0:
            raise BusinessLogicError("Item ID cannot be zero in business logic")

        # Наивная логика: подтвержденные пользователи без нарушений,
        # неподтвержденные - только при наличии изображений
        if data.is_verified_seller:
            is_violation = False
        else:
            is_violation = data.images_qty == 0

        # Сохраняем результат (демонстрация использования репозитория)
        await self.repository.save_prediction(data.item_id, is_violation)

        return is_violation