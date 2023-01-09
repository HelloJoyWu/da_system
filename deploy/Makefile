SYS_NAME = sys_django
SYS_VERSION = 2.0
NGINX_NAME = sys_nginx
NGINX_VERSION = 2.0

.PHONY: build_django build_nginx build test start deploy down

build_django:
	docker build --force-rm --no-cache -t ${SYS_NAME}:${SYS_VERSION} ../da_sys_django \
		&& docker image prune -f

build_nginx:
	docker build --force-rm --no-cache -t ${NGINX_NAME}:${NGINX_VERSION} ./nginx \
		&& docker image prune -f


build:
	docker build --force-rm --no-cache -t ${SYS_NAME}:${SYS_VERSION} ../da_sys_django \
		&& docker build --force-rm -t ${NGINX_NAME}:${NGINX_VERSION} ./nginx \
		&& docker image prune -f

test:
	docker-compose -f docker-compose.test.yml up -d && docker-compose logs

test_down:
	docker-compose -f docker-compose.test.yml down && docker volume rm deploy_da_sys_volume && docker volume rm deploy_da_static

# -p server_port:container_port
# run on Integral server
start:
	docker run -d --rm --name da_system_DEV -p 8000:8000 \
		-v ${HOME}/dev/da_system/da_sys_django:/da_sys_django -w /da_sys_django \
		-e DJANGO_SETTINGS_MODULE=da_sys_django.settings.default \
		${SYS_NAME}:${SYS_VERSION} \
		/venv/bin/python manage.py runserver 0.0.0.0:8000 &

deploy:
	docker-compose up -d && docker-compose logs

down:
	docker-compose down && docker volume rm deploy_da_sys_volume && docker volume rm deploy_da_static
