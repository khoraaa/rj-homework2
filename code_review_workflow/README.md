# 代码审查工作流（MVP）

<<<<<<< HEAD
基于 PPT 中的 Simple Workflow MVP 要求，实现“提交代码 → 分析 → 审查 → 修复 → 验证”的顺序工作流。提交的源文件代表编码阶段的产物；分析、审查、修复由三个可协作的 Agent 完成，随后由验证器检查修复副本。Agent 通过 `WorkflowState` 共享源代码和上一步结果。
=======
基于 PPT 中的 Simple Workflow MVP 要求，实现“提交代码 → 分析 → 审查 → 修复”的顺序工作流。提交的源文件代表编码阶段的产物；分析、审查、修复由三个可协作的 Agent 完成。Agent 通过 `WorkflowState` 共享源代码和上一步结果。
>>>>>>> 1f1fede7bb24d5607d1d08ffad544d7c4b5b57f7

## 工作流

```text
用户提交源代码
      │
      ▼
代码分析 Agent ──分析结果──┐
      │                    ▼
      └──────────────► 代码审查 Agent ──审查意见──┐
                                                   ▼
                                             代码修复 Agent
                                                   │
<<<<<<< HEAD
                                                   ▼
                                           修复后自动验证
                                                   │
                         ┌─────────────────────────┴──────────┐
                         ▼                 ▼                  ▼
                  分析/审查报告      *.fixed.* 修复副本   validation.md
=======
                         ┌─────────────────────────┴──────────┐
                         ▼                                    ▼
                  analysis.md / review.md              *.fixed.* 修复副本
>>>>>>> 1f1fede7bb24d5607d1d08ffad544d7c4b5b57f7
```

`CodeAnalysisAgent` 适配了项目 1 `code_explain_agent` 的代码读取后调用 GLM 分析的思路，并将其输出作为审查上下文。它不替代审查 Agent，也不把分析猜测视为已确认缺陷。适配为工作流节点而非直接导入项目 1 的文件，因此项目 2 可独立运行。

## 环境与运行

需要 Python 3.10+。先进入 `code_review_workflow` 项目目录，再执行：

```powershell
uv venv
uv pip install -r requirements.txt
Copy-Item .env.example .env
```

在 `.env` 中填入智谱 API Key，然后运行：

```powershell
uv run python -m app.main path\to\your_code.py
uv run python -m app.main path\to\your_code.py --output-dir review_output
```

源文件以 UTF-8 读取；原文件不会被覆盖。输出目录包含：

- `analysis.md`：代码分析 Agent 的分析结果
- `review.md`：代码审查 Agent 的审查意见
- `<源文件名>.fixed.<扩展名>`：代码修复 Agent 生成的修复副本
<<<<<<< HEAD
- `validation.md`：修复副本的 Python 语法检查和项目测试结果
- `workflow.log`：每个阶段的开始、完成或失败记录

修复后会自动检查 Python 文件语法；如果源文件所在项目存在 `tests` 目录，还会使用当前 Python 环境运行 `unittest discover`，最长等待 120 秒。未发现测试用例时会在报告中标明跳过。项目测试在原工作区运行，不会替换源文件；测试是否覆盖修复副本取决于项目自身的测试设计。验证失败时，命令以非零状态结束，但仍保留修复副本和验证报告。验证通过也不代表模型修改一定正确，请在采用前人工检查并运行项目自己的完整测试。

审查 Agent 会收到带显式行号的源代码，并被要求为每条问题引用对应行号或范围；模型仍可能定位不准确，请人工对照源代码核实。
=======
- `workflow.log`：每个阶段的开始、完成或失败记录

修复结果是模型建议，请在采用前人工检查并运行项目测试。
>>>>>>> 1f1fede7bb24d5607d1d08ffad544d7c4b5b57f7

## 实现与扩展

- `ReviewWorkflow` 顺序编排 Agent，通过共享状态传递代码、分析和审查结果。
- `ChatClient` 协议隔离模型调用；可以替换为其他兼容实现，也可在测试中注入假客户端。
<<<<<<< HEAD
- `CodeValidator` 对生成的修复副本做语法检查，并尝试运行项目测试；检查结果写入 `validation.md`。
=======
>>>>>>> 1f1fede7bb24d5607d1d08ffad544d7c4b5b57f7
- 阶段失败会记录并向调用方抛出异常，后续阶段不会继续执行。
- `app/workflow.py` 不依赖具体模型 SDK；`app/main.py` 使用与项目 1 相同的智谱 OpenAI 兼容 API。
- MVP 暂不实现并行调度、自动重试和可视化编排。

## 目录结构

```text
code_review_workflow/
├── app/                 # 工作流和命令行入口
│   ├── main.py
│   └── workflow.py
├── tests/               # 自动化测试
│   └── test_workflow.py
├── .env.example         # API 配置模板
├── .gitignore
├── requirements.txt
└── README.md
```

## 测试

不需要 API Key 即可运行工作流单元测试：

```powershell
uv run python -m unittest discover -s tests -v
```
