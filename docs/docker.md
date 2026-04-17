# 🐳 Запуск через Docker

Проєкт CodeUA повністю контейнеризований. Для збірки та запуску використовуйте такі дії:

## 🛠 Збірка образу
```bash
docker build -t flet-codeua .
```
## 🛠 Підготовка до запуску
```bash
mv src/assets/.env.example src/assets/.env
nano src/assets/.env
```

## Запуск
```bash
docker run -d \
  -p 8585:8080 \
  --name codeua-container \
  -v $(pwd)/src/assets/.env:/app/src/assets/.env \
  --restart always \
  flet-codeua
```

#### Або:
```bash
docker run -it \
  -p 8585:8080 --name codeua-container \
  -e PYTHONUNBUFFERED=1 \
  -v $(pwd)/src/assets/.env:/app/src/assets/.env \
  flet-codeua
```
