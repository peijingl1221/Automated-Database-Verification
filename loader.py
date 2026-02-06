import yaml
from typing import Dict, Any

class TaskLoader:
    def __init__(self, rules_pool_path: str, task_path: str):
        '''
        初始化 TaskLoader。

        :param rules_pool_path: rules_pool.yml 文件路径
        :param task_path: task.yml 文件路径
        '''
        self.rules_pool_path = rules_pool_path
        self.task_path = task_path
        self.rules_pool = self._load_rules_pool()
        self.task_info = self._load_task_info()

    def _load_rules_pool(self) -> Dict[str, Any]:
        '''
        加载 rules_pool.yml 文件。

        :return: 规则池配置
        '''
        with open(self.rules_pool_path, "r") as f:
            return yaml.safe_load(f)["TRANSMATRIX_RULE"]["RULES_POOL"]

    def _load_task_info(self) -> Dict[str, Any]:
        '''
        加载 task.yml 文件。

        :return: 任务配置
        '''
        with open(self.task_path, "r") as f:
            return yaml.safe_load(f)["TASK_INFO"]

    def validate_task(self) -> None:
        '''
        验证任务中的规则是否与规则池匹配。

        :raises ValueError: 如果规则不匹配
        '''
        for rule_name, rule_config in self.task_info.items():
            if rule_name in ["name", "report"]:
                continue  # 跳过任务信息字段

            # 检查规则是否在规则池中
            if rule_name not in self.rules_pool:
                raise ValueError(f"Rule '{rule_name}' not found in rules pool.")

            # 检查模式是否支持
            mode = rule_config["mode"].lower()
            if mode not in self.rules_pool[rule_name]["support_mode"]:
                raise ValueError(f"Mode '{mode}' is not supported by rule '{rule_name}'.")

            # 检查字段是否匹配
            required_fields = self.rules_pool[rule_name]["fields"]
            provided_fields = rule_config["fields"].keys()
            for field in required_fields:
                if field not in provided_fields:
                    raise ValueError(f"Field '{field}' is required by rule '{rule_name}' but not provided.")

    def get_task_info(self) -> Dict[str, Any]:
        '''
        获取任务信息。

        :return: 任务配置
        '''
        return self.task_info

    def get_rules_pool(self) -> Dict[str, Any]:
        '''
        获取规则池。

        :return: 规则池配置
        '''
        return self.rules_pool

    def get_sorted_rules(self) -> list:
        '''
        根据优先级对规则进行排序。

        :return: 按优先级排序的规则列表
        '''
        # 获取任务中定义的规则
        task_rules = {k: v for k, v in self.task_info.items() if k not in ["name", "report"]}

        # 获取每个规则的优先级
        sorted_rules = sorted(
            task_rules.items(),
            key=lambda x: self.rules_pool[x[0]]["priority"]
        )

        return sorted_rules