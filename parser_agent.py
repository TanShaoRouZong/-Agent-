"""
Parser Agent — 合同结构化解析
从合同文本中提取关键信息，输出结构化JSON
"""

import json
import anthropic


class ParserAgent:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.name = "ParserAgent"
        self.model = "claude-sonnet-4-20250514"

    def log(self, msg: str):
        print(f"  [{self.name}] {msg}")

    def run(self, contract_text: str) -> dict:
        self.log("开始解析合同结构...")

        prompt = f"""请从以下合同中提取关键结构化信息，严格按JSON格式返回，不要包含任何其他文字：

合同内容：
{contract_text}

返回格式：
{{
  "parties": {{"party_a": "甲方名称", "party_b": "乙方名称"}},
  "service_type": "服务类型",
  "duration": {{"start": "开始日期", "end": "结束日期", "months": 月数}},
  "total_amount": 金额数字,
  "payment_schedule": "付款安排",
  "confidentiality_period_years": 保密年限数字,
  "penalty_rate": "违约金比例",
  "penalty_cap": 违约金上限数字,
  "dispute_resolution": "争议解决方式",
  "ip_ownership": "知识产权归属",
  "force_majeure_notice_days": 不可抗力通知天数
}}"""

        self.log("调用 Claude API → 提取合同要素...")
        start = __import__('time').time()

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        elapsed = __import__('time').time() - start
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        self.log(f"API响应完成 | 耗时: {elapsed:.2f}s | Token消耗: {tokens_used:,}")

        raw = response.content[0].text.strip()
        # Clean potential markdown fences
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            result = json.loads(raw)
            self.log(f"✅ 成功提取 {len(result)} 个关键字段")
            for k, v in result.items():
                print(f"     • {k}: {v}")
            return result
        except json.JSONDecodeError:
            self.log("⚠️ JSON解析失败，返回原始文本")
            return {"raw": raw}
