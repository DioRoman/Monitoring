import os
import json
import time
from datetime import datetime

def get_cpu_usage():
    # Читаем информацию из /proc/stat и считаем загрузку CPU (напр. общая сумма "user", "nice", "system", "idle" и др.)
    with open('/proc/stat', 'r') as f:
        line = f.readline()
    parts = line.split()[1:]
    parts = list(map(int, parts))
    total = sum(parts)
    idle = parts[3]  # idle время
    return total, idle

def calc_cpu_percent(prev, curr):
    prev_total, prev_idle = prev
    curr_total, curr_idle = curr
    total_diff = curr_total - prev_total
    idle_diff = curr_idle - prev_idle
    cpu_usage = 100 * (total_diff - idle_diff) / total_diff if total_diff > 0 else 0
    return round(cpu_usage, 2)

def get_mem_usage():
    meminfo = {}
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            key, val = line.split(':')[0], line.split(':')[1].strip().split()[0]
            meminfo[key] = int(val)
    mem_total = meminfo.get('MemTotal', 0)
    mem_free = meminfo.get('MemFree', 0)
    mem_available = meminfo.get('MemAvailable', mem_free)
    used_percent = 100 * (mem_total - mem_available) / mem_total if mem_total > 0 else 0
    return round(used_percent, 2), mem_total, mem_available

def get_disk_usage():
    statvfs = os.statvfs('/')
    total = statvfs.f_blocks * statvfs.f_frsize
    free = statvfs.f_bfree * statvfs.f_frsize
    used = total - free
    usage_percent = 100 * used / total if total > 0 else 0
    return round(usage_percent, 2), total, used, free

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return int(uptime_seconds)

def get_container_count():
    # Пример простого подсчета контейнеров docker через наличие папок в /var/lib/docker/containers
    containers_path = '/var/lib/docker/containers'
    try:
        count = len([name for name in os.listdir(containers_path) if os.path.isdir(os.path.join(containers_path, name))])
    except Exception:
        count = 0
    return count

def main():
    log_dir = '/var/log'
    os.makedirs(log_dir, exist_ok=True)
    prev_cpu = get_cpu_usage()
    time.sleep(1)
    while True:
        timestamp = int(time.time())
        curr_cpu = get_cpu_usage()
        cpu_percent = calc_cpu_percent(prev_cpu, curr_cpu)
        prev_cpu = curr_cpu
        mem_percent, mem_total_kb, mem_avail_kb = get_mem_usage()
        disk_percent, disk_total, disk_used, disk_free = get_disk_usage()
        uptime_sec = get_uptime()
        container_count = get_container_count()

        metrics = {
            'timestamp': timestamp,
            'cpu_usage_percent': cpu_percent,
            'memory_usage_percent': mem_percent,
            'disk_usage_percent': disk_percent,
            'uptime_seconds': uptime_sec,
            'containers_running': container_count
        }

        log_filename = datetime.now().strftime('%y-%m-%d-awesome-monitoring.log')
        log_path = os.path.join(log_dir, log_filename)
        with open(log_path, 'a') as f:
            f.write(json.dumps(metrics) + '\n')

        # Сбор раз в минуту
        time.sleep(60)

if __name__ == '__main__':
    main()