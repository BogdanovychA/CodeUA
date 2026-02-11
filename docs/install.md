```bash
# 1. Клонуйте репозиторій
git clone https://github.com/BogdanovychA/CodeUA.git
cd CodeUA

# 2. Створіть оточення та встановіть залежності (Python підтягнеться автоматично)
uv sync

# 3. Налаштуйте pre-commit хуки (для розробки)
uv run pre-commit install
# опційно: uv run pre-commit run --all-files

# 4. Запустіть застосунок
uv run flet run     # опційно з ключем  --web 