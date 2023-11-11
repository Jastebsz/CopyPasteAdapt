



![LOGO](https://storage.blackterminal.com/source/img/emitents/background_img_logo/1/2VNzTGsSAtMWkjd1czBI5JXSmv0S-So8.jpg)

<h1 align="center">CopyPasteAdapt</h1>
<h1 align="center"><a href="http://188.242.135.131:5000/">Live Demo</a></h21>
<h2 align="center">Решение команды RA1NF0RCE по задаче №2</h2>


[![Описание](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=008BFF&background=2DFFDA00&width=435&lines=%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5)](https://git.io/typing-svg)

Наше решение основано на фреймворке Flask, позволяет администратору в автоматияеском режиме распределять задачи между сотрудниками банка. Ресурс рабоает а паре с мобилным приложением для сотрудников,созданном на фреимворке Flutter

В данный момент до конца реализованы только первые 3 парсера

Для хранения и быстрого поиска информации на Web-ресурсе была использована база данных Elasticsearch.

Ссылки на используемые ресурсы в приложении:
1. Основной сервер приложения: http://188.242.135.131:5000/
2.

[![Порядок установки и запуска](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=008BFF&background=2DFFDA00&width=435&lines=%D0%9F%D0%BE%D1%80%D1%8F%D0%B4%D0%BE%D0%BA+%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8+%D0%B8+%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D0%B0)](https://git.io/typing-svg)

Для удобства Вы можете воспользоваться ссылками выше для проверки работоспособности решения.

Если Вы хотите развернуть сервер на локальном компьютере, проделайте следующие шаги:
1. Загрузите проект с помощью любого редактора кода (Например VSCode с расширением GitLens)
```
git clone https://github.com/Andruxa0/ra1nf0rce_case2.git
```
1. Создайте новое виртуальное окружение, прописав в терминале команды:
```
python -m venv venv
venv\scripts\activate
```
Если у Вас возникла ошибка, откройте PowerShell с правами администратора и пропишите команды:
```
Set-ExecutionPolicy RemoteSigned
A
```
1. Установите все необходимые зависимости, указанные в файле requirements.txt, с помощью команды:
```
pip install -r requirements.txt
```
1. Убедитесь, что Elasticsearch запущен на вашем компьютере. Для этого необходимо:

4.1. Скачать docker c официального сайта https://www.docker.com/products/docker-desktop/ и установить его

4.2. Распаковать архив ra1nf0rce_elastic_base.rar

4.3. Обязательно запустить VPN на машине для выполнения следующих команд

4.4. Зайти в папку ra1nf0rce_elastic_base через cmd, используя команду 
```
cd C:\path_to_ra1nf0rce_elastic_base\ra1nf0rce_elastic_base
```
4.5. Прописать команду 
```
docker-compose up
```
4.6. После окончания установки, запустить контейнер elastic10

5. Запустите приложение, используя команду:
```
flask run
```
6. Откройте браузер и перейдите по адресу http://localhost:5000. Вы увидите домашнюю страницу приложения, позволяющую выбрать ресурс, продукты с которого будет просматривать оператор.
7. Оператор имеет возможность производить поиск необходимых комплектующих, вводя необходимые названия в строку поиска, выгружать результаты работы парсера в формате .xlsx, а также запускать работу парсеров-по соответсвующим кнопкам.

[![Сценарий использования](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=008BFF&background=2DFFDA00&width=435&lines=%D0%A1%D1%86%D0%B5%D0%BD%D0%B0%D1%80%D0%B8%D0%B9+%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F)](https://git.io/typing-svg)

## Сценарий 1: выбор ресурса для просмотра комплектующих

| Действия оператора | Результат |
|------------|---------------------|
 Ввести название ресурса ( уже внедренного для парсинга) или выбрать из списка вариантов |Переход на страницу с просмотром комплектующих на данном ресурсе

## Сценарий 2: поиск комплектующих в базе данных 

| Шаг | Действия оператора | Результат |
|-----|------------|---------------------|
| 1   | Ввести название в комплектующего в  строку поиска           | В результате будет сгенерирована страница со всеми подходящими комлектующими на выбранном ресурсе |
| 2    | Перейти к необходимому комплектующему           | В результате будет сгенерирована страница с ссылкой на комплектующее, его категорией, при пролистывании страницы пользователь получает информацию о характеристиках комплектующего. Характеристики отслеживаются с помощью проверки изменений с прошлого обновления базы данных|

## Сценарий 3: выбор категории для поиска

| Действия оператора | Результат |
|------------|---------------------|
| Выбрать фильтр поиска из предложенных в док-баре          | В результате будет сгенерирована страница со всеми подходящими комлектующими на выбранном ресурсе с выбранными фильтрами |

## Сценарий 4: выгрузка базы данных

| Действия оператора | Результат |
|------------|---------------------|
|Нажать на клавишу «Выгрузить базу данных»|Производится выгрузка базы данных в формате .xlsx

## Сценарий 5: обновление базы данных

| Действия оператора | Результат |
|------------|---------------------|
|Нажать на клавишу «Обновить базу данных»|Производится обновление базы данных всеми доступными парсерами, при запуске и окончании обновления появляются соответствующие уведомления. Обновление базы данных занимает продолжительное время (от 2 часов). Чтобы получить уведомление об окончании парсинга, необходимо не обновлять страницу, с которой было запущено обновление.

[![Проблемы](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=FF040F&width=435&lines=%D0%92%D0%BE%D0%B7%D0%BC%D0%BE%D0%B6%D0%BD%D1%8B%D0%B5+%D0%BF%D1%80%D0%BE%D0%B1%D0%BB%D0%B5%D0%BC%D1%8B)](https://git.io/typing-svg)

В этом разделе описаны известные проблемы, которые могут возникнуть при работе с проектом.

- **Проблема 1:** Некоторые функции могут работать неправильно на определенных версиях Python.
  - **Решение:** Убедитесь, что у вас установлена подходящая версия Python и обновите ее, если необходимо.

- **Проблема 2:** Некоторые файлы могут отсутствовать или быть повреждены после загрузки проекта.
  - **Решение:** Попробуйте загрузить проект заново или проверьте целостность файлов вручную.

- **Проблема 3:** Работоспособность парсеров зависит от нагруженности ресурсов, возможны ошибки при их запуске.
  - **Решение:** Перезапустите проект.

- **Проблема 4:** При большом количестве запусков парсера с одного устройства возможно попдание в черный список ресурса.
  - **Решение:** В случае поподания в черный список используйте VPN.

- **Проблема 5:** В данный момент обновление баз настроено на локальную базу elasticsearsh. При открытии сайта по адресу http://188.242.135.131:5000/, обновление базы может быть недоступно.
  - **Решение:** Разверните проект на локальной машине по инструкции выше.

- **Проблема 6:** В данный момент страница плохо адаптирована под мобильные телефоны.
  - **Решение:** Откройте страницу на компьютере

Проект находится в процессе активной разработки, возможны определенные ошибки и недоработки. В силу ограниченности временных ресурсов, база данных не была заполнена полностью. В дальнейшем планируется полная упаковка всего проекта в докер контейнер.



![](https://github.com/Platane/snk/raw/output/github-contribution-grid-snake.svg)