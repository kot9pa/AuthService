Функциональные требования:
1. Регистрация и аутентификация пользователя (JWT, Oauth 2.0);
2. Аутентифицированный пользователь должен иметь возможность создать или удалить свой реферальный код. Одновременно может быть активен только 1 код. При создании кода обязательно должен быть задан его срок годности;
3. Возможность получения реферального кода по email адресу реферера;
4. Возможность регистрации по реферальному коду в качестве реферала;
5. Получение информации о рефералах по id реферера;
6. UI документация (Swagger/ReDoc).

Опциональные задачи:
1. Использование clearbit.com/platform/enrichment для получения дополнительной информации о пользователе при регистрации;
2. Использование emailhunter.co для проверки указанного email адреса;
3. Кеширование реферальных кодов с использованием in-memory БД.

<<<<<<< HEAD

Сборка приложения:
1. Создать каталог certs:
`mkdir certs`
2. Сгенерировать публичный и приватный ключи:
# Generate an RSA private key, of size 2048
`openssl genrsa -out certs/private.pem 2048`
# Extract the public key from the key pair, which can be used in a certificate
`openssl rsa -in certs/private.pem -outform PEM -pubout -out certs/public.pem`
3. Запустить сборку образа приложения:
`docker build -t auth_service_app .`
`docker-compose build`

Как запустить приложение:
1. Установить и настроить Docker https://docs.docker.com/desktop/
2. Выполнить `docker-compose up`
=======
Как запустить приложение:
1. Установить и настроить Docker https://docs.docker.com/desktop/
2. Выполнить docker-compose up
>>>>>>> ffa37207553e94d5f73f37b6041eca84d76d6ae5
3. Перейти по адресу http://localhost:8080
