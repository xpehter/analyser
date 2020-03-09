# Тестовое задание
Сервис анализа логов для выявления аварии

### Легенда
В файлах u_exDDMMYY.log содержатся журналы сервиса, опубликованного в IIS.
Периодически возникают задержки в ответах. Единичные долгие ответы сервиса не являются критичными для клиентского приложения. Однако продолжительные цепочки вызовов с долгим ответом ведут к деградации клиентского приложения (аварии).

### Требуется
Создать сервис для анализа журналов:
1. В качестве средства кодирования использовать Python;
2. При помощи Ansible происходит сборка docker-образа с сервисом и запуск через docker-compose;
3. После запуска приложение работает в виде сервиса и "слушает" папку Input. При поступлении нового файла, происходит его анализ. Файлы не дописываются и попадают в папку в полном виде;
4. Сервис размещает результат работы в папку Output. В файле должна содержаться информация: время аварии, продолжительность аварии, причина (какие пороговые значения превышены и на сколько).

Пороговые значения для анализа файлов (длительность ответа, размер цепочки, и т.д.) выбрать самостоятельно.
Формат результирующих файлов выбрать самостоятельно.

Предоставить ссылку на git-репозиторий с исходным кодом.

#### Алгоритм
Сам анализ производится в "окне", "ширина" которого определяется переменной `coverage`. Считаем среднее арифметическое, элементов входящих в окно, если оно больше заданного значения переменной `incident_setting`, то пишем в лог о начале аварии, указывая время и дату. Соответственно если значение `incident_setting` меньше среднего арифметического, пишем в лог об окончании аварии, указывая время и дату.

#### Сделано
- Сам алгоритм, но ещё есть куда стремиться в плане точности.
- Мониторинг папки с логами и запуск анализа файла логов при его создании в папке.
- Вывод результата анализа в файл.
- Запуск скрипта в контейнере Docker Compose'ом, но есть нюанс.

#### Предстоит реализовать/починить
- Запуск контейнера Ansible'ом.
- Скрипт, запущенный в контейнере не анализирует файл с логами. Точно известно, что скрипт, "видит" появление нового файла и открывает его, однако считывание строк из файла не происходит. Нужно дальше отлаживать.
- Рефакторинг скрипта, т.к. сейчас он напоминает спагетти-код.
- При копировании файла логов в папку для анализа в Midnight Commander, анализ не запускается, однако если копировать через cp, то всё работает. Есть предположение, что помимо создания файла логов, нужно учитывать его изменение. Если, файл очень большой, то процесс его копирования займёт некоторое время, потому запускать анализ нужно после окончания изменения файла. В этом же случае стоит фиксировать в каком месте был завершён предыдущий анализ. В общем, тема большая и интересная.

### Результат
Полностью задание не выполнено.
