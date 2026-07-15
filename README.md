# TodoManager 📝

一个基于 **Python + PySide6** 开发的桌面待办事项管理软件，使用`uv`进行项目管理依赖

TodoManager 提供简洁直观的任务管理界面，支持任务添加、编辑、删除、完成状态管理以及任务分类查看

项目采用分层架构设计，将：

- GUI 界面层
- 业务逻辑层
- 数据存储层

进行分离，方便后续功能扩展和维护

## ✨ 功能特性

### 当前功能

- ✅ 添加任务
- ✅ 删除任务
- ✅ 编辑任务
- ✅ 标记任务完成/未完成
- ✅ 查看全部任务
- ✅ 查看已完成任务
- ✅ JSON 本地数据持久化
- ✅ QSS 自定义界面样式
- ✅ 模块化项目结构

### 🛠 技术栈

| 技术 | 用途 |
| --- | --- |
| Python | 核心开发语言 |
| PySide6 | GUI 框架 |
| Qt | 桌面应用开发 |
| JSON | 数据持久化存储 |
| QSS | Qt 样式设计 |
| Dataclass | 数据模型管理 |

## 🚀 安装运行
```bash
1. 克隆项目
git clone https://github.com/xunmouren/TodoManager.git
cd TodoManager

2. 安装 uv
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

3. 创建虚拟环境并安装依赖
#本项目使用uv管理 Python 环境和依赖
uv sync

4. 运行程序
uv run main.py
```

## 🔮 后续开发计划
- [x] 增加任务优先级
- [x] 深色模式
- [ ] 右键菜单
- [ ] 数据导出
- [ ] 仪表盘
