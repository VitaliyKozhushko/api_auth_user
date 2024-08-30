# Тестовое задание

Создать api приложение на Django с использованием DRF по управлению менторством

## Требования

API должен принимать запросы по следующим адресам:

1. `api/registration` - создание нового пользователя.
2. `api/login` - авторизация пользователя.
3. `api/users/` - список пользователей.
4. `api/users/<id>` - информация о пользователе.
5. `api/logout` - выход пользователя.

Аутентификация должна быть реализована через djangorestframework-simplejwt.

При регистрации обязательными параметрами являются - логин, пароль. Необязательным - номер телефона, e-mail.
В п.3 присылать информацию по логину и принадлежности к менторам.
К адресам из п.3, п.4 и п.5 должен быть доступ у всех авторизованных пользователей.
п.4 показывать пароль и иметь возможность изменить любое значение только самого себя.
п.4 если пользователь является ментором, то нужно дополнительно присылать список логинов пользователей, для которых он является ментором.
п.4 если у пользователя есть ментор(может быть только один), то присылать логин ментора
