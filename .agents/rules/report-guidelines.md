# 报告结构与维护规范（Report Guidelines）

## 1. 报告存储目录结构
所有报告按**公司名**建文件夹，存放在 `reports/{公司名}/`：
- 单公司深度报告：`reports/{公司名}/{公司名}-research-{YYYYMMDD}.md`
- 财报点评：`reports/{公司名}/{公司名}-earnings-{期间}.md`
- 投资团队四大师协同：`reports/{公司名}/最终报告.md` 及分部报告
- 投资论文跟踪：`reports/{公司名}/{公司名}-thesis.md`
- 管理层调研：`reports/{公司名}/{公司名}-management-{YYYYMMDD}.md`

行业/多公司报告放根目录：
- 行业研究：`reports/{行业名}-industry-{YYYYMMDD}.md`
- 漏斗筛选：`reports/{行业名}-funnel-{YYYYMMDD}.md`
- 投资检查清单：`reports/多公司对比-checklist-{YYYYMMDD}.md`
- 投资组合追踪：`reports/portfolio-latest.md`

## 2. 报告索引更新
- 每次生成或修改报告后，必须在终端运行索引更新命令：
  ```bash
  python3 tools/reports_index.py
  ```
- 运行检查确保索引无缝同步：
  ```bash
  python3 tools/reports_index.py --check
  ```
- 新建的专题目录或筛选池目录需登记在 `reports/_index/config.json` 中。
