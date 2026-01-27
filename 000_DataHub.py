import streamlit as st

st.set_page_config(page_title="DataHub - 数据处理工具集", layout="wide")
st.title("DataHub - 数据处理工具集")
st.markdown("欢迎使用 DataHub 数据处理工具集！这里提供了多个实用的数据处理工具。")

st.header("📋 工具列表")

# 001_Combine_multiCSVs.py
st.subheader("001_Combine_multiCSVs.py - 合并多个CSV文件")
st.markdown("""
**用途**: 将多个CSV文件合并为一个CSV文件，支持不同的合并方式。

**功能特点**:
- 支持按行合并（concat rows）或按列合并（concat columns）
- 可选择分隔符、编码、是否包含表头
- 支持重建索引、去重等选项
- 按行合并时可选择outer或inner对齐方式
- 添加_source_filename列追踪来源

**使用方法**:
1. 上传多个CSV文件
2. 设置合并参数（分隔符、编码、表头等）
3. 选择合并方向和方式
4. 点击"执行合并"查看结果
5. 下载合并后的CSV文件
""")

# 002_Convert_txt_to_csv.py
st.subheader("002_Convert_txt_to_csv.py - 批量转换TXT到CSV")
st.markdown("""
**用途**: 将TXT文件批量转换为CSV格式，支持自动检测分隔符。

**功能特点**:
- 自动检测TXT文件中的分隔符（逗号、制表符、分号、管道、空格）
- 支持批量处理多个TXT文件
- 可选择是否包含表头
- 输出标准CSV格式（逗号分隔）
- 单个和批量下载选项

**使用方法**:
1. 上传多个TXT文件
2. 选择文件编码（默认UTF-8）
3. 选择是否包含表头
4. 系统自动检测每个文件的分隔符
5. 预览转换结果
6. 下载单个或批量CSV文件
""")

# 003_Merge_2CSVs.py
st.subheader("003_Merge_2CSVs.py - 合并两个CSV文件（JOIN操作）")
st.markdown("""
**用途**: 使用SQL JOIN类似的操作合并两个CSV文件，支持多种JOIN类型。

**功能特点**:
- 支持7种JOIN类型：inner, left, right, outer, left_excluding, right_excluding, outer_excluding
- 支持左右表不同的键列
- 可视化JOIN类型说明和图示
- 支持多个右表文件批量处理
- 单个和批量下载合并结果

**使用方法**:
1. 上传一个左侧CSV文件和多个右侧CSV文件
2. 选择左右表的键列
3. 选择JOIN类型（可展开查看详细说明和图示）
4. 系统自动合并并显示结果
5. 下载单个或批量合并后的CSV文件
""")

# 004_CSV_Data_Cleaning.py
st.subheader("004_CSV_Data_Cleaning.py - CSV数据清洗与筛选")
st.markdown("""
**用途**: 对CSV文件进行数据清洗、调整大小和条件筛选。

**功能特点**:
- 支持多种筛选条件：等于、不等于、包含、不包含、以...开始、以...结束、大于、小于等
- 支持多个筛选条件之间的逻辑关系（AND/OR）
- 数据调整功能：跳过行数、取前N行、选择列
- 动态添加多个筛选条件
- 支持批量处理多个CSV文件
- 单个和批量下载清洗结果

**使用方法**:
1. 上传多个CSV文件
2. 设置编码和表头选项
3. 配置数据调整参数（跳过行、取行数、选择列）
4. 添加筛选条件（列、操作符、值）
5. 选择条件之间的逻辑关系（AND/OR）
6. 系统自动应用所有条件并显示结果
7. 下载单个或批量清洗后的CSV文件
""")

# 005_Combine_multiExcels.py
st.subheader("005_Combine_multiExcels.py - 合并多个Excel文件")
st.markdown("""
**用途**: 将多个Excel文件合并为一个Excel文件，支持不同的合并方式。

**功能特点**:
- 支持按行合并（concat rows）或按列合并（concat columns）
- 可选择是否包含表头
- 支持重建索引、去重等选项
- 按行合并时可选择outer或inner对齐方式
- 添加_source_filename列追踪来源

**使用方法**:
1. 上传多个Excel文件
2. 设置合并参数（表头等）
3. 选择合并方向和方式
4. 点击"执行合并"查看结果
5. 下载合并后的Excel文件
""")

# 006_Convert_txt_to_excel.py
st.subheader("006_Convert_txt_to_excel.py - 批量转换TXT到Excel")
st.markdown("""
**用途**: 将TXT文件批量转换为Excel格式，支持自动检测分隔符。

**功能特点**:
- 自动检测TXT文件中的分隔符（逗号、制表符、分号、管道、空格）
- 支持批量处理多个TXT文件
- 可选择是否包含表头
- 输出标准Excel格式
- 单个和批量下载选项

**使用方法**:
1. 上传多个TXT文件
2. 选择文件编码（默认UTF-8）
3. 选择是否包含表头
4. 系统自动检测每个文件的分隔符
5. 预览转换结果
6. 下载单个或批量Excel文件
""")

# 007_Merge_2Excels.py
st.subheader("007_Merge_2Excels.py - 合并两个Excel文件（JOIN操作）")
st.markdown("""
**用途**: 使用SQL JOIN类似的操作合并两个Excel文件，支持多种JOIN类型。

**功能特点**:
- 支持7种JOIN类型：inner, left, right, outer, left_excluding, right_excluding, outer_excluding
- 可视化JOIN类型说明和图示
- 手动选择左右表的键列
- 支持多个右表文件批量处理
- 单个和批量下载合并结果

**使用方法**:
1. 上传一个左侧Excel文件和多个右侧Excel文件
2. 选择左右表的键列
3. 选择JOIN类型（可展开查看详细说明和图示）
4. 系统自动合并并显示结果
5. 下载单个或批量合并后的Excel文件
""")

# 008_Excel_Data_Cleaning.py
st.subheader("008_Excel_Data_Cleaning.py - Excel数据清洗与筛选")
st.markdown("""
**用途**: 对Excel文件进行数据清洗、调整大小和条件筛选。

**功能特点**:
- 支持多种筛选条件：等于、不等于、包含、不包含、以...开始、以...结束、大于、小于等
- 支持多个筛选条件之间的逻辑关系（AND/OR）
- 数据类型转换（数值型、字符串、日期时间）
- 缺失值分析（统计缺失值数量和比例）
- 数据类型信息显示
- 动态添加多个筛选条件
- 单个下载清洗结果

**使用方法**:
1. 上传一个Excel文件
2. 查看数据预览和缺失值分析
3. 配置清洗选项（缺失值处理）
4. 添加筛选条件（列、操作符、值）
5. 选择条件之间的逻辑关系（AND/OR）
6. 可选：进行数据类型转换
7. 系统自动应用所有条件并显示结果
8. 下载清洗后的Excel文件
""")

st.header("🚀 如何使用")
st.markdown("""
1. **启动应用**: 运行 `streamlit run 000_DataHub.py` 或直接运行其他页面
2. **导航**: 使用侧边栏选择不同的工具页面
3. **上传数据**: 每个工具都支持文件上传
4. **配置参数**: 根据需要调整设置
5. **处理数据**: 点击相应按钮执行操作
6. **下载结果**: 获取处理后的文件

**注意**: 所有工具都支持中文界面，适合处理中文数据文件。
""")

st.header("📞 技术支持")
st.markdown("""
- 基于 Python + Streamlit + Pandas 开发
- 支持多种文件编码
- 实时预览处理结果
- 批量处理能力
""")

# 页脚
st.markdown("---")
st.markdown("© 2026 DataHub - 数据处理工具集")