

## 📘 README.md

```markdown
# 📊 Matplotlib + SlowAPI Demo

Интерактивная демонстрационная программа, показывающая возможности библиотек **Matplotlib** (визуализация данных) и **SlowAPI** (ограничение частоты запросов).

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8.0-orange.svg)](https://matplotlib.org/)
[![SlowAPI](https://img.shields.io/badge/SlowAPI-0.1.9-red.svg)](https://github.com/laurentS/slowapi)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## ✨ Возможности

✅ **6 типов интерактивных графиков** — линейные, столбчатые, круговые, точечные, гистограммы, произвольные функции  
✅ **Rate Limiting из коробки** — защита API от чрезмерного количества запросов через SlowAPI  
✅ **Интерактивные формы** — выбор параметров, ввод данных, настройка стилей  
✅ **Наглядная демонстрация** — как работает ограничение запросов  
✅ **Красивый интерфейс** — адаптивный дизайн с карточками и анимацией  
✅ **Готовые примеры** — для быстрого старта и изучения

---

## 📦 Установка

```bash
# Клонируем репозиторий
git clone https://github.com/yourusername/matplotlib-slowapi-demo.git
cd matplotlib-slowapi-demo

# Создаем виртуальное окружение (рекомендуется)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Устанавливаем зависимости
pip install -r requirements.txt
```

**Файл requirements.txt:**
```txt
fastapi==0.104.1
uvicorn==0.24.0
slowapi==0.1.9
matplotlib==3.8.0
numpy==1.24.3
python-multipart==0.0.6
scipy==1.11.3
```

---

## 🚀 Быстрый старт

```bash
# Запускаем сервер
python demo.py
```

Откройте браузер и перейдите по адресу: **http://localhost:8000**

```python
# Минимальный пример использования API
import requests

# Получить линейный график
response = requests.get("http://localhost:8000/plot/line", data={
    "function": "sin",
    "color": "blue",
    "xmin": 0,
    "xmax": 10
})
print(response.status_code)  # 200 OK
```

**Больше примеров** — в [Wiki](https://github.com/yourusername/matplotlib-slowapi-demo/wiki).

---

## 📖 Примеры использования

### 🔹 Создание линейного графика через интерфейс

1. На главной странице нажмите на карточку **"Линейный график"**
2. Выберите функцию `sin(x)` из списка
3. Укажите диапазон X: от 0 до 10
4. Нажмите **"Построить график"**

### 🔹 Тестирование rate limiting

1. Перейдите на страницу **/test**
2. Несколько раз нажмите на карточку **"Ограниченный endpoint"**
3. На 4-й раз увидите ошибку 429 (Too Many Requests)

### 🔹 Создание своей функции

```python
# В форме произвольной функции введите:
np.sin(x) * np.exp(-x/5) + np.cos(x*2)
```

---

## 🏗 Архитектура

```
matplotlib-slowapi-demo/
├── demo.py                 # Основной файл приложения
├── requirements.txt        # Зависимости
├── README.md               # Документация
├── LICENSE                 # Лицензия
└── .gitignore              # Игнорируемые файлы
```

**Основные компоненты:**
- **FastAPI** — веб-фреймворк
- **SlowAPI** — rate limiting middleware
- **Matplotlib** — генерация графиков
- **NumPy/SciPy** — математические вычисления
- **HTML/CSS** — интерфейс пользователя

**Подробнее** — в разделе [Архитектура](https://github.com/yourusername/matplotlib-slowapi-demo/wiki/Архитектура).

---

## 📚 Документация

Полная документация доступна в [Wiki](https://github.com/yourusername/matplotlib-slowapi-demo/wiki):

- [Установка и настройка](https://github.com/yourusername/matplotlib-slowapi-demo/wiki/Установка)
- [Интерактивные графики](https://github.com/yourusername/matplotlib-slowapi-demo/wiki/Интерактивные-графики)
- [Rate Limiting с SlowAPI](https://github.com/yourusername/matplotlib-slowapi-demo/wiki/Rate-Limiting)
- [API Reference](https://github.com/yourusername/matplotlib-slowapi-demo/wiki/API-Reference)
- [Примеры использования](https://github.com/yourusername/matplotlib-slowapi-demo/wiki/Примеры)
- [FAQ](https://github.com/yourusername/matplotlib-slowapi-demo/wiki/FAQ)

---

## 🎯 Доступные endpoint'ы

| Маршрут | Описание | Rate Limit |
|---------|----------|------------|
| `/` | Главная страница | 10/мин |
| `/interactive/line` | Форма линейного графика | 5/мин |
| `/interactive/bar` | Форма столбчатой диаграммы | 5/мин |
| `/interactive/pie` | Форма круговой диаграммы | 5/мин |
| `/interactive/scatter` | Форма точечного графика | 5/мин |
| `/interactive/histogram` | Форма гистограммы | 5/мин |
| `/interactive/function` | Форма произвольной функции | 5/мин |
| `/plot/line` | POST создание линейного графика | 5/мин |
| `/plot/bar` | POST создание столбчатой диаграммы | 5/мин |
| `/plot/pie` | POST создание круговой диаграммы | 5/мин |
| `/plot/scatter` | POST создание точечного графика | 5/мин |
| `/plot/histogram` | POST создание гистограммы | 5/мин |
| `/plot/function` | POST создание произвольной функции | 5/мин |
| `/test` | Страница тестирования | 10/мин |
| `/test/public` | Публичный тестовый endpoint | 20/мин |
| `/test/limited` | Ограниченный тестовый endpoint | 3/мин |

---

## 🧪 Тестирование

### Тестирование rate limiting через curl

```bash
# Откройте новый терминал и быстро выполните:
curl http://localhost:8000/test/limited
curl http://localhost:8000/test/limited
curl http://localhost:8000/test/limited
curl http://localhost:8000/test/limited  # 429 Too Many Requests
```

### Тестирование создания графиков

```bash
# Создать линейный график через POST
curl -X POST http://localhost:8000/plot/line \
  -d "function=sin" \
  -d "color=blue" \
  -d "style=-" \
  -d "xmin=0" \
  -d "xmax=10" \
  -d "points=100" \
  -d "title=Мой+график"
```

---

## 🐛 Известные проблемы и решения

### SlowAPI не устанавливается на Python 3.13
**Решение:** Используйте Python 3.10 или 3.11, либо установите зависимости вручную:
```bash
pip install setuptools==65.5.0
pip install slowapi --no-deps
pip install fastapi uvicorn matplotlib numpy
```

### Графики не отображаются
**Решение:** Убедитесь, что используется `matplotlib.use('Agg')` в начале файла

---

## 🤝 Как помочь проекту

- Сообщайте об ошибках в [Issues](https://github.com/yourusername/matplotlib-slowapi-demo/issues)
- Предлагайте новые типы графиков
- Улучшайте дизайн интерфейса
- Добавляйте примеры использования
- Отправляйте Pull Request'ы

---

## 📄 Лицензия

MIT License. Подробнее в файле [LICENSE](LICENSE).

---

## 👨‍💻 Автор

**Ваше Имя**  
[![GitHub](https://img.shields.io/badge/GitHub-username-black)](https://github.com/username)  
[![Telegram](https://img.shields.io/badge/Telegram-@username-blue)](https://t.me/username)

---

⭐ **Если проект оказался полезным — поставьте звезду на GitHub!**
```

## 📚 Wiki: Главная страница

```markdown
# Добро пожаловать в Wiki Matplotlib + SlowAPI Demo!

Это полное руководство по демонстрационной программе, которая показывает возможности библиотек Matplotlib и SlowAPI.

## 📋 Содержание

- [Установка и настройка](Установка-и-настройка)
- [Интерактивные графики](Интерактивные-графики)
- [Rate Limiting с SlowAPI](Rate-Limiting-с-SlowAPI)
- [API Reference](API-Reference)
- [Примеры использования](Примеры-использования)
- [Архитектура](Архитектура)
- [FAQ](FAQ)
- [Contributing Guide](Contributing-Guide)

## 🎯 О проекте

Это интерактивное веб-приложение создано для демонстрации двух мощных Python библиотек:

### 📊 Matplotlib
Библиотека для визуализации данных, позволяющая создавать статические, анимированные и интерактивные графики. В нашем проекте реализовано 6 типов графиков с возможностью настройки параметров.

### ⏱️ SlowAPI
Библиотека для ограничения частоты запросов (rate limiting) в FastAPI приложениях. Защищает API от чрезмерного количества запросов и DDoS-атак.

## 🚀 Быстрый старт

1. **Установите Python 3.10+** (рекомендуется 3.10 или 3.11 для лучшей совместимости)
2. **Клонируйте репозиторий:** `git clone https://github.com/yourusername/matplotlib-slowapi-demo.git`
3. **Установите зависимости:** `pip install -r requirements.txt`
4. **Запустите приложение:** `python demo.py`
5. **Откройте браузер:** http://localhost:8000

## 📖 Структура Wiki

| Раздел | Описание |
|--------|----------|
| [Установка и настройка](Установка-и-настройка) | Подробная инструкция по установке, решению проблем, настройке окружения |
| [Интерактивные графики](Интерактивные-графики) | Описание всех типов графиков, параметров, примеры |
| [Rate Limiting с SlowAPI](Rate-Limiting-с-SlowAPI) | Как работает rate limiting, настройка лимитов, тестирование |
| [API Reference](API-Reference) | Полная документация по всем endpoint'ам |
| [Примеры использования](Примеры-использования) | Реальные примеры, сценарии использования |
| [Архитектура](Архитектура) | Внутреннее устройство, компоненты, поток данных |
| [FAQ](FAQ) | Часто задаваемые вопросы и ответы |
| [Contributing Guide](Contributing-Guide) | Как помочь проекту, код-стайл, PR |

---

**Следующий шаг:** [Установка и настройка →](Установка-и-настройка)
```

## 📚 Wiki: Установка и настройка

```markdown
# Установка и настройка

## 📋 Требования

- **Python**: 3.8 - 3.11 (рекомендуется 3.10 или 3.11)
- **pip**: последняя версия
- **Операционная система**: Windows, Linux, macOS

## 🔧 Пошаговая установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/matplotlib-slowapi-demo.git
cd matplotlib-slowapi-demo
```

### 2. Создание виртуального окружения (рекомендуется)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Содержимое requirements.txt:**
```txt
fastapi==0.104.1
uvicorn==0.24.0
slowapi==0.1.9
matplotlib==3.8.0
numpy==1.24.3
python-multipart==0.0.6
scipy==1.11.3
```

### 4. Запуск приложения

```bash
python demo.py
```

Вы должны увидеть:
```
======================================================================
🚀 ИНТЕРАКТИВНАЯ ДЕМОНСТРАЦИЯ MATPLOTLIB + SLOWAPI
======================================================================

📊 Matplotlib: 3.8.0
⏱️  SlowAPI: ✅ УСТАНОВЛЕН

📌 ИНТЕРАКТИВНЫЕ СТРАНИЦЫ:
   🏠 http://localhost:8000 - Главная с выбором
   ...
```

### 5. Проверка работы

Откройте браузер и перейдите по адресу: **http://localhost:8000**

## 🐛 Решение проблем

### SlowAPI не устанавливается на Python 3.13

**Проблема:** SlowAPI требует старые версии зависимостей, несовместимые с Python 3.13

**Решения:**

1. **Используйте Python 3.10 или 3.11** (рекомендуется)
   ```bash
   # Установите Python 3.10 с официального сайта
   # Создайте виртуальное окружение с Python 3.10
   python3.10 -m venv venv
   ```

2. **Установка с игнорированием зависимостей**
   ```bash
   pip install setuptools==65.5.0
   pip install slowapi --no-deps
   pip install fastapi uvicorn matplotlib numpy
   ```

### Matplotlib ошибка "no display name and no $DISPLAY environment variable"

**Решение:** Добавьте в начало файла:
```python
import matplotlib
matplotlib.use('Agg')  # Использовать бэкенд без GUI
```

### Порт 8000 уже занят

**Решение:** Измените порт в последней строке:
```python
uvicorn.run(app, host="127.0.0.1", port=8001)  # Использовать другой порт
```

### Ошибка "ModuleNotFoundError: No module named 'scipy'"

**Решение:** Установите scipy:
```bash
pip install scipy
```

## ⚙️ Настройка rate limiting

По умолчанию установлены следующие лимиты:

| Endpoint | Лимит | Назначение |
|----------|-------|------------|
| `/` | 10/мин | Главная страница |
| `/interactive/*` | 5/мин | Формы графиков |
| `/plot/*` | 5/мин | Создание графиков |
| `/test/public` | 20/мин | Тестовый публичный |
| `/test/limited` | 3/мин | Тестовый ограниченный |

### Изменение лимитов

В коде найдите декораторы `@limiter.limit()` и измените значение:

```python
@app.get("/plot/line")
@limiter.limit("10/minute")  # Было 5/мин, стало 10/мин
async def line_plot():
    ...
```

## 🚀 Запуск в production

Для production-среды рекомендуется использовать Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker demo:app
```

Или с настройками:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  demo:app
```

## 📦 Docker (опционально)

Создайте `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY demo.py .

CMD ["uvicorn", "demo:app", "--host", "0.0.0.0", "--port", "8000"]
```

Сборка и запуск:
```bash
docker build -t matplotlib-slowapi-demo .
docker run -p 8000:8000 matplotlib-slowapi-demo
```

---

**Далее:** [Интерактивные графики →](Интерактивные-графики)
```

## 📚 Wiki: Интерактивные графики

```markdown
# Интерактивные графики

## 📊 Обзор

В приложении реализовано 6 типов интерактивных графиков. Каждый график имеет форму для настройки параметров и ограничение 5 запросов в минуту.

---

## 📈 1. Линейный график

**Маршрут:** `/interactive/line`

### Параметры настройки

| Параметр | Описание | Возможные значения |
|----------|----------|-------------------|
| Функция | Тип функции | sin, cos, tan, exp, log, sqrt, x², x³ |
| Цвет линии | Цвет графика | Синий, Красный, Зеленый, Оранжевый, Фиолетовый, Черный |
| Стиль линии | Вид линии | Сплошная, Пунктирная, Точечная, Штрих-пунктирная |
| X от | Начало диапазона | Любое число |
| X до | Конец диапазона | Любое число |
| Точек | Количество точек | 10-1000 |
| Название | Заголовок графика | Текст |

### Пример использования

1. Выберите функцию `sin(x)`
2. Цвет: Красный
3. X от: 0, X до: 10
4. Точек: 200
5. Нажмите "Построить график"

**Результат:** График синусоиды красного цвета от 0 до 10 с 200 точками.

---

## 📊 2. Столбчатая диаграмма

**Маршрут:** `/interactive/bar`

### Параметры настройки

| Параметр | Описание | Пример |
|----------|----------|--------|
| Категории | Названия столбцов через запятую | Python, JavaScript, Java, C++ |
| Значения | Числа через запятую | 95, 90, 85, 80 |
| Цветовая схема | Цветовая палитра | Viridis, Plasma, Inferno, Magma, Cividis |
| Название | Заголовок диаграммы | Популярность языков |
| Показывать значения | Отображать числа над столбцами | Да/Нет |

### Пример использования

```
Категории: Продажи, Маркетинг, Разработка, Поддержка
Значения: 450000, 230000, 380000, 120000
Название: Бюджет компании 2024
```

---

## 🥧 3. Круговая диаграмма

**Маршрут:** `/interactive/pie`

### Параметры настройки

| Параметр | Описание | Пример |
|----------|----------|--------|
| Названия секторов | Через запятую | Продажи, Маркетинг, Разработка |
| Размеры секторов | Через запятую | 40, 25, 20 |
| Выделить сектор | Номер сектора для выделения | 0 (первый) |
| Название | Заголовок | Распределение бюджета |
| Тень | Добавить тень | Да/Нет |

### Особенности
- Автоматически рассчитываются проценты
- Сектора разноцветные
- Можно выделить один сектор (увеличить отступ)

---

## 🔵 4. Диаграмма рассеяния

**Маршрут:** `/interactive/scatter`

### Параметры настройки

| Параметр | Описание | Диапазон |
|----------|----------|----------|
| Количество точек | Сколько точек сгенерировать | 10-500 |
| Сила корреляции | Насколько связаны X и Y | 0-1 (слайдер) |
| Цвет точек по | По какому параметру красить | X, Y, Плотность |
| Название | Заголовок | Текст |

### Как это работает

Генерируются случайные данные с заданной корреляцией:
- **Корреляция 0** — точки распределены случайно
- **Корреляция 0.5** — средняя связь
- **Корреляция 0.9** — точки почти на линии

Добавляется линия тренда и показывается фактическая корреляция.

---

## 📋 5. Гистограмма

**Маршрут:** `/interactive/histogram`

### Параметры настройки

| Параметр | Описание | Значения |
|----------|----------|----------|
| Тип распределения | Статистическое распределение | Нормальное, Равномерное, Экспоненциальное, Пуассона, Биномиальное |
| Количество значений | Размер выборки | 10-10000 |
| Интервалов | Количество столбцов | 5-100 |
| Параметр 1 | Зависит от распределения | Среднее, λ, n и т.д. |
| Параметр 2 | Зависит от распределения | Std, p и т.д. |

### Типы распределений

| Тип | Параметр 1 | Параметр 2 | Описание |
|-----|------------|------------|----------|
| Нормальное | Среднее (μ) | Стд. отклонение (σ) | Колоколообразная кривая |
| Равномерное | Минимум | Максимум | Все значения равновероятны |
| Экспоненциальное | λ (лямбда) | - | Время между событиями |
| Пуассона | λ (лямбда) | - | Количество событий |
| Биномиальное | n (испытаний) | p (вероятность) | Успехи в серии испытаний |

---

## 📐 6. Произвольная функция

**Маршрут:** `/interactive/function`

### Параметры настройки

| Параметр | Описание | Пример |
|----------|----------|--------|
| Функция | Математическое выражение | np.sin(x) * np.exp(-x/5) |
| X от | Начало диапазона | 0 |
| X до | Конец диапазона | 20 |
| Точек | Количество точек | 200 |
| Название | Заголовок | Сложная функция |

### Доступные функции и константы

**Математические функции:**
- `np.sin(x)`, `np.cos(x)`, `np.tan(x)`
- `np.exp(x)`, `np.log(x)`, `np.sqrt(x)`
- `np.abs(x)`, `np.floor(x)`, `np.ceil(x)`

**Константы:**
- `np.pi` — число π (3.14159...)
- `np.e` — число e (2.71828...)

**Операторы:**
- `+` сложение
- `-` вычитание
- `*` умножение
- `/` деление
- `**` возведение в степень

### Примеры функций

```python
# Простые
x**2                    # Парабола
x**3 - 2*x + 1          # Кубическая
np.sin(2*x)             # Синус с частотой 2

# Сложные
np.sin(x) * np.exp(-x/10)           # Затухающие колебания
np.sin(x) * np.cos(2*x)             # Биения
np.sqrt(x) * np.sin(x)               # Корень * синус
np.exp(-((x-5)**2)/2)                # Гауссиана
np.sin(x) / x                         # sinc функция
```

---

## ⚠️ Обработка ошибок

При вводе некорректных данных вы увидите сообщение об ошибке:

- **Не совпадает количество категорий и значений** — для столбчатой диаграммы
- **Ошибка в функции** — синтаксическая ошибка в выражении
- **Превышен лимит запросов** — 429 Too Many Requests

---

**Далее:** [Rate Limiting с SlowAPI →](Rate-Limiting-с-SlowAPI)
```

## 📚 Wiki: Rate Limiting с SlowAPI

```markdown
# Rate Limiting с SlowAPI

## ⏱️ Что такое rate limiting?

Rate limiting (ограничение частоты запросов) — это механизм защиты API от чрезмерного количества запросов. Он ограничивает, сколько раз клиент (IP-адрес) может обратиться к серверу за определенный промежуток времени.

**Зачем нужно:**
- Защита от DDoS-атак
- Предотвращение перегрузки сервера
- Справедливое распределение ресурсов
- Защита от брутфорс-атак

---

## 🔧 Как работает SlowAPI

SlowAPI — это библиотека для FastAPI, которая добавляет middleware для отслеживания и ограничения запросов.

### Базовый пример

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

# Создаем лимитер на основе IP-адреса
limiter = Limiter(key_func=get_remote_address)

# Применяем к endpoint'у
@app.get("/api/data")
@limiter.limit("5/minute")
async def get_data(request: Request):
    return {"data": "success"}
```

### Формат лимитов

```
[количество]/[период]
```

Примеры:
- `5/minute` — 5 запросов в минуту
- `100/hour` — 100 запросов в час
- `1000/day` — 1000 запросов в день
- `10/second` — 10 запросов в секунду

---

## 📊 Лимиты в демо-приложении

| Endpoint | Лимит | Назначение |
|----------|-------|------------|
| `/` | 10/мин | Главная страница |
| `/interactive/line` | 5/мин | Форма линейного графика |
| `/interactive/bar` | 5/мин | Форма столбчатой диаграммы |
| `/interactive/pie` | 5/мин | Форма круговой диаграммы |
| `/interactive/scatter` | 5/мин | Форма точечного графика |
| `/interactive/histogram` | 5/мин | Форма гистограммы |
| `/interactive/function` | 5/мин | Форма произвольной функции |
| `/plot/line` | 5/мин | Создание линейного графика |
| `/plot/bar` | 5/мин | Создание столбчатой диаграммы |
| `/plot/pie` | 5/мин | Создание круговой диаграммы |
| `/plot/scatter` | 5/мин | Создание точечного графика |
| `/plot/histogram` | 5/мин | Создание гистограммы |
| `/plot/function` | 5/мин | Создание произвольной функции |
| `/test` | 10/мин | Страница тестирования |
| `/test/public` | 20/мин | Публичный тестовый endpoint |
| `/test/limited` | 3/мин | Ограниченный тестовый endpoint |

---

## 🧪 Тестирование rate limiting

### Через браузер

1. Перейдите на страницу `/test`
2. Нажимайте на карточку **"Ограниченный endpoint"**
3. Первые 3 раза — успех
4. На 4-й раз — ошибка 429

### Через curl (в новом окне терминала)

```bash
# Быстро выполните эти команды:
curl http://localhost:8000/test/limited
curl http://localhost:8000/test/limited
curl http://localhost:8000/test/limited
curl http://localhost:8000/test/limited  # 429 Too Many Requests
```

### Через Python

```python
import requests
import time

url = "http://localhost:8000/test/limited"

for i in range(4):
    response = requests.get(url)
    print(f"Попытка {i+1}: {response.status_code}")
    if response.status_code == 429:
        print("  Превышен лимит!")
        print(f"  Осталось подождать: {response.json().get('reset_after', 60)} сек")
    time.sleep(0.5)  # Небольшая задержка
```

---

## 📝 Обработка ошибок

При превышении лимита SlowAPI возвращает:

```json
{
    "detail": "Rate limit exceeded: 3 per 1 minute"
}
```

Статус-код: **429 Too Many Requests**

### Кастомная обработка

```python
from fastapi import HTTPException
from slowapi.errors import RateLimitExceeded

@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Слишком много запросов",
            "message": "Подождите немного и повторите",
            "limit": "3 запроса в минуту",
            "ip": request.client.host
        }
    )
```

---

## 🔧 Настройка хранилища

SlowAPI поддерживает различные хранилища для счетчиков:

### In-memory (по умолчанию)

```python
limiter = Limiter(key_func=get_remote_address)
```

### Redis (для production)

```python
from slowapi import Limiter
from slowapi.storage import redis_storage

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379/0"
)
```

### Memcached

```python
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memcached://localhost:11211"
)
```

---

## 🎯 Разные лимиты для разных пользователей

### По IP-адресу

```python
limiter = Limiter(key_func=get_remote_address)
```

### По API-ключу

```python
def get_api_key(request):
    return request.headers.get("X-API-Key", "anonymous")

limiter = Limiter(key_func=get_api_key)
```

### По пользователю (из токена)

```python
def get_user_id(request):
    token = request.headers.get("Authorization")
    # Декодируем токен и получаем user_id
    return user_id

limiter = Limiter(key_func=get_user_id)
```

### Комбинированный ключ

```python
def get_custom_key(request):
    ip = request.client.host
    user_agent = request.headers.get("User-Agent", "unknown")
    return f"{ip}:{user_agent}"

limiter = Limiter(key_func=get_custom_key)
```

---

## 📈 Мониторинг и статистика

### Получение информации о лимитах

```python
@app.get("/rate-limits")
async def get_rate_limits():
    return {
        "limits": {
            "/": "10/minute",
            "/test/public": "20/minute",
            "/test/limited": "3/minute"
        }
    }
```

### Показ оставшихся запросов

```python
@app.get("/api/data")
@limiter.limit("5/minute")
async def get_data(request: Request):
    # В реальном SlowAPI нужно получать из middleware
    remaining = 4  # Заглушка
    
    return {
        "data": "success",
        "rate_limit": {
            "limit": 5,
            "remaining": remaining,
            "period": "1 minute"
        }
    }
```

---

## ⚠️ Особенности и ограничения

### SlowAPI не работает с WebSocket
Rate limiting применяется только к HTTP запросам.

### Точность времени
Зависит от хранилища. In-memory — точный, Redis — зависит от сети.

### Сброс лимитов
Лимиты сбрасываются автоматически по истечении периода (скользящее окно).

---

## 🔍 Отладка

### Включение логов

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Проверка счетчиков

```python
# Для in-memory хранилища
print(limiter._storage._get("rate_limit:192.168.1.1:/limited"))
```

---

## 📚 Дополнительные ресурсы

- [Официальная документация SlowAPI](https://github.com/laurentS/slowapi)
- [Rate limiting strategies](https://blog.logrocket.com/rate-limiting-fastapi/)
- [FastAPI middleware](https://fastapi.tiangolo.com/tutorial/middleware/)

---

**Далее:** [API Reference →](API-Reference)
```

## 📚 Wiki: API Reference

```markdown
# API Reference

## 📋 Общая информация

**Базовый URL:** `http://localhost:8000`

**Формат ответов:** JSON / HTML

**Rate Limiting:** Применяется ко всем endpoint'ам

---

## 🏠 Основные страницы

### GET /

Главная страница с карточками графиков.

**Rate Limit:** 10/минуту

**Ответ:** HTML страница

---

## 📈 Интерактивные формы

### GET /interactive/line

Форма для создания линейного графика.

**Rate Limit:** 5/минуту

**Ответ:** HTML страница с формой

---

### GET /interactive/bar

Форма для создания столбчатой диаграммы.

**Rate Limit:** 5/минуту

---

### GET /interactive/pie

Форма для создания круговой диаграммы.

**Rate Limit:** 5/минуту

---

### GET /interactive/scatter

Форма для создания диаграммы рассеяния.

**Rate Limit:** 5/минуту

---

### GET /interactive/histogram

Форма для создания гистограммы.

**Rate Limit:** 5/минуту

---

### GET /interactive/function

Форма для создания произвольной функции.

**Rate Limit:** 5/минуту

---

## 🎨 Создание графиков (POST)

### POST /plot/line

Создает линейный график.

**Rate Limit:** 5/минуту

**Параметры формы:**

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `function` | string | Да | Тип функции: sin, cos, tan, exp, log, sqrt, x^2, x^3 |
| `color` | string | Да | Цвет: blue, red, green, orange, purple, black |
| `style` | string | Да | Стиль: - (сплошная), -- (пунктир), : (точечная), -. (штрих-пунктир) |
| `xmin` | float | Да | Начало диапазона |
| `xmax` | float | Да | Конец диапазона |
| `points` | int | Да | Количество точек (10-1000) |
| `title` | string | Нет | Название графика |

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/plot/line \
  -d "function=sin" \
  -d "color=blue" \
  -d "style=-" \
  -d "xmin=0" \
  -d "xmax=10" \
  -d "points=100" \
  -d "title=Мой+график"
```

**Ответ:** HTML страница с графиком

---

### POST /plot/bar

Создает столбчатую диаграмму.

**Rate Limit:** 5/минуту

**Параметры формы:**

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `categories` | string | Да | Категории через запятую |
| `values` | string | Да | Значения через запятую |
| `color_scheme` | string | Нет | Цветовая схема: viridis, plasma, inferno, magma, cividis |
| `title` | string | Нет | Название |
| `show_values` | bool | Нет | Показывать значения (по умолчанию true) |

---

### POST /plot/pie

Создает круговую диаграмму.

**Rate Limit:** 5/минуту

**Параметры формы:**

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `labels` | string | Да | Названия секторов через запятую |
| `sizes` | string | Да | Размеры секторов через запятую |
| `explode` | int | Нет | Номер сектора для выделения (-1 = не выделять) |
| `title` | string | Нет | Название |
| `shadow` | bool | Нет | Добавить тень |

---

### POST /plot/scatter

Создает диаграмму рассеяния.

**Rate Limit:** 5/минуту

**Параметры формы:**

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `n_points` | int | Да | Количество точек (10-500) |
| `correlation` | float | Да | Сила корреляции (0-1) |
| `color_by` | string | Нет | Цвет по: x, y, density |
| `title` | string | Нет | Название |

---

### POST /plot/histogram

Создает гистограмму.

**Rate Limit:** 5/минуту

**Параметры формы:**

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `distribution` | string | Да | Тип: normal, uniform, exponential, poisson, binomial |
| `n_samples` | int | Да | Количество значений (10-10000) |
| `bins` | int | Да | Количество интервалов (5-100) |
| `param1` | float | Нет | Параметр 1 |
| `param2` | float | Нет | Параметр 2 |
| `title` | string | Нет | Название |

---

### POST /plot/function

Создает график произвольной функции.

**Rate Limit:** 5/минуту

**Параметры формы:**

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `func` | string | Да | Математическое выражение |
| `xmin` | float | Да | Начало диапазона |
| `xmax` | float | Да | Конец диапазона |
| `points` | int | Да | Количество точек |
| `title` | string | Нет | Название |

---

## ⏱️ Тестирование rate limiting

### GET /test

Страница для тестирования rate limiting.

**Rate Limit:** 10/минуту

**Ответ:** HTML страница

---

### GET /test/public

Публичный тестовый endpoint.

**Rate Limit:** 20/минуту

**Ответ:**
```json
{
    "message": "Публичный endpoint",
    "limit": "20/минуту",
    "remaining": 19,
    "ip": "127.0.0.1",
    "time": "2024-01-01T12:00:00"
}
```

---

### GET /test/limited

Ограниченный тестовый endpoint.

**Rate Limit:** 3/минуту

**Ответ:**
```json
{
    "message": "Ограниченный endpoint",
    "limit": "3/минуту",
    "remaining": 2,
    "ip": "127.0.0.1",
    "time": "2024-01-01T12:00:00"
}
```

---

## ℹ️ Дополнительная информация

### GET /rate-limits

Информация о всех rate limits в приложении.

**Rate Limit:** нет

**Ответ:**
```json
{
    "rate_limiting": "активен",
    "type": "SlowAPI",
    "limits": {
        "Главная страница": {"path": "/", "limit": "10/минуту"},
        "Публичный endpoint": {"path": "/test/public", "limit": "20/минуту"},
        "Ограниченный endpoint": {"path": "/test/limited", "limit": "3/минуту"},
        "Линейный график": {"path": "/plots/line", "limit": "5/минуту"},
        ...
    }
}
```

---

### GET /stats

Статистика приложения.

**Rate Limit:** нет

**Ответ:**
```json
{
    "app": "Matplotlib + SlowAPI Demo",
    "python_version": "3.10+",
    "matplotlib_version": "3.8.0",
    "numpy_version": "1.24.3",
    "slowapi_status": "установлен",
    "total_endpoints": 15,
    "time": "2024-01-01T12:00:00"
}
```

---

## 🔍 Документация

### GET /docs

Swagger UI документация (автоматически генерируется FastAPI).

**Rate Limit:** нет

**Ответ:** Интерактивная документация

---

### GET /redoc

ReDoc документация (альтернативный стиль).

**Rate Limit:** нет

---

## ⚠️ Коды ошибок

| Код | Описание | Пример |
|-----|----------|--------|
| 200 | Успех | Запрос выполнен |
| 400 | Bad Request | Неверные параметры |
| 404 | Not Found | Страница не найдена |
| 429 | Too Many Requests | Превышен лимит запросов |
| 500 | Internal Server Error | Ошибка на сервере |

### Пример ошибки 429

```json
{
    "detail": "Rate limit exceeded: 3 per 1 minute"
}
```

---

## 📝 Заголовки ответов

При использовании SlowAPI добавляются заголовки:

- `X-RateLimit-Limit` — максимальное количество запросов
- `X-RateLimit-Remaining` — оставшееся количество
- `X-RateLimit-Reset` — время сброса (Unix timestamp)

---

**Далее:** [Примеры использования →](Примеры-использования)
```

Я создал для вас полноценный README.md и Wiki с 5 разделами:
1. **Главная страница Wiki** — навигация
2. **Установка и настройка** — подробная инструкция
3. **Интерактивные графики** — описание всех типов
4. **Rate Limiting с SlowAPI** — как это работает
5. **API Reference** — полная документация по endpoint'ам

