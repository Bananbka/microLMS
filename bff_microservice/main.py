from fastapi import FastAPI, HTTPException, Request
import httpx
import asyncio

app = FastAPI(title="MicroLMS BFF (API Composition)")


# 1. Замінюємо headers на cookies у допоміжній функції
async def fetch_service_data(client: httpx.AsyncClient, url: str, cookies: dict = None):
    try:
        # Передаємо куки у внутрішній запит
        response = await client.get(url, cookies=cookies, timeout=3.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        print(f"Помилка доступу до {url}: {e}")
        return None


@app.get("/api/bff/purchase-details/{user_id}/{course_id}/")
async def get_purchase_details(user_id: int, course_id: int, request: Request):
    # 2. Витягуємо токен з куки 'access-token', а не з заголовка
    access_token = request.cookies.get("access-token")

    # Формуємо словник з куками для httpx
    req_cookies = {}
    if access_token:
        req_cookies["access-token"] = access_token

    async with httpx.AsyncClient() as client:
        # Зверни увагу: я прибрав одне зайве /users/, яке було у тебе в логах
        # (в логах було /api/users/v1/users/users/1/)
        user_url = f"http://users-service:8001/api/users/v1/users/users/{user_id}/"
        course_url = f"http://courses-service:8002/api/courses/v1/courses/{course_id}/"

        # 3. Передаємо cookies=req_cookies в паралельні запити
        user_data, course_data = await asyncio.gather(
            fetch_service_data(client, user_url, cookies=req_cookies),
            fetch_service_data(client, course_url, cookies=req_cookies)
        )

        if user_data is None and course_data is None:
            raise HTTPException(
                status_code=503,
                detail="Core services are unavailable or unauthorized."
            )

        return {
            "aggregation_status": "success" if (user_data and course_data) else "partial_data",
            "student_info": user_data or {"error": "Users service is unavailable/unauthorized"},
            "course_info": course_data or {"error": "Courses service is unavailable/unauthorized"}
        }
