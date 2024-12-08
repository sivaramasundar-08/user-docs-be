from sqlalchemy.orm import declarative_base
from app.models.user_model import UserDocumentModel


class DynamicModelGenerator:
    def __init__(self, engine):
        self.engine = engine

    @staticmethod
    def generate_user_document_model():
        base = declarative_base()

        class DynamicUserDocumentsModel(base, UserDocumentModel):
            __tablename__ = "user_documents"
            __table_args__ = {"extend_existing": True}

        return DynamicUserDocumentsModel

