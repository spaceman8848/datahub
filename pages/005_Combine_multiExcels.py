
import streamlit as st
import pandas as pd
import io
from datetime import datetime

# /d:/Yuxi/dataHub/pages/005_Combine_multiExcels.py

st.set_page_config(page_title="合并多个Excel", layout="wide")
st.title("合并多个 Excel 文件到一个 Excel")

st.sidebar.header("设置")
sheet_name_option = st.sidebar.selectbox(
    "选择工作表",
    ["第一个工作表", "所有工作表"],
    help="选择读取每个Excel文件的工作表方式"
)
ignore_index = st.sidebar.checkbox("重建索引 (ignore_index=True)", value=True)
drop_duplicates = st.sidebar.checkbox("去重 (基于全部列)", value=False)
join_mode = st.sidebar.selectbox("合并方向", ["按行合并 (concat rows)", "按列合并 (concat columns)"], index=0)
how_outer = st.sidebar.selectbox("行合并时列对齐方式", ["outer", "inner"], index=0)  # only for rows

st.markdown("拖拽或选择多个 Excel 文件上传（支持不同文件名）:")
uploaded_files = st.file_uploader("选择 Excel 文件", type=["xlsx", "xls"], accept_multiple_files=True)

if uploaded_files:
    dfs = []
    errors = []
    for f in uploaded_files:
        try:
            # reset file pointer if needed
            f.seek(0)
            filename = getattr(f, "name", "uploaded")

            if sheet_name_option == "第一个工作表":
                df = pd.read_excel(f, engine='openpyxl')
                # 获取第一个工作表名称
                excel_file = pd.ExcelFile(f, engine='openpyxl')
                sheet_name = excel_file.sheet_names[0]
                # 格式化为"文件名_sheet名"
                df["_source_filename"] = f"{filename}_{sheet_name}"
            else:
                # 读取所有工作表并合并
                excel_file = pd.ExcelFile(f, engine='openpyxl')
                sheets_dfs = []
                for sheet in excel_file.sheet_names:
                    sheet_df = pd.read_excel(excel_file, sheet_name=sheet, engine='openpyxl')
                    # 格式化为"文件名_sheet名"
                    sheet_df["_source_filename"] = f"{filename}_{sheet}"
                    sheets_dfs.append(sheet_df)
                df = pd.concat(sheets_dfs, ignore_index=True)

            dfs.append(df)
        except Exception as e:
            errors.append(f"{getattr(f, 'name', 'file')}: {e}")

    if errors:
        st.error("部分文件读取失败：\n" + "\n".join(errors))

    if dfs:
        st.write(f"已读取 {len(dfs)} 个文件，总行数（未合并）: " + str(sum(len(x) for x in dfs)))
        st.dataframe(dfs[0].head())

        if st.button("执行合并"):
            try:
                if join_mode.startswith("按行"):
                    combined = pd.concat(dfs, axis=0, ignore_index=ignore_index, join=how_outer)
                else:
                    # 按列合并：按最短或最长? 这里采用 axis=1，重建索引以保证对齐
                    combined = pd.concat(dfs, axis=1)
                    if ignore_index:
                        combined.reset_index(drop=True, inplace=True)

                if drop_duplicates:
                    before = len(combined)
                    combined.drop_duplicates(inplace=True)
                    st.write(f"去重：{before} -> {len(combined)} 行")

                st.success(f"合并完成，结果 {combined.shape[0]} 行 x {combined.shape[1]} 列")
                st.dataframe(combined.head(200))

                # 准备下载
                buf = io.BytesIO()
                with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                    combined.to_excel(writer, index=False)
                buf.seek(0)
                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"combined_{now}.xlsx"
                st.download_button(
                    "下载合并后的 Excel",
                    data=buf,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"合并失败: {e}")
