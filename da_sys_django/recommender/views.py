from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection

import logging
import json
import pytz
from datetime import datetime, timedelta

from dao.maria import parent, game
from recommender.models import SetupLog

logger = logging.getLogger(__name__)


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['owner_info'] = json.dumps(parent.get_owner_currency_combo())
        code2name, name2code, code2name_en = game.get_code_name_searchers()
        context['game_code2name'] = json.dumps(code2name)
        context['game_name2code'] = json.dumps(name2code)
        context['game_code2name_en'] = json.dumps(code2name_en)
        return context


class Setup(APIView):

    def post(self, request, format=None):

        req_dict = request.data
        logger.info('---get params---')
        logger.info(req_dict)
        logger.info('---get params---')

        start = req_dict.get('start_date')
        end = req_dict.get('end_date')
        timezone = req_dict.get('timezone')
        timezone_diff = int(req_dict.get('timezone_diff'))
        start_time = datetime.strptime(start, '%Y/%m/%d %H:00') - timedelta(hours=timezone_diff)
        start_time = start_time.replace(tzinfo=pytz.UTC)
        end_time = datetime.strptime(end, '%Y/%m/%d %H:00') - timedelta(hours=timezone_diff)
        end_time = end_time.replace(tzinfo=pytz.UTC)
        display_currency_name = req_dict.get('currency')
        currency_name = req_dict.get('currency_name')
        owner_names = []
        owner_ssids = []
        game_names = []
        game_codes = []
        game_names_en = []
        for o_name, o_ssid in req_dict.get('owners'):
            owner_names.append(o_name)
            owner_ssids.append(o_ssid)
        for g_code, g_name, g_name_en in req_dict.get('games'):
            game_codes.append(g_code)
            game_names.append(g_name)
            game_names_en.append(g_name_en)

        setup_log = SetupLog.objects.create(
            start=start, end=end, timezone=timezone, timezone_diff=timezone_diff,
            currency_name=display_currency_name, owner_names=','.join(owner_names), owner_ssids=','.join(owner_ssids),
            game_names=','.join(game_names), game_codes=','.join(game_codes),
            start_time=start_time, end_time=end_time, currency=currency_name,
            creator=request.user.username, game_names_en=','.join(game_names_en)
        )
        setup_log.save()

        return Response('Receive success!')


class GetRecord(APIView):

    def get(self, request, format=None):
        """
        Get steup-logs in recent 3 month (90 days)
        :param: on_page
        :param: page_size
        """

        logger.info(f'{self.request} (param: {self.request.query_params}; data: {self.request.data})')

        query_dict = self.request.query_params
        _on_page: str = query_dict.get('on_page')
        _page_size: str = query_dict.get('page_size')
        if any(map(lambda i: i in ['', None], [_on_page, _page_size])):
            return Response('Request parameters not sufficient for GetRecord!', status.HTTP_400_BAD_REQUEST)

        try:
            on_page = int(_on_page)
            page_size = int(_page_size)
            redis = get_redis_connection()
            utc_now = datetime.utcnow()
            query_from = utc_now.replace(tzinfo=pytz.UTC) - timedelta(days=90)
            _now = utc_now.strftime('%Y%m%dT%H%M')
            _key_prefix = f'recommender:setup:log:{_now}:p' + '{on_page}'
            _key = _key_prefix.format(on_page=on_page)
            _mx_p_key = f'recommender:setup:log:{_now}:maxp'
            logger.info(f'{self.request} with key: {_key}')
            _mx_page = redis.get(_mx_p_key)
            _res = redis.get(_key)
            if _res is None:
                logger.debug(f'Generate for {_key}')
                logs = list(
                    SetupLog.objects.filter(create_time__gte=query_from).values_list(
                        'start', 'end', 'timezone', 'currency_name', 'owner_names',
                        'game_names', 'game_codes', 'game_names_en', 'create_time', 'creator'))
                _mx_p = 0
                for _p in range(0, len(logs), page_size):
                    _page_logs = logs[_p:(_p+page_size)]
                    _p_key = _key_prefix.format(on_page=_p // page_size)
                    redis.setex(_p_key, 60, json.dumps(_page_logs, cls=DjangoJSONEncoder))
                    _mx_p += 1

                redis.setex(_mx_p_key, 60, _mx_p)
                _res = redis.get(_key)
                _mx_page = redis.get(_mx_p_key)

            logger.debug('--- setup logs with page ---')
            logger.debug(_res)
            logger.debug('--- setup logs with page ---')
            _resp_data = {'setup_logs': [], 'max_page': 0}
            if _res is None:
                return Response(_resp_data)
            else:
                _resp_data['setup_logs'] = json.loads(_res.decode())
                _resp_data['max_page'] = json.loads(_mx_page.decode())
                return Response(_resp_data)

        except Exception:
            logger.exception(f'GetRecord API (param: {self.request.query_params}; data: {self.request.data}) FAILED!')
            return Response('Get records error!', status.HTTP_500_INTERNAL_SERVER_ERROR)


class Record(LoginRequiredMixin, ListView):
    template_name = 'record.html'
    login_url = '/login'
    context_object_name = 'new10RecommendLogs'

    def get_queryset(self):
        new10logs = list(
            SetupLog.objects.order_by('-create_time').values_list(
                'start', 'end', 'timezone', 'currency_name', 'owner_names',
                'game_names', 'game_codes', 'create_time', 'creator')[:10])
        return json.dumps(new10logs, cls=DjangoJSONEncoder)
