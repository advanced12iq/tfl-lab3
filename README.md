# ТФЯ ЛАБ3

## Описание

Для генерации слов принадлежащих грамматике фаззер приводит входную грамматику к НФХ, затем генерирует слова по матрице биграмм. Принадлежность слов грамматике определяется с помощью алгоритма Кока — Янгера — Касами.

## Компоненты

Проект состоит из следующего основного модуля:

-   **`fuzz.py`**: Содержит класс `Grammar`, который управляет чтением грамматики, её подготовкой к генерации и самой генерацией тестовых данных.

## Как использовать

1.  **Подготовка грамматики:**
    -   Грамматика должна быть определена в данном формате.
        ```
        [rule]::=[blank]*[NT][blank]*- >[blank]*([NT][blank]*|[T][blank]*)+(\|[blank]*([NT][blank]*|[T][blank]*)+)*[EOL]+
        [T] ::= [a - z]
        [NT] ::= [A - Z][0 - 9]?]\[[A - z]+ ([0 - 9])*\]
        ```

## Структура класса `Grammar`

Класс `Grammar` содержит следующие методы:

-   `__init__()`: Конструктор класса. Начальная инициализация переменных.
-   `readGrammar()`: Метод для чтения грамматики из стандартного потока. Он должен преобразовать грамматику в структуру данных, удобную для дальнейшего использования.
-   `prepareForGeneration()`: Метод для предварительной обработки грамматики, для построения промежуточных структур данных, необходимых для генерации.
-   `generate()`: Основной метод, который генерирует тестовые данные на основе грамматики. Он принимает следующие аргументы:
    -   `n`: (по умолчанию: 100) Количество тестовых строк, которые необходимо сгенерировать.
    -   `testing`: (по умолчанию: True) Если `True`, то будет генерироваться дополнительный файл verify_file.txt без разметки правильных ответов и будет выводится массив индексов слов принадлежащиъ языку для проверки правильности генерации на сайте https://web.stanford.edu/class/archive/cs/cs103/cs103.1156/tools/cfg/
    -   `allTerminals`: (по умолчанию: True) Если `True`, при генерации будут использоваться все возможные терминалы. Если `False`, то будут использоваться только терминалы, использованные в грамматике.
    -   `randomTerminalChance`: (по умолчанию: 0.1) Вероятность того, что при генерации будет выбран случайный терминал.
    -   `randomStopChance`: (по умолчанию: 0.15) Вероятность останвоки при генерации.
