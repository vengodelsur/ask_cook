### Как запустить сервис в докере
Из корня проекта запускаем:
```
docker-compose -f docker/docker-compose.yml up
```
Для остановки:
```
docker-compose -f docker/docker-compose.yml down
```

### Что запускается?
На данный момент, в отдельных контейнерах поднимается тестовое веб приложение cleaned_demo и экземпляр memcached.
При первом запуске может запуститься сборка или скачивание недостающих образов.

### Как обратиться к сервису?
Веб сервис доступен на порту 5000 (см. секцию ports в сервисе web).
Остальные сервисы доступны по сети только из контейнеров.
Так, например, к memcached обращаемся через TCP по адресу "cache:11211".
Доменное имя для контейнера совпадает с именем сервиса в docker-compose.yml