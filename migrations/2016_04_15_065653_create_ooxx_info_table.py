# coding=utf8
from orator.migrations import Migration


class CreateOoxxInfoTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('ooxx') as table:
            table.string('url').unique()
            table.binary('image')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('ooxx')
