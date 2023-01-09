from django.test import SimpleTestCase
from django.test.runner import DiscoverRunner
import logging
from datetime import datetime, timedelta

from dao.maria import parent

logger = logging.getLogger(__name__)


class DAOTest(SimpleTestCase):
    """
    run in terminal:
        python manage.py test dao.tests.DAOTest --testrunner=dao.tests.NoDbTestRunner
    """
    databases = {'maria_read', 'maria_read_test_mysql', }

    def setUp(self) -> None:
        self.to_dt = datetime.utcnow()
        self.from_dt = self.to_dt - timedelta(days=1)
        pass

    def tearDown(self) -> None:
        pass

    def test_mysql_connector_connections(self):
        from django.db import connections
        with connections['maria_read_test_mysql'].cursor() as cursor:
            cursor.execute('SELECT * FROM MaReport.game_info;')
            result = list(cursor)
            print(result[:10])
            self.assertIsNotNone(result)
            cursor.execute('SELECT @@session.time_zone;')
            result = list(cursor)
            print(result)

    def test_connections(self):
        from django.db import connections
        with connections['maria_read'].cursor() as cursor:
            cursor.execute('SELECT * FROM MaReport.game_info;')
            result = list(cursor)
            print(result[:10])
            self.assertIsNotNone(result)
            # cursor.execute('SHOW GRANTS')
            # result = list(cursor)
            # print(result[:10])

    def test_db_setup(self):
        from django.db import connections
        with connections['maria_read'].cursor() as cursor:
            cursor.execute('SELECT @@session.time_zone;')
            tz_setup = cursor.fetchone()[0]
            print('maria timezone is set: ' + tz_setup)
            self.assertEqual('+00:00', tz_setup)
            # cursor.execute('SELECT @@tx_isolation;')
            # isolation_setup = cursor.fetchone()[0]
            # logger.info('maria ISOLATION LEVEL is set: ' + isolation_setup)
            # self.assertEqual('READ-UNCOMMITTED', isolation_setup)

    def test_parent(self):
        result = parent.get_owner_currency_combo()
        print(result['c2o'].keys())
        print(result['display_currency2n'])


class NoDbTestRunner(DiscoverRunner):
    """ A test runner to test without database creation/deletion """

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
