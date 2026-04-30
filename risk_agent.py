"""
Risk Agent — 链式推理风险评估
基于 Chain-of-Thought 对合同条款进行多维度风险分析
"""

import json
import anthropic


class RiskAgent:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.name = "RiskAgent"
        self.model = "claude-sonnet-4-20250514"

    def log(self, msg: str):
        print(f"  [{self.name}] {msg}")

    def run(self, contract_text: str, parsed_info: dict) -> dict:
        self.log("启动Chain-of-Thought风险推理...")

        system_prompt = """你是一位资深合同法律顾问，专注于商业合同风险评估。
请使用严格的链式推理（Chain-of-Thought）逐步分析风险，每个风险点必须给出：
1. 发现的问题
2. 推理过程（为什么这是风险）
3. 风险等级（高/中/低）
4. 建议修改方向"""

        prompt = f"""请对以下合同进行全面风险评估：

【合同全文】
{contract_text}

【已解析要素】
{json.dumps(parsed_info, ensure_ascii=False, indent=2)}

请按以下JSON格式返回，不要包含其他文字：
{{
  "overall_risk_level": "高/中/低",
  "risk_score": 0到100的数字,
  "risks": [
    {{
      "clause": "条款名称",
      "issue": "发现的问题",
      "reasoning": "链式推理过程",
      "risk_level": "高/中/低",
      "suggestion": "建议修改方向"
    }}
  ],
  "missing_clauses": ["缺失的重要条款列表"],
  "favorable_clauses": ["对甲方有利的条款列表"],
  "recommendation": "总体建议"
}}"""

        self.log("执行多维度风险推理 (财务/法律/合规/数据安全)...")
        start = __import__('time').time()

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )

        elapsed = __import__('time').time() - start
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        self.log(f"API响应完成 | 耗时: {elapsed:.2f}s | Token消耗: {tokens_used:,}")

        raw = response.content[0].text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            result = json.loads(raw)
            risks = result.get("risks", [])
            score = result.get("risk_score", "N/A")
            level = result.get("overall_risk_level", "N/A")
            self.log(f"✅ 风险评估完成 | 综合风险评分: {score}/100 | 等级: {level}")
            self.log(f"   发现风险点: {len(risks)} 项 | 缺失条款: {len(result.get('missing_clauses', []))} 项")

            for i, r in enumerate(risks, 1):
                icon = "🔴" if r.get("risk_level") == "高" else ("🟡" if r.get("risk_level") == "中" else "🟢")
                print(f"     {icon} 风险{i}: [{r.get('risk_level')}] {r.get('clause')} — {r.get('issue')}")

            return result
        except json.JSONDecodeError:
            self.log("⚠️ JSON解析失败，返回原始文本")
            return {"raw": raw}
