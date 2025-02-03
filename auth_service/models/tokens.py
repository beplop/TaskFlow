from sqlalchemy.orm import Mapped, mapped_column

from auth_service.db.db import Base
from auth_service.schemas.tokens import TokenSchema


# class TokensModel(Base):
#     __tablename__ = 'tokens'
#
#     # id: Mapped[int] = mapped_column(primary_key=True)
#     access_token: Mapped[str]
#     token_type: Mapped[str]
#
#     def to_read_model(self) -> TokenSchema:
#         return TokenSchema(
#             # id=self.id,
#             access_token=self.access_token,
#             token_type=self.token_type,
#         )