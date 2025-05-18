import asyncio
from PIL import Image


async def main(name):
    print(f'Start {name}')
    im = Image.open(name)
    pixels = im.load()  # список с пикселями
    x, y = im.size  # ширина (x) и высота (y) изображения
    quarters = [{}, {}, {}, {}]
    avg = 0
    all_ = {}
    rgb = {}
    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            bright = r + g + b
            avg += bright
            all_[bright] = all_.get(bright, 0) + 1
            rgb[(r, g, b)] = rgb.get((r, g, b), 0) + 1
            if i > (x // 2) and j <= (y // 2):
                quarters[0][bright] = quarters[0].get(bright, 0) + 1
            elif i <= (x // 2) and j <= (y // 2):
                quarters[1][bright] = quarters[1].get(bright, 0) + 1
            elif i <= (x // 2) and j > (y // 2):
                quarters[2][bright] = quarters[2].get(bright, 0) + 1
            else:
                quarters[3][bright] = quarters[3].get(bright, 0) + 1

    await asyncio.sleep(0.1)

    avg /= (x * y)

    quarters = [{j: i[j] for j in i.keys() if j > avg} for i in quarters]
    all_ = {j: all_[j] for j in all_.keys() if j > avg}
    rgb = {j: rgb[j] for j in rgb.keys() if sum(j) > avg}

    percent = int(max(rgb.items(), key=lambda a: a[1])[1] * 100000 / (x * y))

    amount = 100 * sum(j for j in all_.values()) // (x * y)

    quarter = ['I', 'II', 'III', 'IV'][quarters.index(max(quarters, key=lambda a: sum(j for j in a.values())))]

    print(f'Done {name}, percent {percent}')
    print(f'Done {name}, amount {amount}')
    print(f'Done {name}, quarter {quarter}')
    print(f'Ready {name}')

    return name, percent, amount, quarter


async def asteroids(*args):
    tasks = [
        asyncio.create_task(main(i))
        for i in args
    ]
    results = await asyncio.gather(*tasks)
    return results
