Функциональные требования:
1. Регистрация и аутентификация пользователя (JWT, Oauth 2.0);
2. Аутентифицированный пользователь должен иметь возможность создать или удалить свой реферальный код. Одновременно может быть активен только 1 код. При создании кода обязательно должен быть задан его срок годности;
3. Возможность получения реферального кода по email адресу реферера;
4. Возможность регистрации по реферальному коду в качестве реферала;
5. Получение информации о рефералах по id реферера;
6. UI документация (Swagger/ReDoc).

Опциональные задачи (не реализовано):
1. Использование clearbit.com/platform/enrichment для получения дополнительной информации о пользователе при регистрации;
2. Использование emailhunter.co для проверки указанного email адреса;
3. Кеширование реферальных кодов с использованием in-memory БД.

Сборка приложения:
1. Создать каталог certs:
`mkdir certs`
2. Сгенерировать публичный и приватный ключи:

`openssl genrsa -out certs/private.pem 2048`

`openssl rsa -in certs/private.pem -outform PEM -pubout -out certs/public.pem`

3. Запустить сборку образа приложения:

`docker build -t auth_service_app .`

`docker compose build`

Как запустить приложение:
1. Установить и настроить Docker https://docs.docker.com/desktop/
2. Выполнить `docker compose up`
3. Перейти по адресу http://localhost:8080


Swagger UI http://localhost:8080/docs

Регистрация пользователя (JWT, Oauth 2.0)
http://localhost:8080/docs#/Users/create_user_api_v1_users__post

Аутентификация пользователя (JWT, Oauth 2.0)
http://localhost:8080/docs#/Auth/login_for_access_token_api_v1_auth__post

Аутентифицированный пользователь должен иметь возможность создать свой реферальный код
http://localhost:8080/docs#/Codes/create_code_api_v1_users__user_id__codes__post

Аутентифицированный пользователь должен иметь возможность удалить свой реферальный код
http://localhost:8080/docs#/Codes/delete_code_api_v1_users__user_id__codes__code_id__delete

Возможность получения реферального кода по email адресу реферера
http://localhost:8080/docs#/Users/get_codes_by_email_api_v1_users_get_codes_get

Получение информации о рефералах по id реферера
http://localhost:8080/docs#/Users/get_registered_users_api_v1_users_get_referrals_get