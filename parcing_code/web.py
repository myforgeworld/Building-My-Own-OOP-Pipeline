import asyncio
import json
from playwright.async_api import async_playwright

async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=False
        )

        context = await browser.new_context()

        page = await context.new_page()

        async def handle_response(response):

            try:
                url = response.url

                # Ловим GraphQL / API Airbnb
                if "graphql" in url or "StaysSearch" in url:

                    request = response.request
                    post_data = request.post_data

                    # Только запрос StaysSearch
                    if post_data and "StaysSearch" in post_data:

                        print("\n🔥 FOUND STAYS SEARCH")

                        # RESPONSE JSON
                        json_data = await response.json()

                        # СОХРАНЕНИЕ В ФАЙЛ
                        with open(
                            "airbnb_response.json",
                            "w",
                            encoding="utf-8"
                        ) as f:

                            json.dump(
                                json_data,
                                f,
                                ensure_ascii=False,
                                indent=4
                            )

                        print("✅ JSON SAVED -> airbnb_response.json")

            except Exception as e:
                print("ERROR:", e)

        page.on("response", handle_response)

        await page.goto(
            'https://www.airbnb.com/s/%D0%A2%D0%B0%D1%88%D0%BA%D0%B5%D0%BD%D1%82--%D0%A3%D0%B7%D0%B1%D0%B5%D0%BA%D0%B8%D1%81%D1%82%D0%B0%D0%BD/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJk1BMkb-KrjgRVNMnB0d5NC0&date_picker_type=calendar&query=%D0%A2%D0%B0%D1%88%D0%BA%D0%B5%D0%BD%D1%82%2C%20%D0%A3%D0%B7%D0%B1%D0%B5%D0%BA%D0%B8%D1%81%D1%82%D0%B0%D0%BD&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2026-06-01&monthly_length=3&monthly_end_date=2026-09-01&price_filter_input_type=2&channel=EXPLORE&pagination_search=true&price_filter_num_nights=5&federated_search_session_id=633cf677-8613-4273-bc8e-ec854773b31a&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjowLCJ2ZXJzaW9uIjoxfQ%3D%3D"',
            wait_until="networkidle"
        )

        # Ждем ответы API
        await page.wait_for_timeout(15000)

        await browser.close()

asyncio.run(main())