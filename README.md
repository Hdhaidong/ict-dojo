# ICT DOJO · KOSPI200 交易训练平台

**帮交易者摆脱亏损**——主打韩国股市（KOSPI200）的 ICT（Inner Circle Trader）方法论训练平台，AI 能力跑在**吴恩达博士开源的 [OpenWorker](https://github.com/andrewyng/openworker) 框架底座**上。

> **数据说明**：平台内所有行情均为算法实时生成的**合成数据**，仅用于教学与练习，不构成任何投资建议。

## 在线访问

**[https://hdhaidong.github.io/ict-dojo/](https://hdhaidong.github.io/ict-dojo/)**

由 GitHub Pages 托管，浏览器直接打开即用，训练进度保存在浏览器 localStorage。

**宣传片（15秒）**：在线观看 [hdhaidong.github.io/ict-dojo/ict-dojo-intro.mp4](https://hdhaidong.github.io/ict-dojo/ict-dojo-intro.mp4) · [下载 MP4](https://github.com/Hdhaidong/ict-dojo/raw/main/ict-dojo-intro.mp4)

在线版包含完整的核心训练闭环（课程 / 图表练习 / 回放复盘 / 日志）。**AI 功能**需要本地运行 OpenWorker，见下方「接入 OpenWorker AI 底座」。

## 训练闭环

```
课程学习（8节） → 图表标记练习 → K线逐根回放复盘 → AI 教练点评 → 交易日志沉淀
```

## 四大功能模块

### 1. 课程学习（8 节）

覆盖 ICT 体系核心概念，每课配有**算法实时检测并标注的图例**与随堂测验：

| 课 | 主题 | 图例标注 |
|---|---|---|
| 01 | 市场结构与 BOS / CHoCH | 摆动点 HH/HL/LH/LL、结构突破线 |
| 02 | 流动性与扫荡 | BSL/SSL 流动性池、扫荡K线 |
| 03 | 公允价值缺口 FVG | 看涨/看跌缺口色块 |
| 04 | 订单块 OB | 看涨/看跌订单块区域 |
| 05 | Killzone 时间窗 | 伦敦/纽约时段底纹 |
| 06 | 溢价与折价 | EQ 均衡价、Premium/Discount 分区 |
| 07 | SMT 背离 | EURUSD 与 DXY 双图对照 |
| 08 | 综合入场模型（2022 Model） | ①扫荡→②CHoCH→③FVG→④目标 全流程 |

### 2. 图表练习

算法每次生成**全新行情**，在图上**点击作答**，即时反馈并高亮正确答案：FVG / 订单块 / 流动性 / BOS / 扫荡识别 + 概念测验。每轮 5 题，自动统计正确率。

### 3. K线回放复盘

- 逐根推进行情（空格播放/暂停，←/→ 单根，支持 +10 跳跃）
- 任意时点做出**做多 / 做空 / 平仓**决策，图表自动标记进出场
- 结束自动结算：交易笔数、胜率、总盈亏、最大回撤、评级
- 权益曲线 + 可叠加 **ICT 参考标记**（FVG + 结构事件）对照判断
- 打标签 + 复盘笔记，全部归档进交易日志

### 4. 交易日志

所有复盘记录自动归档，支持删除，并汇总累计统计。

## 接入 OpenWorker AI 底座（吴恩达开源）

AI 三件套——**复盘教练 / 课程追问 / 定向出题**——由本地运行的 [OpenWorker](https://github.com/andrewyng/openworker)（吴恩达博士与 Rohit Prasad 开源的桌面 AI Agent，MIT 协议）提供模型能力。全程本地调用、自带模型 Key，数据不出本机。

### 快速接入（三步）

```bash
# ① 启动 OpenWorker 本地服务器（默认端口 8765）
#    方式A：安装 OpenWorker 桌面应用后启动本地 server
#    方式B：源码运行
git clone https://github.com/andrewyng/openworker
cd openworker && bash packaging/setup_dev_env.sh
.venv/Scripts/openworker-server --port 8765        # Windows
# .venv/bin/openworker-server --port 8765          # macOS/Linux

# ② 在 OpenWorker 中配置模型 API Key（OpenAI / Anthropic / DeepSeek / Ollama 本地模型等均可）

# ③ 从仓库根目录一键启动本地模式（自动注入令牌并打开浏览器）
python serve_local.py                  # 默认：页面 8080 ← OpenWorker 8765
python serve_local.py 8080 8913        # 自定义：OpenWorker 跑在其他端口时
```

`serve_local.py` 会读取 `%APPDATA%\coworker\sidecar-8765.token`（Windows）或 `~/.config/coworker/sidecar-8765.token`（macOS/Linux），把**令牌与服务器地址**注入页面后在 `http://localhost:8080` 提供服务；若用环境变量 `COWORKER_API_TOKEN` 自定义了启动令牌，也会被自动识别。页面对旧地址连不上时会**自动切换**到注入的地址。

### 模型与常见错误

- 连接成功后，可在「AI · OpenWorker」设置里指定**模型**（如 `deepseek:deepseek-v4-pro`、`gpt-5.6-sol`），留空则用服务器默认模型——多个账户时切换很方便。
- 调用报 **402 / 429（余额不足 / 账户未激活）**：说明 OpenWorker 里配置的模型账户需要充值，充值后在设置中指定该账户的模型名即可。
- 真实错误信息（含提供商返回的原因）会完整显示在页面上，便于排查。

### 为什么要从 localhost 打开？

OpenWorker 的本地服务器有浏览器来源门禁（只信任 `localhost` / 桌面端来源），因此：

| 打开方式 | 核心训练 | AI 三件套 |
|---|:-:|:-:|
| GitHub Pages 在线版 | ✓ | ✗（跨源限制） |
| 双击 index.html（file://） | ✓ | ✗（跨源限制） |
| `serve_local.py` / `python -m http.server` | ✓ | ✓ |

未连接 OpenWorker 时，AI 入口会显示接入指引，核心训练闭环完全不受影响。

### AI 三件套

| 功能 | 位置 | 说明 |
|---|---|---|
| ✦ AI 复盘教练 | 回放结算面板 | 汇总本局每笔交易、胜率/回撤/评级/标签/笔记，生成「亮点 / 问题 / 改进建议」点评 |
| ✦ AI 助教 | 每课底部 | 结合当前课程内容的多轮追问，可联系其他 ICT 概念 |
| ✦ AI 定向出题 | 图表练习页 | 分析各类型练习正确率与课程进度，针对薄弱概念动态生成 5 道选择题并计入统计 |

连接状态见侧栏底部「AI · OpenWorker」徽标，点击可配置服务器地址与令牌。

## 技术说明

- **单文件 HTML 应用**：无框架、无构建、无外部依赖，任何现代浏览器直接运行
- **自研 Canvas K线引擎**：滚轮缩放、拖动平移、十字线、标注层（区域/水平线/标签/交易标记）
- **算法合成行情**：基于「趋势 → 整理 → 操纵扫荡」状态机的行情生成器，天然产生 FVG、订单块、等高低点、流动性扫荡等教学特征；标的默认 **KOSPI200（韩国）**，另含 EURUSD / GBPUSD / NAS100 / XAUUSD / BTCUSD
- **ICT 特征检测器**：BOS/CHoCH、FVG、订单块、流动性池与扫荡的算法检测，课程图例与练习判分共用同一套检测器
- **OpenWorker AI 底座**：通过其 OpenAI 兼容接口 `POST /v1/chat/completions`（`X-OpenWorker-Token` 鉴权）调用本地模型，未连接时优雅降级
- **localStorage 进度持久化**：课程进度、练习统计、复盘日志、连续训练天数、AI 连接配置全部本地保存

## 免责声明

本平台为交易方法论学习与练习工具，主打韩国股市（KOSPI200）场景但内置行情均为合成数据，不代表任何真实市场，不构成投资建议。交易有风险，入市需谨慎。

---

Made with ICT concepts · OpenWorker AI · 单文件 · 零依赖 · MIT
