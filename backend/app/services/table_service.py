import secrets

from app.models.table import TableStatus
from app.repositories.order_repository import OrderRepository
from app.repositories.table_repository import TableRepository


class TableService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.table_repository = TableRepository(db_session)
        self.order_repository = OrderRepository(db_session)

    def list_tables(self, restaurant_id: int):
        return self.table_repository.list_all(restaurant_id)

    def get_table_by_access(self, table_number: int, qr_token: str):
        return self.table_repository.get_by_number_and_qr_token(table_number, qr_token)

    def create_table(self, number: int, restaurant_id: int):
        existing_table = self.table_repository.get_by_number(number, restaurant_id)
        if existing_table is not None:
            raise ValueError(f"Table {number} already exists")

        return self.table_repository.create(
            number=number,
            qr_token=self._generate_qr_token(),
            restaurant_id=restaurant_id,
            status=TableStatus.AVAILABLE,
        )

    def delete_table(self, table_number: int, restaurant_id: int) -> bool:
        table = self.table_repository.get_by_number(table_number, restaurant_id)
        if table is None:
            return False

        if self.order_repository.has_orders_for_table_id(table.id):
            raise ValueError("Table cannot be deleted because it has order history")

        self.table_repository.delete(table)
        return True

    def _generate_qr_token(self) -> str:
        return secrets.token_urlsafe(16)
