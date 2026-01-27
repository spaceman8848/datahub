# DataHub

DataHub 是一个基于 Streamlit 的数据处理工具集，提供多种 CSV、Excel 和文本数据处理功能。通过简单的网页界面，用户可以轻松合并、转换、合并和清洗数据文件。

## 功能特性

### 🔄 多CSV文件合并 (001_Combine_multiCSVs.py)
- 支持同时上传多个 CSV 文件
- 自动检测和处理不同编码格式
- 可选择合并方式：纵向合并（追加行）或横向合并（追加列）
- 支持批量下载合并后的文件
![多CSV文件合并]((https://github.com/spaceman8848/datahub/blob/master/imgs/001.jpg))

### 📝 TXT转CSV转换 (002_Convert_txt_to_csv.py)
- 自动检测文本文件分隔符（逗号、制表符、分号等）
- 支持自定义分隔符
- 处理带或不带表头的文件
- 批量转换多个 TXT 文件
![TXT转CSV转换](https://github.com/spaceman8848/dataHub/imgs/002.jpg)

### 🔗 CSV文件合并 (003_Merge_2CSVs.py)
- 支持 SQL 风格的 JOIN 操作
- 7种连接类型：INNER JOIN、LEFT JOIN、RIGHT JOIN、OUTER JOIN、LEFT EXCLUDING JOIN、RIGHT EXCLUDING JOIN、OUTER EXCLUDING JOIN
- 支持左右表不同的键列
- 可视化 JOIN 操作示意图
- 支持左侧一个文件与右侧多个文件合并
![CSV文件合并](https://github.com/spaceman8848/dataHub/imgs/003.jpg)

### 🧹 CSV数据清洗 (004_CSV_Data_Cleaning.py)
- 灵活的数据跳过选项（支持跳过指定行数，区分是否包含列名）
- 动态筛选条件（支持多种操作符：等于、不等于、包含、大于、小于等）
- 支持多个筛选条件之间的逻辑关系（AND/OR）
- 数据类型调整（跳过行、取前N行）
- 批量处理和下载清洗后的文件
![CSV数据清洗](https://github.com/spaceman8848/dataHub/imgs/004.jpg)

### 🔄 多Excel文件合并 (005_Combine_multiExcels.py)
- 支持同时上传多个 Excel 文件
- 可选择合并方式：纵向合并（追加行）或横向合并（追加列）
- 支持批量下载合并后的文件

### 📝 TXT转Excel转换 (006_Convert_txt_to_excel.py)
- 自动检测文本文件分隔符（逗号、制表符、分号等）
- 支持自定义分隔符
- 处理带或不带表头的文件
- 批量转换多个 TXT 文件

### 🔗 Excel文件合并 (007_Merge_2Excels.py)
- 支持 SQL 风格的 JOIN 操作
- 7种连接类型：INNER JOIN、LEFT JOIN、RIGHT JOIN、OUTER JOIN、LEFT EXCLUDING JOIN、RIGHT EXCLUDING JOIN、OUTER EXCLUDING JOIN
- 支持左右表不同的键列
- 可视化 JOIN 操作示意图
- 支持左侧一个文件与右侧多个文件合并

### 🧹 Excel数据清洗 (008_Excel_Data_Cleaning.py)
- 灵活的数据跳过选项（支持跳过指定行数，区分是否包含列名）
- 动态筛选条件（支持多种操作符：等于、不等于、包含、大于、小于等）
- 支持多个筛选条件之间的逻辑关系（AND/OR）
- 数据类型转换（数值型、字符串、日期时间）
- 批量处理和下载清洗后的文件

## 安装步骤

### 环境要求
- Python 3.8+
- pip

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行应用
```bash
streamlit run 000_DataHub.py
```

应用将在浏览器中自动打开，默认地址：http://localhost:8501

## 使用方法

1. 启动应用后，在主页选择要使用的工具
2. 根据页面提示上传文件
3. 配置处理参数
4. 点击处理按钮
5. 下载处理后的结果文件

## 项目结构

```
dataHub/
├── 000_DataHub.py              # 主页
├── pages/
│   ├── 001_Combine_multiCSVs.py    # 多CSV合并
│   ├── 002_Convert_txt_to_csv.py   # TXT转CSV
│   ├── 003_Merge_2CSVs.py          # CSV合并
│   ├── 004_CSV_Data_Cleaning.py    # CSV数据清洗
│   ├── 005_Combine_multiExcels.py  # 多Excel合并
│   ├── 006_Convert_txt_to_excel.py # TXT转Excel
│   ├── 007_Merge_2Excels.py        # Excel合并
│   └── 008_Excel_Data_Cleaning.py  # Excel数据清洗
├── demoData/                    # 示例数据文件
├── imgs/                        # 图片资源
├── requirements.txt             # 依赖包列表
└── README.md                    # 项目说明
```

## 示例数据

项目包含示例数据文件（位于 `demoData/` 目录）：
- `addresses.csv` - 地址数据
- `airtravel.csv` - 航空旅行数据
- `left_test.csv`, `right_test.csv` - 合并测试数据
- `sample_tab.txt`, `sample_comma.txt` - 文本转换示例

## 技术栈

- **前端界面**: Streamlit
- **数据处理**: Pandas
- **文件处理**: Python 标准库

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 许可证

MIT License

## 作者

[Feiyu YU习](https://github.com/spaceman8848/datahub)

---

如果您在使用过程中遇到问题，请查看各页面的帮助提示或提交 Issue。
