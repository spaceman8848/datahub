import streamlit as st
import pandas as pd
import io
from collections import Counter
import zipfile

# /d:/Yuxi/dataHub/pages/002_Convert_txt_to_csv.py

def detect_separator(content, candidates=[',', '\t', ';', '|', ' ']):
    """
    自动检测分隔符：选择在第一行产生最多列的分隔符，
    如果有多个，选择在第二行也一致的分隔符。
    """
    lines = content.split('\n')[:3]  # 检查前3行
    lines = [line.strip() for line in lines if line.strip()]
    
    if not lines:
        return ','
    
    best_sep = ','
    max_cols = 0
    
    for sep in candidates:
        cols_first = len(lines[0].split(sep))
        if cols_first > max_cols:
            max_cols = cols_first
            best_sep = sep
        elif cols_first == max_cols and len(lines) > 1:
            # 如果列数相同，检查第二行
            cols_second = len(lines[1].split(sep))
            if cols_second > len(lines[1].split(best_sep)):
                best_sep = sep
    
    return best_sep

st.set_page_config(page_title="批量转换TXT到CSV", layout="wide")
st.title("批量转换 TXT 文件到 CSV 格式")

st.sidebar.header("设置")
encoding = st.sidebar.text_input("文件编码", "utf-8", help="例如 utf-8 或 gbk")
header_option = st.sidebar.selectbox("包含表头(header)", ["有表头 (第一行为列名)", "无表头"], index=0)

st.markdown("拖拽或选择多个 TXT 文件上传（系统将自动检测分隔符）：")
uploaded_files = st.file_uploader("选择 TXT 文件", type=["txt"], accept_multiple_files=True)

if uploaded_files:
    st.write(f"已上传 {len(uploaded_files)} 个文件")
    
    csv_files = {}  # 存储转换后的CSV数据
    
    for f in uploaded_files:
        st.subheader(f"处理文件: {f.name}")
        try:
            # 重置文件指针
            f.seek(0)
            # 读取为字符串
            content = f.read().decode(encoding)
            
            # 自动检测分隔符
            detected_sep = detect_separator(content)
            st.write(f"检测到的分隔符: '{detected_sep}' (显示为: {repr(detected_sep)})")
            
            # 使用StringIO读取为DataFrame
            string_io = io.StringIO(content)
            if header_option.startswith("有"):
                df = pd.read_csv(string_io, sep=detected_sep)
            else:
                df = pd.read_csv(string_io, sep=detected_sep, header=None)
            
            st.write(f"预览 (前5行):")
            st.dataframe(df.head())
            
            # 转换为CSV字符串，使用逗号分隔
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, sep=',')
            csv_data = csv_buffer.getvalue()
            
            # 存储到字典
            csv_filename = f.name.replace('.txt', '.csv')
            csv_files[csv_filename] = csv_data
            
            # 单个下载按钮
            st.download_button(
                label=f"下载 {csv_filename}",
                data=csv_data,
                file_name=csv_filename,
                mime='text/csv'
            )
            
        except Exception as e:
            st.error(f"处理文件 {f.name} 时出错: {e}")
    
    # 批量下载按钮
    if csv_files:
        st.markdown("---")
        st.subheader("批量下载")
        
        # 创建ZIP文件
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename, data in csv_files.items():
                zip_file.writestr(filename, data)
        
        zip_data = zip_buffer.getvalue()
        
        st.download_button(
            label="下载所有CSV文件 (ZIP)",
            data=zip_data,
            file_name="converted_csv_files.zip",
            mime="application/zip"
        )