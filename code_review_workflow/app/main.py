import argparse
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from .workflow import CodeAnalysisAgent, FixAgent, ReviewAgent, ReviewWorkflow


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="运行代码审查与修复工作流")
    parser.add_argument("source", type=Path, help="待审查的源代码文件")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("review_output"),
        help="审查报告和修复文件的输出目录（默认：review_output）",
    )
    return parser


def main() -> int:
    args = create_parser().parse_args()
    load_dotenv()
    api_key = os.getenv("ZHIPU_API_KEY")
    if not api_key:
        print("错误：请在 .env 中配置 ZHIPU_API_KEY。", file=sys.stderr)
        return 2

    try:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        log_path = args.output_dir / "workflow.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_path, encoding="utf-8"),
            ],
            force=True,
        )
        client = OpenAI(
            api_key=api_key,
            base_url=os.getenv(
                "ZHIPU_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"
            ),
        )
        model = os.getenv("ZHIPU_MODEL", "glm-4-flash")

        class ZhipuChatClient:
            def complete(self, system_prompt: str, user_prompt: str) -> str:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.2,
                )
                content = response.choices[0].message.content
                if not content:
                    raise RuntimeError("智谱 API 返回了空内容")
                return content

        chat_client = ZhipuChatClient()
        workflow = ReviewWorkflow(
            CodeAnalysisAgent(chat_client),
            ReviewAgent(chat_client),
            FixAgent(chat_client),
        )
<<<<<<< HEAD
        state = workflow.run(args.source, args.output_dir)
=======
        workflow.run(args.source, args.output_dir)
>>>>>>> 1f1fede7bb24d5607d1d08ffad544d7c4b5b57f7
    except (OSError, OpenAIError, RuntimeError, ValueError) as error:
        logging.getLogger(__name__).error("工作流未能完成：%s", error)
        return 1

<<<<<<< HEAD
    if not state.validation_passed:
        print(
            "工作流已运行，但修复后验证未通过；请检查 "
            f"{(args.output_dir / 'validation.md').resolve()}",
            file=sys.stderr,
        )
        return 3

    print(f"工作流完成。报告与修复文件位于：{args.output_dir.resolve()}")
    if not state.validation_tests_run:
        print("注意：没有运行到项目测试，请查看 validation.md 中的说明。")
=======
    print(f"工作流完成。报告与修复文件位于：{args.output_dir.resolve()}")
>>>>>>> 1f1fede7bb24d5607d1d08ffad544d7c4b5b57f7
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
