from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase, APIClient

import logging
import json

from recommender import views
from recommender.models import SetupLog

logger = logging.getLogger(__name__)


class ViewTest(TestCase):
    """
    run in terminal:
        python manage.py test recommender.tests.ViewTest
    """

    def setUp(self) -> None:

        # create user
        group = Group(name='DA')
        group.save()
        self.test_user1 = User.objects.create_user(username='testuser1', password='12345')
        self.test_user1.save()
        self.test_user1.groups.add(group)
        self.test_user1.save()
        self.test_user2 = User.objects.create_user(username='testuser2', password='12345')
        self.test_user2.save()
        self.client = APIClient()

    def test_get_records(self):
        self.client.force_authenticate(user=self.test_user1)
        data = {
            'on_page': 0,
            'page_size': 10,
        }
        resp = self.client.get(
            '/recommender/get/records', data=data,
            content_type='application/json;charset=utf-8')
        logger.info(resp)
        print(resp.json())

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('recommender'))
        logger.info(resp)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, '/accounts/login?next=/recommender')
        # self.assertRedirects(resp, '/accounts/login?next=/risk/risk_alert')

    def test_forbidden_if_logged_in_with_wrong_group(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('recommender'))
        logger.info(resp)
        self.assertEqual(resp.status_code, 403)

    def test_logged_in_with_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('recommender'))

        # Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(resp, 'index.html')

    def test_get_queryset(self):
        request = RequestFactory().get('/recommender')
        view = views.Record()
        view.request = request
        qs = view.get_queryset()
        logger.info(qs)

    def test_post_recommend_setup(self):
        self.client.force_authenticate(user=self.test_user1)
        data = {
            'start_date': '2021/08/18 11:00',
            'end_date': '2021/08/19 11:00',
            'timezone': 'UTC+0', 'timezone_diff': '0',
            'currency': 'CNY',
            'owners': [['istartbet', '597ee9128dfc0f0001dcd3d2'], ['seqrunqa', '597ee9aa8dfc0f0001dcd3da']],
            'games': [['1', 'FruitKing'], ['2', 'GodOfChess'], ['3', 'VampireKiss'], ['4', 'WildTarzan'], ['5', 'Mr.Rich'], ['6', '1945'], ['7', 'RaveJump'], ['8', 'SoSweet'], ['9', 'ZhongKui'], ['11', 'Wonderland2']]
        }
        self.client.post(
            '/recommender/setup', data=json.dumps(data),
            content_type='application/json;charset=utf-8')
        # setup second
        data['currency'] = 'THB'
        self.client.post(
            '/recommender/setup', data=json.dumps(data),
            content_type='application/json;charset=utf-8')

        logger.info('--------log---------')
        logger.info(SetupLog.objects.order_by('-create_time').values()[:1])
