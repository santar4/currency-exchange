from exchange.tools import get_response
import aiohttp



async def all_currencies(exchange_currencies:list, currencies: list) -> tuple[list, list]:
    url = "https://api.frankfurter.dev/v2/currencies"
    data = await get_response(url)
    try:
        for item in data:
            currency = f"{item['iso_code']} - {item['name']}"
            exchange_currency = item['iso_code']
            currencies.append(currency)
            exchange_currencies.append(exchange_currency)

        return currencies, exchange_currencies
    except aiohttp.ClientError as e:
        raise Exception(f"Connection error while fetching currencies: {e}") from e
    except (KeyError, ValueError, TypeError, AttributeError) as e:
        raise Exception(f"Invalid data format from Frankfurter API: {e}") from e
    except Exception as e:
        raise Exception(f"Unexpected error while getting currencies: {e}") from e


async def currency_rate(base: str, quote: str) -> float:
    url = f"https://api.frankfurter.dev/v2/rate/{base}/{quote}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

        return data["rate"]
    except aiohttp.ClientError as e:
        raise Exception(f"Connection error: {e}")
    except (KeyError, ValueError, TypeError) as e:
        raise Exception(f"Invalid response from API: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error while getting rate {base}/{quote}: {e}")



async def convert_currency(amount: float, based_currency: str, quoted_currency: str) -> float:
    rate = await currency_rate(
        base=based_currency,
        quote=quoted_currency
    )
    value = amount * rate
    return value
