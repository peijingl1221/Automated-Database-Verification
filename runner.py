import importlib
from typing import Dict, Any
from loader import TaskLoader

class TaskRunner:
    def __init__(self, task_loader: TaskLoader):
        """
        初始化 TaskRunner。

        :param task_loader: TaskLoader 实例
        """
        self.task_loader = task_loader
        self.task_info = task_loader.get_task_info()
        self.rules_pool = task_loader.get_rules_pool()

    def _load_rule_class(self, module_name: str, class_name: str):
        """
        动态加载规则文件中的指定类。

        :param module_name: 模块名称（文件名，不含 .py）
        :param class_name: 类名
        :return: 规则类的实例
        """
        # 动态加载模块
        module = importlib.import_module(f'rules.{module_name}')

        # 获取指定的类
        if hasattr(module, class_name):
            rule_class = getattr(module, class_name)
            return rule_class()
        else:
            raise ValueError(f"Class '{class_name}' not found in module '{module_name}'.")

    def run_task(self) -> None:
        """
        按优先级运行任务中的所有规则。
        """
        task_name = self.task_info["name"]
        report_enabled = self.task_info["report"]

        print("============================================")
        print(f"Starting task: {task_name}")

        # 按优先级排序规则
        sorted_rules = self.task_loader.get_sorted_rules()

        for rule_name, rule_config in sorted_rules:
            # 获取规则池中的规则配置
            rule_pool_config = self.rules_pool[rule_name]

            # 动态加载规则文件
            module_name = rule_pool_config["file"].replace(".py", "")
            class_name = rule_pool_config["class"]
            rule_class_instance = self._load_rule_class(module_name, class_name)

            # 执行规则
            print("============================================")
            print(f"Executing rule: {rule_name}")
            print(f"Priority: {rule_pool_config['priority']}")
            print(f"Check mode: {rule_pool_config['check_mode']}")
            print(f"Mode: {rule_config['mode']}")
            print(f"Time range: {rule_config['start']} to {rule_config['end']}")

            # 执行规则类的 execute 方法
            rule_class_instance.check(rule_config)

            # 模拟生成报告
            if report_enabled:
                print("Generating report...")

        print("============================================")
        print(f"Task '{task_name}' completed.")
        print("============================================")