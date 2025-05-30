# UnitedChangerWeb 💱

![Logo](images/ReadMeIcon.png)

*Ваш универсальный инструмент для работы с валютами мира*

https://unitedchanger.glitch.me/

Многофункциональная веб-платформа для конвертации валют, анализа курсов и визуализации финансовых данных.

## 🌟 Основные возможности

- 🚀 **Мгновенная конвертация** 10+ мировых валют
- 📊 **Интерактивные графики** динамики курсов
- 💾 Автоматическое сохранение истории операций
- 🔗 Таблица смежности курсов валют
- 📈 Экспорт данных в CSV
- 🔍 Поиск по историческим данным

Приложение использует SQLite для хранения данных и предоставляет удобный веб-интерфейс.

-------------------------------------
🚀 Возможности
-------------------------------------

💱 Конвертер валют
📈 Графики изменений курсов
🧩 Таблица смежности валют
🗃 Хранение истории в базе данных SQLite
🌐 Простая и расширяемая архитектура на Flask

-------------------------------------
🛠️ Используемые технологии
-------------------------------------

- Python 3.11+
- Flask
- SQLite
- Jinja2
- Matplotlib (для графиков)
- Requests (для получения данных по API)

### Установка
```bash
# Клонирование репозитория
git clone https://github.com/yourusername/UnitedChangerWeb.git
cd UnitedChangerWeb
```

# Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate.bat  # Windows
```

# Установка зависимостей
```bash
pip install -r requirements.txt
```

# Инициализация БД
```bash
flask db init
flask db migrate
flask db upgrade
```

# Запуск приложения
```bash
flask run
```

Перейди по адресу http://127.0.0.1:5000 в браузере.

## 🛠 Внесение вклада

Мы рады любым улучшениям и идеям! Чтобы внести вклад:

1. Сделайте **fork** репозитория.
2. Создайте новую ветку:

   ```bash
   git checkout -b feature-name
   ```

3. Внесите изменения и закоммитьте:

   ```bash
   git commit -m "Добавил новую функцию"
   ```

4. Отправьте изменения:

   ```bash
   git push origin feature-name
   ```
   
5. Создайте **Pull Request**.

---

## 📄 Лицензия

Этот проект лицензирован на условиях **MIT License**. Подробности в [LICENSE](LICENSE).

---

## 📬 Контакты

Если у вас есть вопросы, идеи или предложения, пишите:

📧 **surovov1@yandex.ru**

---

**Спасибо за интерес к UnitedChanger!**  
Следите за обновлениями и помогайте развивать проект!
