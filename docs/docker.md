# 🐳 Запуск через Docker

Проєкт CodeUA повністю контейнеризований. Для збірки та запуску використовуйте такі команди:

## 🛠 Збірка образу
```bash
docker build -t flet-codeua .
```

## Запуск
```bash
docker run -d \
  -p 8585:8080 \
  --name codeua-container \
  -v $(pwd)/src/assets/.env:/app/src/assets/.env \
  --restart always \
  flet-codeua

## Або: 
# docker run -it \
#  -p 8585:8080 --name codeua-container \
#  -e PYTHONUNBUFFERED=1 \
#  -v $(pwd)/src/assets/.env:/app/src/assets/.env \
#  flet-codeua
```