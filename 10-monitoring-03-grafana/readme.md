# 📘 Обобщённая документация по разворачиванию инфраструктуры мониторинга Prometheus + Grafana + Node Exporter через Terraform и Ansible.

## Общий смысл  
Данный проект автоматизирует развёртывание и настройку **стека мониторинга (Prometheus + Node Exporter + Grafana)** в **Yandex Cloud**.  
Terraform создаёт облачную инфраструктуру (сеть, виртуальные машины и правила безопасности), а Ansible конфигурирует установленные сервисы и настраивает их взаимную интеграцию.  

В итоге получается связка:  
- **Node Exporter** собирает метрики с серверов,  
- **Prometheus** агрегирует и хранит данные,  
- **Grafana** предоставляет визуализацию и дашборды.

Весь стек поднимается 5 командами!
1. `terraform apply` (из директории terraform)
2. `ansible-playbook -i ./inventories/hosts.yml ./install-prometheus.yml` (из директории ansible)
3. `ansible-playbook -i ./inventories/hosts.yml ./install-grafana.yml` (из директории ansible)
4. `ansible-playbook -i ./inventories/hosts.yml ./install-node-exporter.yml` (из директории ansible)
5. `ansible-playbook -i ./inventories/hosts.yml ./connected-node-exporter.yml` (из директории ansible)

***

## Основные шаги

### 1. Terraform (инфраструктура)
- Разворачивает VPC, подсети и security group с доступом на нужные порты (22, 80, 443, 9090, 9100, 3000).  
- Создаёт три ВМ:  
  - **Prometheus VM** – сбор и хранение метрик (порт 9090);  
  - **Node Exporter VM** – агент мониторинга ОС (порт 9100);  
  - **Grafana VM** – визуализация метрик (порт 3000).  
- Применяет cloud-init для настройки пользователей и ключей.  

<img width="2433" height="336" alt="Снимок экрана 2025-08-17 154803" src="https://github.com/user-attachments/assets/f450647a-b086-4eb3-8329-9e385aaca798" />

### 2. Ansible (конфигурация сервисов)

- **Prometheus**: установка бинарников, настройка директорий, добавление systemd‑сервиса.

<img width="1528" height="506" alt="Снимок экрана 2025-08-17 155607" src="https://github.com/user-attachments/assets/c91ff105-c730-4e00-82b6-a6bfa9b04614" />

- **Grafana**: установка пакета, конфигурация пользователя и папок, запуск systemd‑сервиса.

  При первом входе вводим учетные данные admin\admin. Будет предложено сменить пароль.

<img width="1181" height="860" alt="Снимок экрана 2025-08-17 155800" src="https://github.com/user-attachments/assets/4842b5ba-3e0c-4fc8-bced-abef88c32e93" />

  Добавляем в datasource наш сервер Prometheus.

<img width="1503" height="372" alt="Снимок экрана 2025-08-17 160130" src="https://github.com/user-attachments/assets/69c9f1f4-3bb2-4624-8ac4-958f10f66072" />

- **Node Exporter**: установка бинарника, настройка systemd‑сервиса.
- **Интеграция**: обновление `prometheus.yml`, добавление таргетов Node Exporter и перезапуск Prometheus.

<img width="1522" height="372" alt="image" src="https://github.com/user-attachments/assets/7bf97036-24e4-45bc-b20a-c0b3b9b54edd" />
  
ВАЖНО: не забывайте добавить в inventory hosts.yml внешние адреса ВМ! Grafana из официального репозитория в РФ не доступна. Пакет скачиваем с сервера Yandex.

***

## Результат
После `terraform apply` и запуска ansible‑playbook:  
- В облаке разворачивается инфраструктура с ВМ под Prometheus, Grafana и Node Exporter.  
- Все сервисы установлены и запущены как systemd‑службы.  
- Prometheus автоматически собирает метрики с Node Exporter, а Grafana готова для создания дашбордов.  
- Итоговая система — **готовый к работе стек мониторинга инфраструктуры**.  

***

## Настройка dashboard Grafana

Настроим минимальный dashboard Grafana для анализа информации из Prometheus (к которому подключен Node Exporter).

Будем использовать следующие panels:

1. Утилизация CPU для nodeexporter (в процентах, 100-idle);
  
  `100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance))`

2. CPULA 1/5/15;

`node_load1` 

`node_load5` 

`node_load15`
   
3. Количество свободной оперативной памяти;

`node_memory_MemAvailable_bytes` 
   
4. количество места на файловой системе.

`node_filesystem_free_bytes{mountpoint="/", fstype!~"tmpfs|overlay"}`

В результате получаем: 

<img width="2517" height="959" alt="Снимок экрана 2025-08-16 211616" src="https://github.com/user-attachments/assets/6b12bfae-40a4-490b-b011-57e6d788ffe5" />

Файл с конфигурацией в формате json

https://github.com/DioRoman/10-monitoring-03-grafana/blob/main/Best%20Dashboard-1755209095627.json

***

# 📘 Интеграция Grafana с Telegram для оповещений

## 🚀 Общий смысл
Интеграция позволяет получать оповещения (**alerts**) из Grafana напрямую в Telegram‑чат или группу через специально созданного бота.  

---

## 🔹 1. Создание Telegram-бота и получение API токена
1. В Telegram найдите бота **BotFather**.  
2. Отправьте ему команду:  

/newbot

# 📘 Интеграция Grafana с Telegram для оповещений

## 🚀 Общий смысл
Интеграция позволяет получать оповещения (**alerts**) из Grafana напрямую в Telegram‑чат или группу через специально созданного бота.  

---

## 🔹 1. Создание Telegram-бота и получение API токена
1. В Telegram найдите бота **BotFather**.  
2. Отправьте ему команду:  
   ```
   /newbot
   ```
3. Следуйте инструкциям: выберите имя и `username` (имя должно заканчиваться на `bot` или `_bot`).  
4. После создания BotFather вернёт **API токен** — сохраните его, он понадобится для настройки Grafana.  

---

## 🔹 2. Получение Chat ID
1. Создайте в Telegram группу или используйте существующую.  
2. Добавьте в неё вашего нового бота.  
3. Узнать Chat ID можно двумя способами:  
   - Через **web.telegram.org**: откройте группу, в адресной строке будет ID чата после символа `#` (например: `-123456789`).  
   - Через API:  
     ```
     https://api.telegram.org/bot/getUpdates
     ```
     В ответе найдите поле `chat -> id`.  

---

## 🔹 3. Настройка Grafana для отправки оповещений в Telegram
1. В Grafana откройте меню: **Alerting → Contact points**.  
2. Нажмите **+ Add contact point**.  
3. Укажите имя (например, `telegram_alerts`).  
4. В списке **Integration** выберите `Telegram`.  
5. Введите:  
   - **Bot API Token** — полученный от BotFather токен.  
   - **Chat ID** — ID группы/чата.  
6. Нажмите **Test** для проверки работы.  
7. Сохраните контактную точку.  

---

## 🔹 4. Подключение Telegram-уведомлений к правилам оповещений
1. Перейдите в Grafana: **Alerting → Alert rules**.  
2. Создайте новое правило или отредактируйте существующее.  
3. В разделе **Configure labels and notifications** выберите созданный контакт (`telegram_alerts`).  
4. Сохраните правило.

Скриншот правила, которое направляет сообщение в telegram-bot если instance не доступен больше минуты:

   <img width="2101" height="812" alt="Снимок экрана 2025-08-16 191700" src="https://github.com/user-attachments/assets/10dfc7bb-a50c-473d-961a-132ec442a9bd" />

Пример сообщения из telegram бота.

<img width="752" height="517" alt="Снимок экрана 2025-08-17 163037" src="https://github.com/user-attachments/assets/73b09c28-aa18-4906-a0ad-6912ec675575" />

---

## ✅ Результат
Теперь при срабатывании правил оповещений Grafana будет отправлять сообщения в ваш Telegram‑чат через созданного бота.  

После этого при срабатывании правил оповещения вы будете получать сообщения от бота в Telegram. 

Обратите внимание, что Telegram ограничивает длину сообщений 4096 UTF-8 символов, учитывайте это при формировании текстов оповещений.

Эти шаги обеспечивают стандартную интеграцию между Grafana и Telegram для получения alert-уведомлений.

# 📘 Требования для успешного развёртывания мониторинга через Terraform и Ansible

Для корректной работы всего проекта и успешного выполнения кода необходимо соблюсти следующие требования:

---

## 1. Предустановленные инструменты
- **Terraform**: должен быть установлен на рабочей машине (рекомендована актуальная версия, например, ≥1.4).
- **Ansible**: потребуется для конфигурации сервисов (рекомендована версия ≥2.10).
- **Python**: необходим для Ansible (рекомендована версия ≥3.7).
- **sshpass** (для работы Ansible с паролями, если используете, либо настройте SSH-ключи).
- **Git**: для клонирования модулей Terraform (если источник — репозиторий).

---

## 2. Подготовка инфраструктуры в Yandex Cloud
- **Доступ к Yandex Cloud** и наличие необходимых IAM‑прав (создание VPC, виртуальных машин, security group и т.д.).
- **Сервисный аккаунт** или авторизация через Yandex CLI — Ansible и Terraform должны иметь доступ к облаку.
- **Публичный SSH‑ключ** — необходимо указать в переменных Terraform и передать на создаваемые ВМ.

<details>
  <summary>Полезные команды</summary>

`cd /mnt/c/Users/rlyst/Netology/10-monitoring-03-grafana/terraform`

`terraform apply -auto-approve`

`ansible-playbook -i /mnt/c/Users/rlyst/Netology/10-monitoring-03-grafana/ansible/inventories/hosts.yml /mnt/c/Users/rlyst/Netology/10-monitoring-03-grafana/ansible/install-prometheus.yml`

`ansible-playbook -i /mnt/c/Users/rlyst/Netology/10-monitoring-03-grafana/ansible/inventories/hosts.yml /mnt/c/Users/rlyst/Netology/10-monitoring-03-grafana/ansible/install-grafana.yml`

`ansible-playbook -i /mnt/c/Users/rlyst/Netology/10-monitoring-03-grafana/ansible/inventories/hosts.yml /mnt/c/Users/rlyst/Netology/10-monitoring-03-grafana/ansible/install-node-exporter.yml`

`ansible-playbook -i /mnt/c/Users/rlyst/Netology/10-monitoring-03-grafana/ansible/inventories/hosts.yml /mnt/c/Users/rlyst/Netology/10-monitoring-03-grafana/ansible/connected-node-exporter.yml`

</details>
