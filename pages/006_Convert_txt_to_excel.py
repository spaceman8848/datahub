
import streamlit as st
import pandas as pd
import io
from datetime import datetime
import zipfile

# /d:/Yuxi/dataHub/pages/006_Convert_txt_to_excel.py

st.set_page_config(page_title="批量转换TXT到Excel", layout="wide")
st.title("批量转换 TXT 文件到 Excel")

st.sidebar.header("设置")
sep = st.sidebar.selectbox("分隔符", [",", "\t", ";", "|"], index=0, help="选择 TXT 文件的分隔符")
encoding = st.sidebar.text_input("文件编码", "utf-8", help="例如 utf-8 或 gbk")
header_option = st.sidebar.selectbox("包含表头(header)", ["有表头 (第一行为列名)", "无表头"], index=0)
output_mode = st.sidebar.radio(
    "输出方式",
    ["单个Excel文件，每个TXT为一个Sheet", "每个TXT转换为单独的Excel文件"],
    help="选择输出方式：将所有TXT转换到一个Excel的不同Sheet中，或者每个TXT生成一个独立的Excel文件"
)

st.markdown("拖拽或选择多个 TXT 文件上传（支持不同文件名）:")
uploaded_files = st.file_uploader("选择 TXT 文件", type=["txt"], accept_multiple_files=True)

if uploaded_files:
    st.write(f"已选择 {len(uploaded_files)} 个文件")

    if st.button("执行转换"):
        try:
            if output_mode == "单个Excel文件，每个TXT为一个Sheet":
                # 将所有TXT转换到一个Excel的不同Sheet中
                buf = io.BytesIO()
                with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                    for f in uploaded_files:
                        try:
                            f.seek(0)
                            if header_option.startswith("有"):
                                df = pd.read_csv(f, sep=sep, encoding=encoding)
                            else:
                                df = pd.read_csv(f, sep=sep, encoding=encoding, header=None)

                            # Excel sheet名称限制31个字符
                            sheet_name = f.name.replace('.txt', '')[:31]
                            df.to_excel(writer, sheet_name=sheet_name, index=False)
                            st.success(f"成功转换: {f.name} -> {sheet_name}")
                        except Exception as e:
                            st.error(f"转换失败 {f.name}: {e}")

                buf.seek(0)
                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"converted_{now}.xlsx"
                st.download_button(
                    "下载转换后的 Excel",
                    data=buf,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                # 每个TXT生成一个独立的Excel文件
                st.info("请点击下方按钮下载各个转换后的Excel文件")
                
                # 存储所有转换后的文件数据
                converted_files = []
                
                for f in uploaded_files:
                    try:
                        f.seek(0)
                        if header_option.startswith("有"):
                            df = pd.read_csv(f, sep=sep, encoding=encoding)
                        else:
                            df = pd.read_csv(f, sep=sep, encoding=encoding, header=None)

                        # Excel sheet名称限制31个字符
                        sheet_name = f.name.replace('.txt', '')[:31]
                        excel_filename = f.name.replace('.txt', '.xlsx')

                        # 为每个文件创建一个BytesIO对象
                        buf = io.BytesIO()
                        with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                            df.to_excel(writer, sheet_name=sheet_name, index=False)

                        buf.seek(0)
                        converted_files.append({
                            'filename': excel_filename,
                            'data': buf.getvalue()
                        })
                        
                        st.download_button(
                            f"下载 {excel_filename}",
                            data=buf,
                            file_name=excel_filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"download_{f.name}"
                        )
                        st.success(f"成功转换: {f.name} -> {excel_filename}")
                    except Exception as e:
                        st.error(f"转换失败 {f.name}: {e}")
                
                # 添加"下载所有文件"按钮
                if converted_files:
                    st.write("---")
                    # 创建ZIP文件
                    zip_buf = io.BytesIO()
                    with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for file_info in converted_files:
                            zipf.writestr(file_info['filename'], file_info['data'])
                    
                    zip_buf.seek(0)
                    now = datetime.now().strftime("%Y%m%d_%H%M%S")
                    zip_filename = f"converted_all_{now}.zip"
                    st.download_button(
                        "📦 下载所有文件 (ZIP)",
                        data=zip_buf,
                        file_name=zip_filename,
                        mime="application/zip"
                    )
        except Exception as e:
            st.error(f"转换过程出错: {e}")
