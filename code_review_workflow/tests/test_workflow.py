import tempfile
import unittest
from pathlib import Path

from app.workflow import CodeAnalysisAgent, FixAgent, ReviewAgent, ReviewWorkflow


class FakeChatClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        self.calls.append((system_prompt, user_prompt))
        if "代码分析助手" in system_prompt:
            return "分析：函数接收两个参数并返回其和。"
        if "代码审查员" in system_prompt:
            return "中风险：缺少输入校验。"
        return "def add(a, b):\n    if not isinstance(a, int) or not isinstance(b, int):\n        raise TypeError\n    return a + b\n"


class ReviewWorkflowTests(unittest.TestCase):
    def test_agents_share_state_and_save_outputs_in_order(self) -> None:
        client = FakeChatClient()
        workflow = ReviewWorkflow(
            CodeAnalysisAgent(client), ReviewAgent(client), FixAgent(client)
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_path = root / "sample.py"
            output_dir = root / "output"
            original = "def add(a, b):\n    return a + b\n"
            source_path.write_text(original, encoding="utf-8")

            state = workflow.run(source_path, output_dir)

            self.assertEqual(len(client.calls), 3)
            self.assertIn("分析：", client.calls[1][1])
<<<<<<< HEAD
            self.assertIn("1: def add(a, b):", client.calls[1][1])
            self.assertIn("2:     return a + b", client.calls[1][1])
=======
>>>>>>> 1f1fede7bb24d5607d1d08ffad544d7c4b5b57f7
            self.assertIn("缺少输入校验", client.calls[2][1])
            self.assertEqual(source_path.read_text(encoding="utf-8"), original)
            self.assertEqual(
                (output_dir / "analysis.md").read_text(encoding="utf-8"),
                state.analysis,
            )
            self.assertEqual(
                (output_dir / "review.md").read_text(encoding="utf-8"),
                state.review,
            )
            self.assertEqual(
                (output_dir / "sample.fixed.py").read_text(encoding="utf-8"),
                state.fixed_code,
            )
<<<<<<< HEAD
            self.assertTrue(state.validation_passed)
            self.assertFalse(state.validation_tests_run)
            self.assertIn("语法检查：**通过**", state.validation_report)
            self.assertEqual(
                (output_dir / "validation.md").read_text(encoding="utf-8"),
                state.validation_report,
            )
=======
>>>>>>> 1f1fede7bb24d5607d1d08ffad544d7c4b5b57f7
            self.assertEqual(
                state.events,
                [
                    "started:代码分析",
                    "completed:代码分析",
                    "started:代码审查",
                    "completed:代码审查",
                    "started:代码修复",
                    "completed:代码修复",
                    f"completed:修复文件已写入 {output_dir / 'sample.fixed.py'}",
<<<<<<< HEAD
                    "started:修复后验证",
                    "completed:修复后验证",
                ],
            )

    def test_validation_fails_for_invalid_python_syntax(self) -> None:
        class InvalidFixClient(FakeChatClient):
            def complete(self, system_prompt: str, user_prompt: str) -> str:
                self.calls.append((system_prompt, user_prompt))
                if "代码分析助手" in system_prompt:
                    return "分析"
                if "代码审查员" in system_prompt:
                    return "审查"
                return "def broken(:\n    pass\n"

        client = InvalidFixClient()
        workflow = ReviewWorkflow(
            CodeAnalysisAgent(client), ReviewAgent(client), FixAgent(client)
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_path = root / "sample.py"
            output_dir = root / "output"
            source_path.write_text("print('hello')\n", encoding="utf-8")

            state = workflow.run(source_path, output_dir)

            self.assertFalse(state.validation_passed)
            self.assertIn("Python 语法检查：**失败**", state.validation_report)
            self.assertIn("项目测试：跳过", state.validation_report)
            self.assertTrue((output_dir / "sample.fixed.py").exists())
            self.assertTrue((output_dir / "validation.md").exists())

    def test_validation_runs_project_tests_when_available(self) -> None:
        client = FakeChatClient()
        workflow = ReviewWorkflow(
            CodeAnalysisAgent(client), ReviewAgent(client), FixAgent(client)
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            app_dir = root / "app"
            tests_dir = root / "tests"
            app_dir.mkdir()
            tests_dir.mkdir()
            source_path = app_dir / "sample.py"
            source_path.write_text("print('hello')\n", encoding="utf-8")
            (tests_dir / "test_smoke.py").write_text(
                "import unittest\n\n"
                "class SmokeTest(unittest.TestCase):\n"
                "    def test_passes(self):\n"
                "        self.assertEqual(1 + 1, 2)\n",
                encoding="utf-8",
            )

            state = workflow.run(source_path, root / "output")

            self.assertTrue(state.validation_passed)
            self.assertTrue(state.validation_tests_run)
            self.assertIn("项目测试：**通过**（运行 1 个测试）", state.validation_report)

    def test_validation_fails_when_project_tests_fail(self) -> None:
        client = FakeChatClient()
        workflow = ReviewWorkflow(
            CodeAnalysisAgent(client), ReviewAgent(client), FixAgent(client)
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            app_dir = root / "app"
            tests_dir = root / "tests"
            app_dir.mkdir()
            tests_dir.mkdir()
            source_path = app_dir / "sample.py"
            source_path.write_text("print('hello')\n", encoding="utf-8")
            (tests_dir / "test_failure.py").write_text(
                "import unittest\n\n"
                "class FailureTest(unittest.TestCase):\n"
                "    def test_fails(self):\n"
                "        self.assertEqual(1, 2)\n",
                encoding="utf-8",
            )

            state = workflow.run(source_path, root / "output")

            self.assertFalse(state.validation_passed)
            self.assertTrue(state.validation_tests_run)
            self.assertIn("项目测试：**失败**", state.validation_report)
            self.assertIn("AssertionError", state.validation_report)

=======
                ],
            )

>>>>>>> 1f1fede7bb24d5607d1d08ffad544d7c4b5b57f7
    def test_failed_stage_stops_the_remaining_workflow(self) -> None:
        class FailingClient(FakeChatClient):
            def complete(self, system_prompt: str, user_prompt: str) -> str:
                self.calls.append((system_prompt, user_prompt))
                if "代码分析助手" in system_prompt:
                    raise RuntimeError("model unavailable")
                if "代码审查员" in system_prompt:
                    return "审查"
                return "修复"

        client = FailingClient()
        workflow = ReviewWorkflow(
            CodeAnalysisAgent(client), ReviewAgent(client), FixAgent(client)
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_path = root / "sample.py"
            source_path.write_text("print('hello')\n", encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "model unavailable"):
                workflow.run(source_path, root / "output")

        self.assertEqual(len(client.calls), 1)
