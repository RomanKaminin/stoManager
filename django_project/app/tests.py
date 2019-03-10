import unittest

from app.models import Manager, Statement

from .utils import CarMark


class StatementModelTest(unittest.TestCase):
    def create_client_manager(self):
        self.manager = Manager.objects.create(name="Менеджер", parent=None)
        self.client = Statement.objects.create(
            username="Иван",
            first_name="Иванов",
            last_name="Иванович",
            date="2019-03-10",
            time="11:00",
            auto_mark=CarMark.KIA_S.name,
            manager=self.manager,
        )
        return self.client

    def test_client_model_creation(self):
        new_client = self.create_client_manager()
        self.assertTrue(isinstance(new_client, Statement))
