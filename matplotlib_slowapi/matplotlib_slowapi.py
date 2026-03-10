"""
Интерактивная демонстрация Matplotlib + SlowAPI
С возможностью выбора параметров и ввода данных
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
from datetime import datetime
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import random
from collections import defaultdict
import threading
import os

# Пытаемся импортировать slowapi
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    SLOWAPI_AVAILABLE = True
    print("✅ SlowAPI успешно импортирован")
except ImportError:
    print("⚠️ SlowAPI не установлен, используется встроенный rate limiter")
    SLOWAPI_AVAILABLE = False

# ==================== СОБСТВЕННЫЙ RATE LIMITER ====================
class SimpleRateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def check_limit(self, key: str, limit: int, period: int = 60) -> bool:
        with self.lock:
            now = time.time()
            self.requests[key] = [ts for ts in self.requests[key] if now - ts < period]
            if len(self.requests[key]) >= limit:
                return False
            self.requests[key].append(now)
            return True
    
    def get_remaining(self, key: str, limit: int, period: int = 60) -> int:
        with self.lock:
            now = time.time()
            self.requests[key] = [ts for ts in self.requests[key] if now - ts < period]
            return max(0, limit - len(self.requests[key]))

simple_limiter = SimpleRateLimiter()

# ==================== НАСТРОЙКА FASTAPI ====================
if SLOWAPI_AVAILABLE:
    limiter = Limiter(key_func=get_remote_address)
    app = FastAPI(title="Matplotlib + SlowAPI Interactive Demo")
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
else:
    class DummyLimiter:
        def limit(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
    limiter = DummyLimiter()
    app = FastAPI(title="Matplotlib + Rate Limiting Interactive Demo")

# Создаем директорию для шаблонов
os.makedirs("templates", exist_ok=True)

# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================
def fig_to_base64(fig):
    """Конвертирует график в base64"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_str

def generate_html(title, content, image=None, form=None):
    """Генерирует HTML страницу с формой и результатами"""
    image_html = f'<img src="data:image/png;base64,{image}" style="max-width:100%; margin-top:20px; border:1px solid #ddd; border-radius:10px; box-shadow:0 5px 15px rgba(0,0,0,0.1);">' if image else ''
    
    form_html = form if form else ''
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            
            .nav {{
                background: #f8f9fa;
                padding: 15px 30px;
                border-bottom: 1px solid #dee2e6;
            }}
            
            .nav a {{
                display: inline-block;
                padding: 10px 20px;
                margin-right: 10px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background 0.3s;
            }}
            
            .nav a:hover {{
                background: #764ba2;
            }}
            
            .content {{
                padding: 40px;
            }}
            
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin: 30px 0;
            }}
            
            .card {{
                background: white;
                border: 1px solid #e9ecef;
                border-radius: 10px;
                padding: 25px;
                transition: transform 0.3s, box-shadow 0.3s;
                cursor: pointer;
            }}
            
            .card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(102,126,234,0.3);
            }}
            
            .card h3 {{
                color: #495057;
                margin-bottom: 15px;
                font-size: 1.5em;
            }}
            
            .card .icon {{
                font-size: 2.5em;
                margin-bottom: 15px;
                color: #667eea;
            }}
            
            .limit-badge {{
                background: #e9ecef;
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 0.9em;
                color: #495057;
                display: inline-block;
                margin: 10px 0;
            }}
            
            .form-container {{
                background: #f8f9fa;
                padding: 30px;
                border-radius: 10px;
                margin: 20px 0;
            }}
            
            .form-group {{
                margin-bottom: 20px;
            }}
            
            label {{
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #495057;
            }}
            
            input[type="text"],
            input[type="number"],
            select,
            textarea {{
                width: 100%;
                padding: 12px;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                font-size: 1em;
                transition: border-color 0.3s;
            }}
            
            input[type="text"]:focus,
            input[type="number"]:focus,
            select:focus,
            textarea:focus {{
                outline: none;
                border-color: #667eea;
            }}
            
            .btn {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 8px;
                font-size: 1.1em;
                cursor: pointer;
                transition: opacity 0.3s;
            }}
            
            .btn:hover {{
                opacity: 0.9;
            }}
            
            .btn-secondary {{
                background: #6c757d;
            }}
            
            .result-container {{
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
            }}
            
            .info-box {{
                background: #e7f3ff;
                border-left: 4px solid #667eea;
                padding: 20px;
                margin: 20px 0;
                border-radius: 5px;
            }}
            
            .stats {{
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-top: 30px;
            }}
            
            .stat-item {{
                text-align: center;
            }}
            
            .stat-value {{
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }}
            
            .stat-label {{
                color: #6c757d;
            }}
            
            @media (max-width: 768px) {{
                .content {{
                    padding: 20px;
                }}
                
                .nav a {{
                    display: block;
                    margin: 5px 0;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Matplotlib + SlowAPI</h1>
                <p>Интерактивная демонстрация с возможностью выбора параметров</p>
            </div>
            
            <div class="nav">
                <a href="/">🏠 Главная</a>
                <a href="/interactive/line">📈 Линейный</a>
                <a href="/interactive/bar">📊 Столбчатый</a>
                <a href="/interactive/pie">🥧 Круговой</a>
                <a href="/interactive/scatter">🔵 Точечный</a>
                <a href="/interactive/histogram">📋 Гистограмма</a>
                <a href="/interactive/function">📐 Функция</a>
                <a href="/test">⏱️ Тест лимитов</a>
            </div>
            
            <div class="content">
                {form_html}
                {image_html}
                <div class="result-container">
                    {content}
                </div>
            </div>
        </div>
    </body>
    </html>
    """

# ==================== ИНТЕРАКТИВНЫЕ ЭНДПОИНТЫ ====================
@app.get("/", response_class=HTMLResponse)
@limiter.limit("10/minute")
async def root(request: Request):
    """Главная страница с выбором"""
    remaining = simple_limiter.get_remaining(request.client.host, 10, 60) if not SLOWAPI_AVAILABLE else 10
    
    form = f"""
    <div class="grid">
        <div class="card" onclick="location.href='/interactive/line'">
            <div class="icon">📈</div>
            <h3>Линейный график</h3>
            <p>Постройте график функции с настраиваемыми параметрами</p>
            <div class="limit-badge">5 запросов/мин</div>
        </div>
        
        <div class="card" onclick="location.href='/interactive/bar'">
            <div class="icon">📊</div>
            <h3>Столбчатая диаграмма</h3>
            <p>Сравните несколько категорий с разными значениями</p>
            <div class="limit-badge">5 запросов/мин</div>
        </div>
        
        <div class="card" onclick="location.href='/interactive/pie'">
            <div class="icon">🥧</div>
            <h3>Круговая диаграмма</h3>
            <p>Визуализируйте доли и проценты</p>
            <div class="limit-badge">5 запросов/мин</div>
        </div>
        
        <div class="card" onclick="location.href='/interactive/scatter'">
            <div class="icon">🔵</div>
            <h3>Диаграмма рассеяния</h3>
            <p>Исследуйте корреляцию между переменными</p>
            <div class="limit-badge">5 запросов/мин</div>
        </div>
        
        <div class="card" onclick="location.href='/interactive/histogram'">
            <div class="icon">📋</div>
            <h3>Гистограмма</h3>
            <p>Анализируйте распределение данных</p>
            <div class="limit-badge">5 запросов/мин</div>
        </div>
        
        <div class="card" onclick="location.href='/interactive/function'">
            <div class="icon">📐</div>
            <h3>Произвольная функция</h3>
            <p>Введите свою математическую функцию</p>
            <div class="limit-badge">5 запросов/мин</div>
        </div>
    </div>
    
    <div class="info-box">
        <h3>ℹ️ Информация</h3>
        <p>👋 Ваш IP: <strong>{request.client.host}</strong></p>
        <p>⏱️ Rate Limiting: <strong>{"SlowAPI" if SLOWAPI_AVAILABLE else "Встроенный"}</strong></p>
        <p>📊 Matplotlib: <strong>{matplotlib.__version__}</strong></p>
        <p>🎯 Осталось запросов: <strong>{remaining}/10</strong> на этой странице</p>
    </div>
    
    <div class="stats">
        <div class="stat-item">
            <div class="stat-value">6</div>
            <div class="stat-label">Типов графиков</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">∞</div>
            <div class="stat-label">Настроек</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">5/мин</div>
            <div class="stat-label">Лимит графиков</div>
        </div>
    </div>
    """
    
    return HTMLResponse(content=generate_html("Главная", "", form=form))

@app.get("/interactive/line", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def line_form(request: Request):
    """Форма для линейного графика"""
    remaining = simple_limiter.get_remaining(request.client.host, 5, 60) if not SLOWAPI_AVAILABLE else 5
    
    form = f"""
    <h2>📈 Линейный график</h2>
    <div class="info-box">
        <p>Осталось запросов: <strong>{remaining}/5</strong> в минуту</p>
    </div>
    
    <form action="/plot/line" method="post" class="form-container">
        <div class="form-group">
            <label for="function">Выберите функцию:</label>
            <select name="function" id="function" required>
                <option value="sin">sin(x)</option>
                <option value="cos">cos(x)</option>
                <option value="tan">tan(x)</option>
                <option value="exp">exp(x)</option>
                <option value="log">log(x)</option>
                <option value="sqrt">sqrt(x)</option>
                <option value="x^2">x²</option>
                <option value="x^3">x³</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="color">Цвет линии:</label>
            <select name="color" id="color" required>
                <option value="blue">Синий</option>
                <option value="red">Красный</option>
                <option value="green">Зеленый</option>
                <option value="orange">Оранжевый</option>
                <option value="purple">Фиолетовый</option>
                <option value="black">Черный</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="style">Стиль линии:</label>
            <select name="style" id="style" required>
                <option value="-">Сплошная</option>
                <option value="--">Пунктирная</option>
                <option value=":">Точечная</option>
                <option value="-."">Штрих-пунктирная</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="xmin">X от:</label>
            <input type="number" name="xmin" id="xmin" step="any" value="0" required>
        </div>
        
        <div class="form-group">
            <label for="xmax">X до:</label>
            <input type="number" name="xmax" id="xmax" step="any" value="10" required>
        </div>
        
        <div class="form-group">
            <label for="points">Количество точек:</label>
            <input type="number" name="points" id="points" min="10" max="1000" value="100" required>
        </div>
        
        <div class="form-group">
            <label for="title">Название графика:</label>
            <input type="text" name="title" id="title" value="Мой график">
        </div>
        
        <button type="submit" class="btn">Построить график</button>
    </form>
    """
    
    return HTMLResponse(content=generate_html("Линейный график", "", form=form))

@app.post("/plot/line", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def plot_line(
    request: Request,
    function: str = Form(...),
    color: str = Form(...),
    style: str = Form(...),
    xmin: float = Form(...),
    xmax: float = Form(...),
    points: int = Form(...),
    title: str = Form("Мой график")
):
    """Построение линейного графика с заданными параметрами"""
    
    # Проверка лимитов
    if not SLOWAPI_AVAILABLE:
        if not simple_limiter.check_limit(f"{request.client.host}:/plot/line", 5, 60):
            return HTMLResponse(content=generate_html(
                "Ошибка",
                "<h2 style='color:red'>Превышен лимит запросов!</h2><p>Подождите минуту.</p>"
            ))
    
    # Создаем данные
    x = np.linspace(xmin, xmax, points)
    
    # Вычисляем функцию
    if function == "sin":
        y = np.sin(x)
        func_str = "sin(x)"
    elif function == "cos":
        y = np.cos(x)
        func_str = "cos(x)"
    elif function == "tan":
        y = np.tan(x)
        func_str = "tan(x)"
    elif function == "exp":
        y = np.exp(x)
        func_str = "exp(x)"
    elif function == "log":
        x = np.linspace(max(0.1, xmin), xmax, points)  # log не определен для <=0
        y = np.log(x)
        func_str = "log(x)"
    elif function == "sqrt":
        x = np.linspace(max(0, xmin), xmax, points)  # sqrt не определен для <0
        y = np.sqrt(x)
        func_str = "sqrt(x)"
    elif function == "x^2":
        y = x**2
        func_str = "x²"
    elif function == "x^3":
        y = x**3
        func_str = "x³"
    else:
        y = x
        func_str = "x"
    
    # Строим график
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, y, color=color, linestyle=style, linewidth=2, label=func_str)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    img_base64 = fig_to_base64(fig)
    
    result = f"""
    <h3>Результат:</h3>
    <p>Функция: <strong>{func_str}</strong></p>
    <p>Диапазон: [{xmin}, {xmax}]</p>
    <p>Точек: {points}</p>
    <p><a href="/interactive/line" class="btn btn-secondary">Построить другой</a></p>
    """
    
    return HTMLResponse(content=generate_html("Результат", result, img_base64))

@app.get("/interactive/bar", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def bar_form(request: Request):
    """Форма для столбчатой диаграммы"""
    remaining = simple_limiter.get_remaining(request.client.host, 5, 60) if not SLOWAPI_AVAILABLE else 5
    
    form = f"""
    <h2>📊 Столбчатая диаграмма</h2>
    <div class="info-box">
        <p>Осталось запросов: <strong>{remaining}/5</strong> в минуту</p>
    </div>
    
    <form action="/plot/bar" method="post" class="form-container">
        <div class="form-group">
            <label for="categories">Категории (через запятую):</label>
            <input type="text" name="categories" id="categories" value="Python, JavaScript, Java, C++" required>
        </div>
        
        <div class="form-group">
            <label for="values">Значения (через запятую):</label>
            <input type="text" name="values" id="values" value="95, 90, 85, 80" required>
        </div>
        
        <div class="form-group">
            <label for="color_scheme">Цветовая схема:</label>
            <select name="color_scheme" id="color_scheme">
                <option value="viridis">Viridis</option>
                <option value="plasma">Plasma</option>
                <option value="inferno">Inferno</option>
                <option value="magma">Magma</option>
                <option value="cividis">Cividis</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="title">Название:</label>
            <input type="text" name="title" id="title" value="Популярность языков программирования">
        </div>
        
        <div class="form-group">
            <label for="show_values">Показывать значения:</label>
            <input type="checkbox" name="show_values" id="show_values" checked>
        </div>
        
        <button type="submit" class="btn">Построить диаграмму</button>
    </form>
    """
    
    return HTMLResponse(content=generate_html("Столбчатая диаграмма", "", form=form))

@app.post("/plot/bar", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def plot_bar(
    request: Request,
    categories: str = Form(...),
    values: str = Form(...),
    color_scheme: str = Form("viridis"),
    title: str = Form("Столбчатая диаграмма"),
    show_values: bool = Form(False)
):
    """Построение столбчатой диаграммы"""
    
    # Парсим введенные данные
    cat_list = [c.strip() for c in categories.split(',')]
    val_list = [float(v.strip()) for v in values.split(',')]
    
    # Проверяем, что количество совпадает
    if len(cat_list) != len(val_list):
        return HTMLResponse(content=generate_html(
            "Ошибка",
            "<h2 style='color:red'>Количество категорий и значений должно совпадать!</h2>"
        ))
    
    # Строим график
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.get_cmap(color_scheme)(np.linspace(0.2, 0.9, len(cat_list)))
    bars = ax.bar(cat_list, val_list, color=colors, edgecolor='black', linewidth=1)
    
    if show_values:
        for bar, val in zip(bars, val_list):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(val_list)*0.01,
                   f'{val:.1f}', ha='center', va='bottom', fontweight='bold')
    
    ax.set_ylabel('Значения')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    img_base64 = fig_to_base64(fig)
    
    result = f"""
    <h3>Результат:</h3>
    <p>Категории: {', '.join(cat_list)}</p>
    <p>Значения: {', '.join([str(v) for v in val_list])}</p>
    <p><a href="/interactive/bar" class="btn btn-secondary">Построить другую</a></p>
    """
    
    return HTMLResponse(content=generate_html("Результат", result, img_base64))

@app.get("/interactive/pie", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def pie_form(request: Request):
    """Форма для круговой диаграммы"""
    remaining = simple_limiter.get_remaining(request.client.host, 5, 60) if not SLOWAPI_AVAILABLE else 5
    
    form = f"""
    <h2>🥧 Круговая диаграмма</h2>
    <div class="info-box">
        <p>Осталось запросов: <strong>{remaining}/5</strong> в минуту</p>
    </div>
    
    <form action="/plot/pie" method="post" class="form-container">
        <div class="form-group">
            <label for="labels">Названия секторов (через запятую):</label>
            <input type="text" name="labels" id="labels" value="Продажи, Маркетинг, Разработка, Администрация" required>
        </div>
        
        <div class="form-group">
            <label for="sizes">Размеры секторов (через запятую):</label>
            <input type="text" name="sizes" id="sizes" value="40, 25, 20, 15" required>
        </div>
        
        <div class="form-group">
            <label for="explode">Выделить сектор (номер, начиная с 0):</label>
            <input type="number" name="explode" id="explode" min="-1" max="10" value="-1">
            <small>Оставьте -1, чтобы не выделять</small>
        </div>
        
        <div class="form-group">
            <label for="title">Название:</label>
            <input type="text" name="title" id="title" value="Распределение бюджета">
        </div>
        
        <div class="form-group">
            <label for="shadow">Добавить тень:</label>
            <input type="checkbox" name="shadow" id="shadow" checked>
        </div>
        
        <button type="submit" class="btn">Построить диаграмму</button>
    </form>
    """
    
    return HTMLResponse(content=generate_html("Круговая диаграмма", "", form=form))

@app.post("/plot/pie", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def plot_pie(
    request: Request,
    labels: str = Form(...),
    sizes: str = Form(...),
    explode: int = Form(-1),
    title: str = Form("Круговая диаграмма"),
    shadow: bool = Form(False)
):
    """Построение круговой диаграммы"""
    
    # Парсим данные
    label_list = [l.strip() for l in labels.split(',')]
    size_list = [float(s.strip()) for s in sizes.split(',')]
    
    if len(label_list) != len(size_list):
        return HTMLResponse(content=generate_html(
            "Ошибка",
            "<h2 style='color:red'>Количество названий и размеров должно совпадать!</h2>"
        ))
    
    # Настройка explode
    explode_list = [0] * len(size_list)
    if 0 <= explode < len(size_list):
        explode_list[explode] = 0.1
    
    # Строим график
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = plt.cm.Set3(np.linspace(0, 1, len(size_list)))
    
    wedges, texts, autotexts = ax.pie(
        size_list, 
        labels=label_list,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        shadow=shadow,
        explode=explode_list if any(explode_list) else None
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.axis('equal')
    
    img_base64 = fig_to_base64(fig)
    
    total = sum(size_list)
    result = f"""
    <h3>Результат:</h3>
    <p>Всего: {total:.1f}</p>
    <p><a href="/interactive/pie" class="btn btn-secondary">Построить другую</a></p>
    """
    
    return HTMLResponse(content=generate_html("Результат", result, img_base64))

@app.get("/interactive/scatter", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def scatter_form(request: Request):
    """Форма для диаграммы рассеяния"""
    remaining = simple_limiter.get_remaining(request.client.host, 5, 60) if not SLOWAPI_AVAILABLE else 5
    
    form = f"""
    <h2>🔵 Диаграмма рассеяния</h2>
    <div class="info-box">
        <p>Осталось запросов: <strong>{remaining}/5</strong> в минуту</p>
    </div>
    
    <form action="/plot/scatter" method="post" class="form-container">
        <div class="form-group">
            <label for="n_points">Количество точек:</label>
            <input type="number" name="n_points" id="n_points" min="10" max="500" value="100" required>
        </div>
        
        <div class="form-group">
            <label for="correlation">Сила корреляции (0-1):</label>
            <input type="range" name="correlation" id="correlation" min="0" max="1" step="0.1" value="0.7">
            <output for="correlation" id="correlation_val">0.7</output>
        </div>
        
        <div class="form-group">
            <label for="color_by">Цвет точек по:</label>
            <select name="color_by" id="color_by">
                <option value="x">Значению X</option>
                <option value="y">Значению Y</option>
                <option value="density">Плотности</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="title">Название:</label>
            <input type="text" name="title" id="title" value="Диаграмма рассеяния">
        </div>
        
        <button type="submit" class="btn">Построить</button>
    </form>
    
    <script>
        const correlation = document.getElementById('correlation');
        const output = document.getElementById('correlation_val');
        correlation.addEventListener('input', function() {{
            output.value = this.value;
        }});
    </script>
    """
    
    return HTMLResponse(content=generate_html("Диаграмма рассеяния", "", form=form))

@app.post("/plot/scatter", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def plot_scatter(
    request: Request,
    n_points: int = Form(...),
    correlation: float = Form(...),
    color_by: str = Form("x"),
    title: str = Form("Диаграмма рассеяния")
):
    """Построение диаграммы рассеяния"""
    
    # Генерируем данные с заданной корреляцией
    np.random.seed(random.randint(1, 1000))
    
    mean = [0, 0]
    cov = [[1, correlation], [correlation, 1]]
    data = np.random.multivariate_normal(mean, cov, n_points)
    x, y = data[:, 0], data[:, 1]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if color_by == "x":
        colors = x
        cmap = 'plasma'
        color_label = 'Значение X'
    elif color_by == "y":
        colors = y
        cmap = 'viridis'
        color_label = 'Значение Y'
    else:
        # Плотность
        from scipy.stats import gaussian_kde
        xy = np.vstack([x, y])
        z = gaussian_kde(xy)(xy)
        colors = z
        cmap = 'hot'
        color_label = 'Плотность'
    
    scatter = ax.scatter(x, y, c=colors, s=50, alpha=0.6, cmap=cmap, edgecolor='black', linewidth=0.5)
    plt.colorbar(scatter, ax=ax, label=color_label)
    
    # Линия регрессии
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(sorted(x), p(sorted(x)), 'r--', linewidth=2, label=f'Линия тренда (r={correlation:.2f})')
    
    actual_corr = np.corrcoef(x, y)[0, 1]
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'{title} (корреляция: {actual_corr:.3f})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    img_base64 = fig_to_base64(fig)
    
    result = f"""
    <h3>Результат:</h3>
    <p>Точек: {n_points}</p>
    <p>Заданная корреляция: {correlation:.2f}</p>
    <p>Фактическая корреляция: {actual_corr:.3f}</p>
    <p><a href="/interactive/scatter" class="btn btn-secondary">Построить другую</a></p>
    """
    
    return HTMLResponse(content=generate_html("Результат", result, img_base64))

@app.get("/interactive/histogram", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def histogram_form(request: Request):
    """Форма для гистограммы"""
    remaining = simple_limiter.get_remaining(request.client.host, 5, 60) if not SLOWAPI_AVAILABLE else 5
    
    form = f"""
    <h2>📋 Гистограмма</h2>
    <div class="info-box">
        <p>Осталось запросов: <strong>{remaining}/5</strong> в минуту</p>
    </div>
    
    <form action="/plot/histogram" method="post" class="form-container">
        <div class="form-group">
            <label for="distribution">Тип распределения:</label>
            <select name="distribution" id="distribution" required>
                <option value="normal">Нормальное (Гаусса)</option>
                <option value="uniform">Равномерное</option>
                <option value="exponential">Экспоненциальное</option>
                <option value="poisson">Пуассона</option>
                <option value="binomial">Биномиальное</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="n_samples">Количество значений:</label>
            <input type="number" name="n_samples" id="n_samples" min="10" max="10000" value="1000" required>
        </div>
        
        <div class="form-group">
            <label for="bins">Количество интервалов:</label>
            <input type="number" name="bins" id="bins" min="5" max="100" value="30" required>
        </div>
        
        <div class="form-group">
            <label for="param1">Параметр 1:</label>
            <input type="number" name="param1" id="param1" step="any" value="0">
            <small>Для нормального: среднее</small>
        </div>
        
        <div class="form-group">
            <label for="param2">Параметр 2:</label>
            <input type="number" name="param2" id="param2" step="any" value="1">
            <small>Для нормального: std</small>
        </div>
        
        <div class="form-group">
            <label for="title">Название:</label>
            <input type="text" name="title" id="title" value="Гистограмма">
        </div>
        
        <button type="submit" class="btn">Построить</button>
    </form>
    """
    
    return HTMLResponse(content=generate_html("Гистограмма", "", form=form))

@app.post("/plot/histogram", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def plot_histogram(
    request: Request,
    distribution: str = Form(...),
    n_samples: int = Form(...),
    bins: int = Form(...),
    param1: float = Form(0),
    param2: float = Form(1),
    title: str = Form("Гистограмма")
):
    """Построение гистограммы"""
    
    np.random.seed(random.randint(1, 1000))
    
    # Генерируем данные в зависимости от распределения
    if distribution == "normal":
        data = np.random.normal(param1, param2, n_samples)
        dist_name = f"Нормальное (μ={param1}, σ={param2})"
    elif distribution == "uniform":
        data = np.random.uniform(param1, param2, n_samples)
        dist_name = f"Равномерное [{param1}, {param2}]"
    elif distribution == "exponential":
        data = np.random.exponential(1/param1 if param1 != 0 else 1, n_samples)
        dist_name = f"Экспоненциальное (λ={param1})"
    elif distribution == "poisson":
        data = np.random.poisson(max(param1, 0.1), n_samples)
        dist_name = f"Пуассона (λ={param1})"
    elif distribution == "binomial":
        n = int(max(param1, 1))
        p = min(max(param2, 0), 1)
        data = np.random.binomial(n, p, n_samples)
        dist_name = f"Биномиальное (n={n}, p={p:.2f})"
    else:
        data = np.random.randn(n_samples)
        dist_name = "Нормальное"
    
    fig, ax = plt.subplots(figsize=(12, 6))
    n, bins, patches = ax.hist(data, bins=bins, alpha=0.7, color='skyblue', 
                                edgecolor='black', density=True)
    
    # Добавляем теоретическую кривую для некоторых распределений
    if distribution == "normal":
        x = np.linspace(min(data), max(data), 100)
        y = 1/(param2 * np.sqrt(2*np.pi)) * np.exp(-(x-param1)**2/(2*param2**2))
        ax.plot(x, y, 'r-', linewidth=2, label='Теоретическая кривая')
        ax.legend()
    
    ax.set_xlabel('Значения')
    ax.set_ylabel('Плотность')
    ax.set_title(f'{title} - {dist_name}')
    ax.grid(True, alpha=0.3)
    
    img_base64 = fig_to_base64(fig)
    
    stats = {
        'mean': np.mean(data),
        'std': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        'median': np.median(data)
    }
    
    result = f"""
    <h3>Результат:</h3>
    <p>Распределение: {dist_name}</p>
    <p>Значений: {n_samples}</p>
    <p>Среднее: {stats['mean']:.3f}</p>
    <p>Стд. отклонение: {stats['std']:.3f}</p>
    <p>Медиана: {stats['median']:.3f}</p>
    <p><a href="/interactive/histogram" class="btn btn-secondary">Построить другую</a></p>
    """
    
    return HTMLResponse(content=generate_html("Результат", result, img_base64))

@app.get("/interactive/function", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def function_form(request: Request):
    """Форма для произвольной функции"""
    remaining = simple_limiter.get_remaining(request.client.host, 5, 60) if not SLOWAPI_AVAILABLE else 5
    
    form = f"""
    <h2>📐 Произвольная функция</h2>
    <div class="info-box">
        <p>Осталось запросов: <strong>{remaining}/5</strong> в минуту</p>
    </div>
    <p>Введите математическое выражение на Python (используйте x как переменную)</p>
    
    <form action="/plot/function" method="post" class="form-container">
        <div class="form-group">
            <label for="func">Функция f(x):</label>
            <input type="text" name="func" id="func" value="np.sin(x) * np.exp(-x/10)" required>
            <small>Примеры: x**2, np.sin(x), np.exp(-x), x**3 - 2*x + 1</small>
        </div>
        
        <div class="form-group">
            <label for="xmin">X от:</label>
            <input type="number" name="xmin" id="xmin" step="any" value="0" required>
        </div>
        
        <div class="form-group">
            <label for="xmax">X до:</label>
            <input type="number" name="xmax" id="xmax" step="any" value="10" required>
        </div>
        
        <div class="form-group">
            <label for="points">Количество точек:</label>
            <input type="number" name="points" id="points" min="10" max="1000" value="200" required>
        </div>
        
        <div class="form-group">
            <label for="title">Название:</label>
            <input type="text" name="title" id="title" value="Произвольная функция">
        </div>
        
        <button type="submit" class="btn">Построить</button>
    </form>
    """
    
    return HTMLResponse(content=generate_html("Произвольная функция", "", form=form))

@app.post("/plot/function", response_class=HTMLResponse)
@limiter.limit("5/minute")
async def plot_function(
    request: Request,
    func: str = Form(...),
    xmin: float = Form(...),
    xmax: float = Form(...),
    points: int = Form(...),
    title: str = Form("Произвольная функция")
):
    """Построение произвольной функции"""
    
    try:
        # Создаем данные
        x = np.linspace(xmin, xmax, points)
        
        # Безопасно вычисляем функцию
        namespace = {'x': x, 'np': np, 'sin': np.sin, 'cos': np.cos, 
                     'tan': np.tan, 'exp': np.exp, 'log': np.log,
                     'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e}
        y = eval(func, namespace)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(x, y, 'b-', linewidth=2, label=f'f(x) = {func}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        img_base64 = fig_to_base64(fig)
        
        result = f"""
        <h3>Результат:</h3>
        <p>Функция: f(x) = {func}</p>
        <p>Диапазон: [{xmin}, {xmax}]</p>
        <p>Min y: {np.min(y):.3f}</p>
        <p>Max y: {np.max(y):.3f}</p>
        <p><a href="/interactive/function" class="btn btn-secondary">Построить другую</a></p>
        """
        
        return HTMLResponse(content=generate_html("Результат", result, img_base64))
        
    except Exception as e:
        return HTMLResponse(content=generate_html(
            "Ошибка",
            f"<h2 style='color:red'>Ошибка в функции: {str(e)}</h2><p>Проверьте синтаксис.</p>"
        ))

@app.get("/test")
@limiter.limit("10/minute")
async def test_page(request: Request):
    """Страница для тестирования rate limiting"""
    remaining = simple_limiter.get_remaining(request.client.host, 10, 60) if not SLOWAPI_AVAILABLE else 10
    
    form = f"""
    <h2>⏱️ Тестирование Rate Limiting</h2>
    
    <div class="info-box">
        <p>Ваш IP: <strong>{request.client.host}</strong></p>
        <p>Осталось запросов на этой странице: <strong>{remaining}/10</strong></p>
        <h3>Как это работает:</h3>
        <p>Каждый endpoint имеет свой лимит запросов в минуту</p>
    </div>
    
    <div class="grid">
        <div class="card" onclick="window.open('/test/public', '_blank')">
            <h3>🔓 Публичный endpoint</h3>
            <p>20 запросов в минуту</p>
            <div class="limit-badge">20/мин</div>
        </div>
        
        <div class="card" onclick="window.open('/test/limited', '_blank')">
            <h3>🔒 Ограниченный endpoint</h3>
            <p>3 запроса в минуту</p>
            <div class="limit-badge">3/мин</div>
        </div>
        
        <div class="card" onclick="window.open('/interactive/line', '_blank')">
            <h3>📊 Графики</h3>
            <p>5 запросов в минуту</p>
            <div class="limit-badge">5/мин</div>
        </div>
    </div>
    
    <div style="background: #f5f5f5; padding: 20px; border-radius: 5px; margin-top: 30px;">
        <h3>Тест через curl:</h3>
        <pre>
# Быстро выполните эти команды в новом окне терминала:
curl http://localhost:8000/test/limited
curl http://localhost:8000/test/limited
curl http://localhost:8000/test/limited
curl http://localhost:8000/test/limited  # 4-я вернет ошибку
        </pre>
    </div>
    """
    
    return HTMLResponse(content=generate_html("Тестирование", "", form=form))

@app.get("/test/public")
@limiter.limit("20/minute")
async def test_public(request: Request):
    """Публичный тестовый endpoint"""
    remaining = simple_limiter.get_remaining(f"{request.client.host}:/test/public", 20, 60) if not SLOWAPI_AVAILABLE else 19
    
    return JSONResponse({
        "message": "Публичный endpoint",
        "limit": "20/минуту",
        "remaining": remaining,
        "ip": request.client.host,
        "time": datetime.now().isoformat()
    })

@app.get("/test/limited")
@limiter.limit("3/minute")
async def test_limited(request: Request):
    """Ограниченный тестовый endpoint"""
    remaining = simple_limiter.get_remaining(f"{request.client.host}:/test/limited", 3, 60) if not SLOWAPI_AVAILABLE else 2
    
    return JSONResponse({
        "message": "Ограниченный endpoint",
        "limit": "3/минуту",
        "remaining": remaining,
        "ip": request.client.host,
        "time": datetime.now().isoformat()
    })

# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    print("="*70)
    print("🚀 ИНТЕРАКТИВНАЯ ДЕМОНСТРАЦИЯ MATPLOTLIB + SLOWAPI")
    print("="*70)
    print(f"\n📊 Matplotlib: {matplotlib.__version__}")
    print(f"⏱️  SlowAPI: {'✅ УСТАНОВЛЕН' if SLOWAPI_AVAILABLE else '❌ НЕ УСТАНОВЛЕН (используется встроенный)'}")
    print("\n📌 ИНТЕРАКТИВНЫЕ СТРАНИЦЫ:")
    print("   🏠 http://localhost:8000 - Главная с выбором")
    print("   📈 /interactive/line - Линейный график")
    print("   📊 /interactive/bar - Столбчатая диаграмма")
    print("   🥧 /interactive/pie - Круговая диаграмма")
    print("   🔵 /interactive/scatter - Диаграмма рассеяния")
    print("   📋 /interactive/histogram - Гистограмма")
    print("   📐 /interactive/function - Произвольная функция")
    print("   ⏱️  /test - Тестирование лимитов")
    print("\n🎯 ЧТО МОЖНО ДЕЛАТЬ:")
    print("   ✅ Выбирать тип функции из списка")
    print("   ✅ Задавать цвета и стили")
    print("   ✅ Вводить свои значения")
    print("   ✅ Смотреть корреляцию в реальном времени")
    print("   ✅ Тестировать rate limiting")
    print("="*70)
    
    uvicorn.run(app, host="127.0.0.1", port=8000)