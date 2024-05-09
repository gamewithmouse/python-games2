import asyncio

async def async_function():
    await asyncio.sleep(1)
    return "비동기 작업 완료"

async def main():
    result = await async_function()
    return result

returned_value = asyncio.run(main())
print("asdfasdf")
print("비동기 함수의 반환 값:", returned_value)
