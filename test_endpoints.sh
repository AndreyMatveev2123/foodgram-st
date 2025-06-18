#!/bin/bash

# Настройки пользователя для теста
EMAIL="test@example.com"
PASSWORD="testpass123"

# Получение JWT токена
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/token/login/ -H "Content-Type: application/json" -d '{"email": "'$EMAIL'", "password": "'$PASSWORD'"}' | grep -o '"auth_token":"[^"]*"' | cut -d '"' -f4)

if [ -z "$TOKEN" ]; then
  echo "Не удалось получить токен. Проверьте email и пароль."
  exit 1
fi

AUTH_HEADER="Authorization: Token $TOKEN"

# Функция для проверки endpoint
check() {
  METHOD=$1
  URL=$2
  DATA=$3
  EXTRA=""
  if [[ $METHOD == "POST" || $METHOD == "DELETE" ]]; then
    EXTRA="-H '$AUTH_HEADER'"
  fi
  if [[ $METHOD == "GET" ]]; then
    CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "$AUTH_HEADER" "$URL")
  elif [[ $METHOD == "POST" ]]; then
    CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "$AUTH_HEADER" "$URL" -d "$DATA")
  elif [[ $METHOD == "DELETE" ]]; then
    CODE=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE -H "$AUTH_HEADER" "$URL")
  fi
  echo "$METHOD $URL -> $CODE"
}

# Проверяем все endpoint-ы
check GET    http://localhost:8000/api/users/
check POST   http://localhost:8000/api/auth/jwt/create/ "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}"
check GET    http://localhost:8000/api/users/
check GET    http://localhost:8000/api/users/me/
check GET    http://localhost:8000/api/users/1/
check POST   http://localhost:8000/api/users/2/subscribe/ ""
check DELETE http://localhost:8000/api/users/2/subscribe/ ""
check GET    http://localhost:8000/api/users/subscriptions/
check GET    http://localhost:8000/api/tags/
check GET    http://localhost:8000/api/ingredients/
check GET    http://localhost:8000/api/ingredients/1
check GET    http://localhost:8000/api/recipes/
check GET    http://localhost:8000/api/recipes/1/
check GET    http://localhost:8000/api/recipes/2/
check DELETE http://localhost:8000/api/recipes/1/ ""
check POST   http://localhost:8000/api/recipes/2/favorite/ ""
check DELETE http://localhost:8000/api/recipes/1/favorite/ ""
check POST   http://localhost:8000/api/recipes/2/shopping_cart/ ""
check DELETE http://localhost:8000/api/recipes/1/shopping_cart/ ""
check GET    http://localhost:8000/api/recipes/download_shopping_cart/ 