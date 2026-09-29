import app.models.user
import app.models.product
import app.models.order
import app.models.order_item

from app.db.base import Base
from app.db.session import engine


def init_db():
    Base.metadata.create_all(bind=engine)