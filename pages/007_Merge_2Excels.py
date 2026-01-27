
import streamlit as st
import pandas as pd
import io
import zipfile
from datetime import datetime

# /d:/Yuxi/dataHub/pages/007_Merge_2Excels.py

st.set_page_config(page_title="合并Excel文件", layout="wide")
st.title("合并 Excel 文件")

st.sidebar.header("上传文件")
left_file = st.sidebar.file_uploader("选择左侧 Excel 文件", type=["xlsx", "xls"], key="left")
right_files = st.sidebar.file_uploader("选择右侧 Excel 文件 (可多个)", type=["xlsx", "xls"], accept_multiple_files=True, key="right")

if left_file and right_files:
    # 读取left Excel
    left_file.seek(0)
    left_df = pd.read_excel(left_file, engine='openpyxl')
    st.subheader("左侧 Excel 预览")
    st.dataframe(left_df.head())

    left_columns = left_df.columns.tolist()
    left_key = st.sidebar.selectbox("选择左侧键列", left_columns, key="left_key")

    # 读取第一个right来获取列
    right_files[0].seek(0)
    right_df_sample = pd.read_excel(right_files[0], engine='openpyxl')
    right_columns = right_df_sample.columns.tolist()
    right_key = st.sidebar.selectbox("选择右侧键列", right_columns, key="right_key")

    join_type = st.sidebar.selectbox("选择合并方式", ["inner", "left", "right", "outer", "left_excluding", "right_excluding", "outer_excluding"])

    # Join类型说明
    with st.expander("合并方式说明"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Inner Join")
            st.write("只保留两侧都匹配的行。")
            st.image("imgs/inner_join.png", caption="Inner Join")

            st.subheader("Left Join")
            st.write("保留左侧所有行，右侧匹配的行。右侧不匹配的行用NaN填充。")
            st.image("imgs/left_join.png", caption="Left Join")

            st.subheader("Right Join")
            st.write("保留右侧所有行，左侧匹配的行。左侧不匹配的行用NaN填充。")
            st.image("imgs/right_join.png", caption="Right Join")

        with col2:
            st.subheader("Outer Join (Full Join)")
            st.write("保留两侧所有行，不匹配的用NaN填充。")
            st.image("imgs/outer_join.png", caption="Outer Join")

            st.subheader("Left Excluding Join")
            st.write("只保留左侧不匹配的行（右侧无对应）。")
            st.image("imgs/left_excluding_join.png", caption="Left Excluding Join")

        with col3:
            st.subheader("Right Excluding Join")
            st.write("只保留右侧不匹配的行（左侧无对应）。")
            st.image("imgs/right_excluding_join.png", caption="Right Excluding Join")

            st.subheader("Outer Excluding Join")
            st.write("只保留两侧都不匹配的行。")
            st.image("imgs/outer_excluding_join.png", caption="Outer Excluding Join")

    st.markdown("---")
    st.subheader(f"合并结果 (使用 {join_type} join)")

    merged_files = {}

    for rf in right_files:
        st.markdown(f"**合并右侧文件: {rf.name}**")
        try:
            rf.seek(0)
            right_df = pd.read_excel(rf, engine='openpyxl')

            # 合并
            if join_type in ['inner', 'left', 'right', 'outer']:
                merged_df = pd.merge(left_df, right_df, left_on=left_key, right_on=right_key, how=join_type, suffixes=('_left', '_right'))
            elif join_type == 'left_excluding':
                merged_df = pd.merge(left_df, right_df, left_on=left_key, right_on=right_key, how='left', suffixes=('_left', '_right'))
                merged_df = merged_df[merged_df[right_key].isnull()]
            elif join_type == 'right_excluding':
                merged_df = pd.merge(left_df, right_df, left_on=left_key, right_on=right_key, how='right', suffixes=('_left', '_right'))
                merged_df = merged_df[merged_df[left_key].isnull()]
            elif join_type == 'outer_excluding':
                merged_df = pd.merge(left_df, right_df, left_on=left_key, right_on=right_key, how='outer', suffixes=('_left', '_right'))
                merged_df = merged_df[merged_df[left_key].isnull() | merged_df[right_key].isnull()]

            st.write(f"合并后行数: {len(merged_df)}")
            st.dataframe(merged_df.head())

            # 保存合并结果
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                merged_df.to_excel(writer, index=False)
            buf.seek(0)
            merged_filename = f"{left_file.name.replace('.xlsx', '').replace('.xls', '')}_{rf.name.replace('.xlsx', '').replace('.xls', '')}_merged.xlsx"
            merged_files[merged_filename] = buf.getvalue()

            st.download_button(
                label=f"下载 {merged_filename}",
                data=buf,
                file_name=merged_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"合并文件 {rf.name} 时出错: {e}")

    # 下载所有文件为ZIP
    if merged_files:
        st.markdown("---")
        st.subheader("批量下载")

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename, content in merged_files.items():
                zipf.writestr(filename, content)

        zip_buffer.seek(0)
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"merged_all_{now}.zip"

        st.download_button(
            label="📦 下载所有文件 (ZIP)",
            data=zip_buffer,
            file_name=zip_filename,
            mime="application/zip"
        )
else:
    st.info("请上传左侧和右侧的 Excel 文件")
