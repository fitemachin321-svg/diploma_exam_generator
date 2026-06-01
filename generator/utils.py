import random
import re

def parse_template(template_text):
    pattern = r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}'
    variables = re.findall(pattern, template_text)
    return list(set(variables))

def generate_random_value(var_name, context=None):
    if var_name in ['a', 'b', 'c']:
        return random.randint(1, 10) if var_name == 'a' else random.randint(-10, 10)
    return random.randint(1, 20)

def substitute_variables(template_text, variables_dict):
    result = template_text
    for var_name, var_value in variables_dict.items():
        result = result.replace(f'{{{var_name}}}', str(var_value))
    return result

def safe_eval_math(expr):
    expr = expr.replace(' ', '')
    if not re.match(r'^[\d\.\+\-\*\/\(\)]+$', expr):
        return None
    try:
        result = eval(expr.replace('^', '**'))
        if isinstance(result, float):
            result = round(result, 2)
            if result == -0.0:
                result = 0.0
        return str(result)
    except:
        return None

def solve_linear_equation(a, b):
    if a == 0:
        return "нет решения"
    x = round(-b / a, 2)
    if x == -0.0:
        x = 0.0
    return f"x = {x}"

def solve_quadratic_equation(a, b, c):
    if a == 0:
        return solve_linear_equation(b, c)
    D = b**2 - 4*a*c
    if D < 0:
        return "нет действительных корней"
    elif D == 0:
        x = round(-b / (2*a), 2)
        return f"x = {x}" if x != -0.0 else "x = 0"
    else:
        x1 = round((-b - D**0.5) / (2*a), 2)
        x2 = round((-b + D**0.5) / (2*a), 2)
        if x1 == -0.0:
            x1 = 0.0
        if x2 == -0.0:
            x2 = 0.0
        return f"x1 = {x1}, x2 = {x2}"

def extract_coefficients_simple(text):
    """Извлекает коэффициенты из строки вида '1x^2 + 10x + 3 = 0' или '3x + -7 = 0'."""
    text = text.replace(' ', '').replace('x²', 'x^2')
    # Убираем =0
    if text.endswith('=0'):
        text = text[:-2]
    # Ищем квадратный член
    a = 0
    b = 0
    c = 0
    # Квадратный член
    match_a = re.search(r'([+-]?\d*\.?\d*)x\^2', text)
    if match_a:
        a_str = match_a.group(1)
        if a_str == '' or a_str == '+':
            a = 1
        elif a_str == '-':
            a = -1
        else:
            a = float(a_str)
        # Удаляем его из текста, чтобы не мешал
        text = re.sub(r'[+-]?\d*\.?\d*x\^2', '', text)
    # Линейный член
    match_b = re.search(r'([+-]?\d*\.?\d*)x', text)
    if match_b:
        b_str = match_b.group(1)
        if b_str == '' or b_str == '+':
            b = 1
        elif b_str == '-':
            b = -1
        else:
            b = float(b_str)
        text = re.sub(r'[+-]?\d*\.?\d*x', '', text)
    # Свободный член (оставшееся число)
    if text:
        match_c = re.search(r'([+-]?\d*\.?\d+)', text)
        if match_c:
            c = float(match_c.group(1))
    return a, b, c

def generate_math_answer(template_text, variables_dict):
    # Если есть переменные (например, {a}x + {b} = 0)
    if variables_dict:
        expr = substitute_variables(template_text, variables_dict)
        res = safe_eval_math(expr)
        if res is not None:
            return res
        a = variables_dict.get('a')
        b = variables_dict.get('b')
        c = variables_dict.get('c')
        if 'x²' in template_text or 'x^2' in template_text:
            if a is not None and b is not None and c is not None:
                return solve_quadratic_equation(a, b, c)
        if 'x' in template_text and 'x²' not in template_text:
            if a is not None and b is not None:
                return solve_linear_equation(a, b)
        return expr
    # Нет переменных – обрабатываем как есть
    # Квадратное уравнение
    if 'x²' in template_text or 'x^2' in template_text:
        a, b, c = extract_coefficients_simple(template_text)
        if a != 0 or b != 0 or c != 0:
            return solve_quadratic_equation(a, b, c)
    # Линейное уравнение
    if 'x' in template_text and 'x²' not in template_text and 'x^2' not in template_text:
        a, b, c = extract_coefficients_simple(template_text)
        if b != 0:
            return solve_linear_equation(b, c)
    # Степень
    pow_match = re.search(r'(\d+)\^(\d+)', template_text)
    if pow_match:
        base = int(pow_match.group(1))
        exp = int(pow_match.group(2))
        result = round(base ** exp, 2)
        if result == -0.0:
            result = 0.0
        return str(result)
    # Проценты
    if 'процент' in template_text.lower() or '%' in template_text:
        nums = re.findall(r'\d+\.?\d*', template_text)
        if len(nums) >= 2:
            try:
                percent = float(nums[0])
                number = float(nums[1])
                result = number * percent / 100
                return str(round(result, 2))
            except:
                pass
    # Простая арифметика
    res = safe_eval_math(template_text)
    if res is not None:
        return res
    # Если ничего не подошло, возвращаем "Ответ не указан"
    return "Ответ не указан"

def generate_auto_test_question(question_template, variables_dict):
    question_text = substitute_variables(question_template.text_template, variables_dict)
    correct = question_template.correct_answer_template
    if correct:
        for var_name, var_value in variables_dict.items():
            correct = correct.replace(f'{{{var_name}}}', str(var_value))
    else:
        correct = "?"
    options = question_template.options_template
    wrong = "?"
    if options and len(options) > 1:
        wrong = options[1].get('text', '?')
        for var_name, var_value in variables_dict.items():
            wrong = wrong.replace(f'{{{var_name}}}', str(var_value))
    opts = [{"text": correct, "is_correct": True}, {"text": wrong, "is_correct": False}]
    random.shuffle(opts)
    full_question = question_text + "\n\n"
    for i, opt in enumerate(opts, 1):
        full_question += f"   {chr(64+i)}) {opt['text']}\n"
    return full_question, f"Правильный ответ: {correct}"