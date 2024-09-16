from datetime import datetime
from subprocess import run, PIPE

# Получаем текущую дату и время
now = datetime.now().strftime("%d-%m-%Y-%H:%M")

# Выполняем команду ps aux и сохраняем результат
result = run(["ps", "aux"], stdout=PIPE, text=True)
ps_output = result.stdout

# Анализируем вывод команды ps aux
lines = ps_output.strip().split("\n")
header = lines[0]
processes = lines[1:]

# Словарь для хранения информации о процессах
user_process_count = {}
total_memory = 0.0
total_cpu = 0.0
max_memory = (0.0, "")
max_cpu = (0.0, "")

for process in processes:
    cols = process.split(maxsplit=10)
    user = cols[0]
    cpu = float(cols[2])
    mem = float(cols[3])
    command = cols[10]

    # Подсчет процессов по пользователям
    if user in user_process_count:
        user_process_count[user] += 1
    else:
        user_process_count[user] = 1

    # Подсчет общего использования памяти и CPU
    total_memory += mem
    total_cpu += cpu

    # Определение процесса, занимающего больше всего памяти
    if mem > max_memory[0]:
        max_memory = (mem, command[:20])

    # Определение процесса, занимающего больше всего CPU
    if cpu > max_cpu[0]:
        max_cpu = (cpu, command[:20])

# Создаем отчет
report = f"""Отчёт о состоянии системы:
Пользователи системы: {', '.join(user_process_count.keys())}
Процессов запущено: {len(processes)}

Пользовательских процессов:
"""

for user, count in user_process_count.items():
    report += f"{user}: {count}\n"

report += f"""
Всего памяти используется: {total_memory:.1f}%
Всего CPU используется: {total_cpu:.1f}%
Больше всего памяти использует: ({max_memory[0]:.1f}% {max_memory[1]})
Больше всего CPU использует: ({max_cpu[0]:.1f}% {max_cpu[1]})
"""

# Сохраняем отчет в файл
filename = f"{now}-scan.txt"
with open(filename, "w") as file:
    file.write(report)


print(report)
