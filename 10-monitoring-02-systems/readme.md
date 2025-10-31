### Задания 1-6

#### Ответы на вопросы

https://github.com/DioRoman/10-monitoring-02-systems/blob/main/answers.md

***

### Задание 7

#### Ключевые файлы

##### docker-compose

https://github.com/DioRoman/sandbox/blob/master/docker-compose.yml

##### telegraf

https://github.com/DioRoman/sandbox/blob/master/telegraf/telegraf.conf

#### Запуск Chronograf

<img width="2490" height="1280" alt="Снимок экрана 2025-08-11 203806" src="https://github.com/user-attachments/assets/d6d04949-e8ff-4912-b3d6-989b979ce2d2" />

***

### Задание 8

#### Смотрим метрики

<img width="2507" height="1230" alt="Снимок экрана 2025-08-11 232820" src="https://github.com/user-attachments/assets/14b77eb9-f58c-48b7-9971-dd0cc748a4e7" />

***

### Задание 9

#### Добавили плагин docker и видим метрики

<img width="1532" height="1191" alt="Снимок экрана 2025-08-12 220948" src="https://github.com/user-attachments/assets/c255af2d-e8c3-4ee6-9e89-eef0d07eafd0" />

PS: Обязательно даём права на /var/run/docker.sock. В первую очередь добавляем пользователя в группу docker, во вторую очередь внутри контейнера запускаем всё под root (или пользователем с аналогичными правами).

***

### Дополнительное задание (со звездочкой *)

#### Скрипт 

https://github.com/DioRoman/10-monitoring-02-systems/blob/main/metrics.py

#### Пояснения

- В скрипте собрано 5 метрик: загрузка CPU, загрузка RAM, загрузка диска, uptime системы и количество запущенных контейнеров.
- Метрики берутся частично из `/proc` (cpu, память, uptime), частично с помощью системных вызовов (`os.statvfs` для диска).
- Лог сохраняется в `/var/log/` с именем в формате `YY-MM-DD-awesome-monitoring.log`.
- Cron запускает скрипт каждую минуту, что позволяет избегать сложного управления циклом внутри скрипта, если сделать скрипт однократным (один сбор и выход). В приведенном примере скрипт работает в цикле с sleep 60, поэтому cron его можно вызывать один раз при старте сервера или как сервис.
- Подсчет контейнеров сделан по локальному пути docker-контейнеров, можно адаптировать под другую систему контейнеризации.

#### crontab -e

<img width="1105" height="640" alt="Снимок экрана 2025-08-12 230526" src="https://github.com/user-attachments/assets/9c93d1f2-4cda-451f-8311-f76007b712bf" />

#### cat /var/log

<img width="2075" height="734" alt="Снимок экрана 2025-08-12 230500" src="https://github.com/user-attachments/assets/6a6d0db9-8c88-4b88-9354-140552b46da1" />


<details>
  <summary>Полезные команды</summary>
  
`cd /mnt/c/Users/rlyst/Netology/10-monitoring-02-systems/sandbox`

`./sandbox up`

`* * * * * /usr/bin/env python3 /полный/путь/к/metrics.py`

</details>
