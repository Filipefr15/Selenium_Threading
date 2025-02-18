import asyncio
async def greet(name):
    await asyncio.sleep(1)
    print(name)
async def main():
    await asyncio.gather(greet("Geeks"), greet("For"), greet("Geeks"))
