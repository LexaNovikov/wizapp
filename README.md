# WIZ Control
## Описание:
### Это мини окошко для управления умной лампой wiz

## Быстрый старт
### Сначала скопируйте проект
```git clone https://github.com/LexaNovikov/wizapp.git```
### В папке проекта создайте виртуальное окружение
```python -m venv .venv```
### Активируйте виртуальное окружение и скачайте необходимые зависимости
```pip install -r requirements.txt```
### Создайте файл .env и по шаблону .env.example запишите туда ip своей лампы
```lamp_ip=lamp_ip=192.168.1.xx```

## Ярлык для пользователей linux
### Создайте файл ~/.local/share/applications/wiz-control.desktop
```nano ~/.local/share/applications/wiz-control.desktop```
### Вставьте туда следующий код и поменяйте пути на ваши
```
[Desktop Entry]
Version=1.0
Type=Application
Name=WiZ Control
Comment=Управление умной лампой
# Обязательно укажи полный путь к твоему Python-скрипту!
Exec=Корневая/директория/.venv/bin/python Корневая/директория/main.py
Icon=lightbulb
Terminal=false
Categories=Utility;
```
