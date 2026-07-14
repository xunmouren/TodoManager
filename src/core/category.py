CATEGORIES = {
    "default": "默认",
    "work": "工作",
    "study": "学习",
    "life": "生活",
    "project": "项目"
}


def get_category_name(key):
    """根据key获取显示名称"""
    return CATEGORIES.get(key, "默认")


def get_category_keys():
    """获取所有分类key"""
    return list(CATEGORIES.keys())


def get_category_items():
    """获取所有分类(key, 中文名)"""
    return CATEGORIES.items()
