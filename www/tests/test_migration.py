import unittest
from migrations import MigrationBuilder
import models


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.builder = MigrationBuilder(1, 'init')

    def test_build(self):
        self.builder.add_tables([models.ContentModel, models.ContentItem, models.ContentField, models.User])
        print(self.builder.lines[0]['sqls'])

    def test_drop(self):
        self.builder.drop_tables([models.ContentModel, models.ContentField, models.ContentItem, models.User])
        print(self.builder.lines[0]['sqls'])

    def test_migration_str(self):
        sql = self.builder.add_tables([models.ContentField, models.User])
        print(sql)