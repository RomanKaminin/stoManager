import unittest

from app.models import Manager, Statement

from .utils import CarMark


class StatementModelTest(unittest.TestCase):
    def create_client_manager(self):
        self.managers = Manager.objects.create(name="Менеджеры", parent=None)
        self.client = Statement.objects.create(
            username="Иван",
            first_name="Иванов",
            last_name="Иванович",
            date="2000-10-10",
            time="11:00",
            auto_mark=CarMark.KIA_S.name,
            manager=self.managers,
        )
        return self.client

    def test_client_model_creation(self):
        new_client = self.create_client_manager()
        self.assertTrue(isinstance(new_client, Statement))
