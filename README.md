# -Agent-[README.md](https://github.com/user-attachments/files/27227878/README.md)
# 🤖 智能合同风险审查 Multi-Agent 系统

> **Contract Risk Analysis System** powered by Claude API — Multi-Agent Architecture with Chain-of-Thought Reasoning

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Claude API](https://img.shields.io/badge/Claude-claude--sonnet--4-orange.svg)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 项目背景 / Background

企业法务与采购部门每日需审阅大量合同文本，人工审阅效率低、易漏判关键风险条款，且无法做到标准化输出。本项目通过**多Agent协作架构**，实现合同的自动化结构解析、链式风险推理和决策报告生成，将合同初审时间从平均4小时压缩至2分钟以内。

---

## 🏗️ 系统架构 / Architecture

```
用户输入合同文本
        │
        ▼
┌─────────────────────┐
│   CoordinatorAgent  │  ← 任务调度中枢
│   (任务拆分 & 汇总)  │
└──────────┬──────────┘
           │ 并发调度
     ┌─────┼─────┐
     ▼     ▼     ▼
┌────────┐ ┌──────────┐ ┌───────────┐
│ Parser │ │   Risk   │ │  Summary  │
│ Agent  │ │  Agent   │ │  Agent    │
│        │ │  (CoT)   │ │           │
│结构化  │ │链式推理  │ │决策报告  │
│信息提取│ │风险评估  │ │生成输出  │
└────────┘ └──────────┘ └───────────┘
     │          │              │
     └──────────┴──────────────┘
                │
                ▼
        最终风险报告 (JSON)
```

### Agent 职责说明

| Agent | 职责 | 推理方式 |
|-------|------|----------|
| **CoordinatorAgent** | 任务拆分、调度子Agent、汇总结果 | 规则调度 |
| **ParserAgent** | 从合同文本提取结构化关键信息 | Structured Output |
| **RiskAgent** | 对各条款进行多维度风险评估 | **Chain-of-Thought** |
| **SummaryAgent** | 生成执行摘要与签署建议 | 综合推理 |

---

## ⚡ 核心特性 / Features

- ✅ **Multi-Agent 协作** — 4个独立Agent串联协作，职责清晰，易于扩展
- ✅ **Chain-of-Thought 推理** — RiskAgent逐步推理每个条款的潜在风险，推理过程透明可审计
- ✅ **结构化输出** — 所有Agent输出严格JSON，便于系统集成与下游处理
- ✅ **全量日志** — 每次调用输出完整时间戳、Token消耗、响应耗时，便于监控
- ✅ **可扩展架构** — 新增Agent只需实现 `run()` 接口并在Coordinator中注册

---

## 🚀 快速开始 / Quick Start

### 1. 安装依赖

```bash
git clone https://github.com/your-username/contract-agent-system.git
cd contract-agent-system
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

或创建 `.env` 文件：
```
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. 运行系统

```bash
python main.py
```

### 4. 查看输出报告

结果自动保存至 `output/report_YYYYMMDD_HHMMSS.json`

---

## 📊 输出示例 / Sample Output

```
============================================================
  🤖 智能合同风险审查 Multi-Agent 系统
  Contract Risk Analysis — Powered by Claude API
============================================================
  启动时间: 2025-04-30 14:23:11
============================================================

[CoordinatorAgent] 🚀 启动多Agent协作流程...
[CoordinatorAgent] 任务拆分: Parser → Risk → Summary

[CoordinatorAgent] 📋 Step 1/3 — 调度 ParserAgent
  [ParserAgent] 开始解析合同结构...
  [ParserAgent] 调用 Claude API → 提取合同要素...
  [ParserAgent] API响应完成 | 耗时: 3.21s | Token消耗: 1,243
  [ParserAgent] ✅ 成功提取 11 个关键字段

[CoordinatorAgent] ⚠️  Step 2/3 — 调度 RiskAgent (链式推理)
  [RiskAgent] 执行多维度风险推理...
  [RiskAgent] API响应完成 | 耗时: 5.87s | Token消耗: 2,891
  [RiskAgent] ✅ 风险评估完成 | 综合风险评分: 62/100 | 等级: 中
  [RiskAgent] 发现风险点: 4 项 | 缺失条款: 3 项
     🔴 风险1: [高] 保密条款 — 赔偿上限过低仅10万元
     🟡 风险2: [中] 违约责任 — 5%违约金低于行业标准
     🟡 风险3: [中] 知识产权 — 未约定交付物验收标准
     🟢 风险4: [低] 不可抗力 — 3日通知期限偏短

[CoordinatorAgent] 📝 Step 3/3 — 调度 SummaryAgent
  [SummaryAgent] 整合各Agent结果，生成决策报告...
  [SummaryAgent] API响应完成 | 耗时: 2.43s | Token消耗: 687

  ==================================================
  📊 执行摘要: 合同整体风险中等，保密赔偿上限明显偏低...
  🖊️  建议: 建议修改后签署
  💰 风险敞口: 约10-50万元
  ==================================================

✅ 完整报告已保存至: output/report_20250430_142318.json
```

---

## 📁 项目结构 / Project Structure

```
contract-agent-system/
├── main.py                    # 主入口
├── requirements.txt           # 依赖
├── README.md
├── agents/
│   ├── __init__.py
│   ├── coordinator.py         # 调度中枢
│   ├── parser_agent.py        # 结构化解析Agent
│   ├── risk_agent.py          # CoT风险评估Agent
│   └── summary_agent.py       # 报告生成Agent
├── output/                    # 自动生成的报告目录
└── sample_docs/               # 示例合同文档
```

---

## 🔧 扩展方法 / How to Extend

新增一个Agent只需三步：

```python
# 1. 创建 agents/my_agent.py
class MyAgent:
    def __init__(self, api_key): ...
    def run(self, input_data) -> dict: ...

# 2. 在 coordinator.py 中导入并调用
from agents.my_agent import MyAgent
my_result = MyAgent(self.api_key).run(data)

# 3. 将结果加入最终返回
return { ..., "my_result": my_result }
```

---

## 📈 Token 消耗参考

| 场景 | 单次Token消耗 | 日处理量 | 日Token消耗 |
|------|--------------|----------|------------|
| 单份合同 (8条款) | ~5,000 tokens | 500份 | ~250万 |
| 复杂合同 (30条款) | ~15,000 tokens | 500份 | ~750万 |

---

## 📄 License

MIT License — 自由使用与修改，请保留原作者信息。
