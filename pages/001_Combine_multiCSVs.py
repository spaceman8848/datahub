import streamlit as st
import pandas as pd
import io
import datetime

# /d:/Yuxi/dataHub/pages/001_Combine_multiCSVs.py

st.set_page_config(page_title="合并多个CSV", layout="wide")
st.title("合并多个 CSV 文件到一个 CSV")

st.sidebar.header("设置")
sep = st.sidebar.selectbox("分隔符", [",", "\t", ";", "|"], index=0, help="选择 CSV 的分隔符")
encoding = st.sidebar.text_input("文件编码", "utf-8", help="例如 utf-8 或 gbk")
header_option = st.sidebar.selectbox("包含表头(header)", ["有表头 (第一行为列名)", "无表头"], index=0)
ignore_index = st.sidebar.checkbox("重建索引 (ignore_index=True)", value=True)
drop_duplicates = st.sidebar.checkbox("去重 (基于全部列)", value=False)
join_mode = st.sidebar.selectbox("合并方向", ["按行合并 (concat rows)", "按列合并 (concat columns)"], index=0)
how_outer = st.sidebar.selectbox("行合并时列对齐方式", ["outer", "inner"], index=0)  # only for rows

st.markdown("拖拽或选择多个 CSV 文件上传（支持不同文件名）:")
uploaded_files = st.file_uploader("选择 CSV 文件", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    dfs = []
    errors = []
    for f in uploaded_files:
        try:
            # reset file pointer if needed
            f.seek(0)
            if header_option.startswith("有"):
                df = pd.read_csv(f, sep=sep, encoding=encoding)
            else:
                df = pd.read_csv(f, sep=sep, encoding=encoding, header=None)
            # add source filename column for traceability
            df["_source_filename"] = getattr(f, "name", "uploaded")
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
                csv_bytes = combined.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
                buf.write(csv_bytes)
                buf.seek(0)
                now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"combined_{now}.csv"
                st.download_button("下载合并后的 CSV", data=buf, file_name=filename, mime="text/csv")
            except Exception as e:
                st.error(f"合并失败: {e}")
else:
    st.info("请在上方上传至少一个 CSV 文件以开始合并。")