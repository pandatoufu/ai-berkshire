# 财务严谨性与计算校验规范（Financial Validation）

在执行估值、财务计算与多源数据校验时，必须遵循以下要求：

## 1. 禁用大模型心算，强制使用精确计算工具
- 涉及估值模型（DCF、终值 Terminal Value、股息贴现 DDM）、市值核验、复合年均增长率（CAGR）、市盈率（P/E）、净资产收益率（ROE）等任何数学计算时，严禁使用模型心算。
- 必须通过 `run_command` 调用项目内的精确计算工具：
  ```bash
  python3 tools/financial_rigor.py ...
  python3 tools/terminal_value.py ...
  ```

## 2. 市值与股本双重核对
- 市值必须显式验算：`当前股价 × 最新稀释后总股本`。
- 将验算结果与金融终端/财经网站公布的市值对比，确认是否存在包含不同股份类别（如 A/B 类股、ADR 比例换算）的口径偏差。
- 必须清晰标注计价币种（美元 USD、人民币 RMB、港币 HKD、新台币 TWD），防止跨币种混淆。

## 3. 专用市场取数工具
- 台股数据：使用 `python3 tools/twstock_data.py` (基于 FinMind) 获取，并与公开信息进行交叉核验。
- A股数据：使用 `python3 tools/ashare_data.py` 获取或校对。
- 报告核验：在完成报告产出后，运行 `python3 tools/report_audit.py <path/to/report.md>` 进行发布前机检。
