from app.repositories.table_repository import TableRepository


class TableService:
    def __init__(self, db_session):
        self.table_repository = TableRepository(db_session)

    def list_tables(self):
        return self.table_repository.list_all()

    def get_table_by_access(self, table_number: int, qr_token: str):
        return self.table_repository.get_by_number_and_qr_token(table_number, qr_token)
