# MultiLayerAttackTool - 高并发多层混合攻击模拟工具

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Win%2FLinux%2FmacOS-lightgrey?style=for-the-badge)

```
    __  ___      __  _           __    _      __        __          _        
   /  |/  /___ _/ /_(_)___  ____/ /   (_)____/ /_  ____/ /__  _____(_)___  __
  / /|_/ / __ `/ __/ / __ \/ __  /   / / ___/ __ \/ __  / _ \/ ___/ / __ \/ /
 / /  / / /_/ / /_/ / / / / /_/ /   / / /__/ / / / /_/ /  __/ /  / / /_/ / / 
/_/  /_/\__,_/\__/_/_/ /_/\__,_/   /_/\___/_/ /_/\__,_/\___/_/  /_/\____/_/  
                                                                             
```

## 🚀 工具概述

MultiLayerAttackTool 是一款专为红队攻防演练和网络安全研究设计的高性能异步多层混合攻击模拟框架。集成了四层攻击向量，采用先进的异步IO架构，可实现极致的网络压力测试。

## ⚡ 核心特性

- 🔥 **四维一体混合打击** - 同时发动传输层、网络层、会话层和应用层攻击
- ⚡ **异步高并发引擎** - 基于asyncio + 线程池 + 进程池三级加速
- 🎯 **智能流量控制** - 精确到毫秒级的发包频率调控
- 📊 **实时性能监控** - 内置连接状态追踪和成功率统计
- 🛡️ **隐形模式** - 随机UA代理和IP伪装支持（需配置）
- 🔧 **模块化设计** - 支持攻击模块热插拔和自定义扩展

## 🛠️ 技术架构

```python
# 异步核心引擎架构
async def attack_controller():
    with ThreadPoolExecutor(max_workers=1000) as executor:
        with ProcessPoolExecutor() as process_executor:
            # 三级并发架构：协程 → 线程 → 进程
            tasks = [asyncio.create_task(attack_vector) for _ in range(concurrency)]
            await asyncio.gather(*tasks)
```

## 📦 安装部署

### 环境要求
- Python 3.7+
- Raw Socket权限（Linux需sudo）
- 高速网络连接

### 快速安装
```bash
# 克隆项目
git clone https://github.com/your-username/MultiLayerAttackTool.git
cd MultiLayerAttackTool

# 安装依赖
pip install -r requirements.txt

# 授予权限（Linux）
chmod +x multilayer_attack.py
```

```

## 💥 使用指南

### 基础用法
```bash
# 全面打击模式
python multilayer_attack.py -ip 192.168.1.100 -port 80 -speed 900 -concurrency 500

# 精确打击模式
python multilayer_attack.py -ip 10.0.0.50 -port 443 -speed 700 -concurrency 300 -timeout 10
```

### 高级参数
```bash
# 指定攻击类型
--attack-type [all|udp|icmp|syn|http]  # 选择攻击模式

#  stealth模式
--stealth-mode          # 启用隐形模式
--random-source         # 随机源IP（需要root）

# 性能调优
--worker-threads 2000   # 调整工作线程数
--packet-size 1024      # 自定义数据包大小
```

### 配置文件
创建 `config.ini` 进行持久化配置：
```ini
[attack]
default_speed = 800
max_workers = 2000
timeout = 5

[stealth]
random_user_agent = true
fake_ip_header = true
```

## 🎯 攻击模块详解

### 1. UDP洪水攻击 (`udp_flood_async`)
- **作用**：饱和目标带宽
- **协议**：UDP/传输层
- **特征**：无连接高速发包

### 2. ICMP死亡之Ping (`icmp_flood_async`) 
- **作用**：耗尽网络资源
- **协议**：ICMP/网络层
- **特征**：超大包攻击

### 3. SYN洪水攻击 (`syn_flood_async`)
- **作用**：耗尽连接池
- **协议**：TCP/会话层
- **特征**：半开连接攻击

### 4. HTTP洪水攻击 (`http_flood_async`)
- **作用**：应用层压测
- **协议**：HTTP/应用层
- **特征**：模拟真实流量

## 📊 性能指标

| 攻击类型 | 发包速率 | 并发能力 | 隐蔽性 |
|---------|---------|---------|--------|
| UDP洪水 | 10万+/秒 | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| ICMP洪水 | 8万+/秒  | ⭐⭐⭐⭐ | ⭐ |
| SYN洪水 | 6万+/秒  | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| HTTP洪水 | 3万+/秒  | ⭐⭐⭐ | ⭐⭐⭐⭐ |

## ⚠️ 法律免责声明

```ascii
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█                             █
█   ⚠️ 法律警示与免责声明 ⚠️   █
█                             █
█ 1. 本工具仅用于授权测试和教育研究  █
█ 2. 禁止用于未授权的网络攻击       █  
█ 3. 使用者需自行承担所有法律责任    █
█ 4. 开发者不对任何滥用行为负责     █
█                             █
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
```

**使用前提**：
- [ ] 已获得目标系统书面授权
- [ ] 在隔离测试环境中使用
- [ ] 了解当地网络安全法律法规
- [ ] 具备足够的网络管理权限

## 🤝 贡献指南

欢迎提交Issue和Pull Request！贡献内容包括：
- 新的攻击向量模块
- 性能优化建议
- 隐蔽性增强方案
- 文档改进和翻译

## 📜 开源协议

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🐛 问题反馈

遇到问题？请通过以下方式反馈：
1. 查看 [FAQ](docs/FAQ.md)
2. 提交 [Issue](https://github.com/your-username/MultiLayerAttackTool/issues)
3. 联系维护者：security@example.com

---

**最后提醒**：技术是一把双刃剑，请务必在法律和道德框架内使用本工具。White Hat Hackers save the world! 🎩

```
           _.-;;-._
      '-..-'|   ||   |
      '-..-'|_.-;;-._|
      '-..-'|   ||   |
      '-..-'|_.-''-._|
```
