# coding=utf8
from orator.migrations import Migration


class CreateJavInfoTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('jav') as table:
            table.string('uid', 20)
            table.binary('images')
            table.binary('torrent')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('jav')
