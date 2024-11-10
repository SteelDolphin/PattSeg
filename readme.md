# 大理石拼花图案分割

## 开始使用

### 配置环境依赖
创建conda虚拟环境（可选）

```bash
conda create -n env_name python==3.9
```

在新的环境中，运行以下命令来安装 requirements.txt 文件中列出的所有依赖库：

```python
pip install -r requirements.txt
```

### 熟悉项目结构
这个项目结构是一个典型的使用 PyQt5 框架构建的图形用户界面（GUI）应用程序，包含不同的文件和文件夹，分别用于存储源代码、资源文件、数据、配置文件等。下面是对该项目结构的详细说明：
```
│  GUI.bat                 # ui编译的批处理文件
│  main.py                 # 项目的主入口文件
│  requirements.txt        # Python 依赖文件
├─assets
│      icon.png            # 应用程序的图标文件
├─data                     # 数据文件夹
│  ├─images                # 原始图像文件
│  └─processed_data        # 处理后的图像文件
├─src                      # 源代码文件夹
│  │  __init__.py          # 初始化文件
│  ├─controllers           # 控制器：处理应用逻辑
│  │      controller.py    # 主控制器文件
│  │      edge_v3.0.py     # 图像边缘检测模块
│  ├─utils                 # 工具模块：通用辅助功能
│  │  │  matplot_canvas.py # Matplotlib 画布集成模块
│  │  │  utils.py          # 实用函数
│  │
│  ├─views                 # 视图模块：用户界面定义
│  │  │  help_window_view.py  # 帮助窗口的视图
│  │  │  main_window_view.py  # 主窗口的视图
│  │  │  ui_main_window.py    # Qt Designer 生成的主窗口布局
│  │
│  └─__pycache__           # 缓存文件夹：存放编译后的 `.pyc` 文件
│
└─ui                       # UI 文件夹
        main_window.ui     # Qt Designer 生成的主窗口布局文件
```
### 顶层目录
- **.gitignore**：指定 Git 需要忽略的文件或文件夹，以避免提交不必要或敏感的数据。
- **GUI.bat**：一个批处理文件，可能用于启动该项目的 GUI 程序。
- **main.py**：项目的主入口文件，通常用于初始化应用程序并启动主窗口。
- **readme.md**：项目的说明文件，包含项目简介、使用说明、安装步骤等。
- **requirements.txt**：记录项目所需的 Python 依赖库，可以通过 `pip install -r requirements.txt` 命令安装所有依赖。
- **流程图.drawio**：项目的流程图文件，用于描述项目的逻辑结构或功能流程，通常用 draw.io 编辑。

### 主要文件夹

#### assets
- **icon.png**：项目的图标文件，可能在应用窗口或快捷方式中使用。

#### data
- **images**：存放原始图像数据，用于图像处理或展示。
- **processed_data**：存放处理后的图像数据，通常是经过图像处理模块处理后的文件。

#### img
- **Snipaste_2024-10-04_11-26-16.png** 等：屏幕截图或其他图像，可能用于文档、示例展示或开发测试。

#### src
包含项目的主要源代码，是 PyQt5 项目最核心的部分。

- **\_\_init\_\_.py**：标识 `src` 是一个 Python 包，使其中的模块可以被导入。
  
- **controllers**：用于控制应用逻辑的文件夹。
  - **controller.py**：主要的控制器文件，包含应用的核心逻辑。
  - **edge_v3.0.py**：可能是用于边缘检测或图像处理的功能模块。

- **utils**：存放工具类和辅助函数。
  - **matplot_canvas.py**：可能是与 Matplotlib 集成的画布，用于在 GUI 中展示图表。
  - **utils.py**：包含一些通用的实用函数。

- **views**：存放用于展示和布局的视图模块。
  - **help_window_view.py**：帮助窗口的视图文件，定义了帮助窗口的界面和行为。
  - **main_window_view.py**：主窗口的视图文件，定义了主窗口的界面和行为。
  - **ui_main_window.py**：通过 Qt Designer 生成的主窗口界面文件，通常包含窗口布局的代码。

#### ui
- **main_window.ui**：用 Qt Designer 创建的 UI 文件，描述了主窗口的布局和控件配置。这个 `.ui` 文件可以通过 PyQt5 的 `pyuic5` 命令转换为 Python 代码。