import requests
import concurrent.futures

# URL твого шлюзу
URL = "http://localhost:8080/api/users/v1/users/auth/login/"
TOTAL_REQUESTS = 500
CONCURRENT_WORKERS = 10  # Кількість паралельних потоків


def send_request(req_id):
    try:
        # Робимо GET-запит
        response = requests.get(URL, timeout=2)
        return f"Запит {req_id}: HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Запит {req_id}: Помилка з'єднання ({e})"


if __name__ == "__main__":
    print(f"Починаємо атаку: {TOTAL_REQUESTS} запитів на {URL}...")

    # Запускаємо запити паралельно
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
        results = executor.map(send_request, range(1, TOTAL_REQUESTS + 1))

        # Виводимо результати по мірі їх виконання
        for result in results:
            print(result)

    print("\nГотово! Йди перевіряти дашборд у Grafana 🚀")