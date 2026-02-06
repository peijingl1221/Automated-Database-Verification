from loader import TaskLoader
from runner import TaskRunner
import sys


if __name__ == "__main__":
    # 初始化 TaskLoader
    # task_path = sys.argv[1]
    task_path = 'task_2.yml'
    rules_pool_path = '.rules_pool.yml'
    task_loader = TaskLoader(rules_pool_path, task_path)

    # 验证任务
    task_loader.validate_task()

    # 初始化 TaskRunner
    task_runner = TaskRunner(task_loader)

    # 运行任务
    task_runner.run_task()