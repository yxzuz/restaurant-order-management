from sqlalchemy.orm import Session

from app.models.table import Table, TableStatus


class TableRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self, restaurant_id: int) -> list[Table]:
        return self.db.query(Table).filter(Table.restaurant_id == restaurant_id).order_by(Table.number.asc()).all()

    def get_by_id(self, table_id: int) -> Table | None:
        return self.db.query(Table).filter(Table.id == table_id).first()

    def get_by_number(self, number: int, restaurant_id: int) -> Table | None:
        return self.db.query(Table).filter(
            Table.number == number,
            Table.restaurant_id == restaurant_id
        ).first()

    def get_by_number_and_qr_token(self, number: int, qr_token: str) -> Table | None:
        return (
            self.db.query(Table)
            .filter(Table.number == number, Table.qr_token == qr_token)
            .first()
        )

    def create(
        self,
        *,
        number: int,
        qr_token: str,
        restaurant_id: int,
        status: TableStatus = TableStatus.AVAILABLE,
    ) -> Table:
        table = Table(number=number, qr_token=qr_token,
                      restaurant_id=restaurant_id, status=status)
        self.db.add(table)
        self.db.commit()
        self.db.refresh(table)
        return table

    def delete(self, table: Table) -> None:
        self.db.delete(table)
        self.db.commit()

    def update_status(self, table: Table, status: TableStatus) -> Table:
        table.status = status
        self.db.commit()
        self.db.refresh(table)
        return table
