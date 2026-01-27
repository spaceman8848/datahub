
import streamlit as st
import pandas as pd
import io
import zipfile
from datetime import datetime
from collections import defaultdict

# /d:/Yuxi/dataHub/pages/004_CSV_Data_Cleaning.py

def apply_filters(df, filters, logic="AND"):
    """应用筛选条件

    Args:
        df: DataFrame
        filters: 筛选条件列表
        logic: 条件之间的逻辑关系，"AND" 或 "OR"
    """
    if not filters:
        return df

    # 存储每个条件的筛选结果
    filter_results = []

    for f in filters:
        col = f['column']
        op = f['operator']
        val = f['value']

        if col not in df.columns:
            st.warning(f"列 '{col}' 不存在于数据中，跳过此筛选条件")
            continue

        # 创建一个布尔Series来存储当前条件的筛选结果
        mask = pd.Series([False] * len(df), index=df.index)

        try:
            if op == 'equals':
                mask = df[col] == val
            elif op == 'not equal':
                mask = df[col] != val
            elif op == 'contains':
                mask = df[col].astype(str).str.contains(str(val), na=False)
            elif op == 'not contain':
                mask = ~df[col].astype(str).str.contains(str(val), na=False)
            elif op == 'start with':
                mask = df[col].astype(str).str.startswith(str(val), na=False)
            elif op == 'end with':
                mask = df[col].astype(str).str.endswith(str(val), na=False)
            elif op == 'less than':
                # 先尝试直接比较，如果失败则转换为数字
                try:
                    mask = df[col] < float(val)
                except:
                    mask = pd.to_numeric(df[col], errors='coerce') < float(val)
            elif op == 'greater than':
                # 先尝试直接比较，如果失败则转换为数字
                try:
                    mask = df[col] > float(val)
                except:
                    mask = pd.to_numeric(df[col], errors='coerce') > float(val)
            elif op == 'less or equal':
                # 先尝试直接比较，如果失败则转换为数字
                try:
                    mask = df[col] <= float(val)
                except:
                    mask = pd.to_numeric(df[col], errors='coerce') <= float(val)
            elif op == 'greater or equal':
                # 先尝试直接比较，如果失败则转换为数字
                try:
                    mask = df[col] >= float(val)
                except:
                    mask = pd.to_numeric(df[col], errors='coerce') >= float(val)
            elif op == 'is null':
                mask = df[col].isnull()
            elif op == 'is not null':
                mask = df[col].notnull()
        except Exception as e:
            st.warning(f"应用筛选条件时出错: {e}")
            continue

        filter_results.append(mask)

    # 根据逻辑关系组合所有筛选结果
    if not filter_results:
        return df

    if logic == "AND":
        # 所有条件都必须满足
        final_mask = filter_results[0]
        for mask in filter_results[1:]:
            final_mask = final_mask & mask
    else:
        # 至少满足一个条件
        final_mask = filter_results[0]
        for mask in filter_results[1:]:
            final_mask = final_mask | mask

    return df[final_mask]

st.set_page_config(page_title="CSV数据清洗", layout="wide")
st.title("CSV 数据清洗与筛选")

st.sidebar.header("上传文件")
uploaded_files = st.sidebar.file_uploader("选择 CSV 文件", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    st.sidebar.header("数据清洗设置")
    encoding = st.sidebar.text_input("文件编码", "utf-8", help="例如 utf-8 或 gbk")
    header_option = st.sidebar.selectbox("包含表头(header)", ["有表头 (第一行为列名)", "无表头"], index=0)

    # Resize options
    st.sidebar.subheader("数据调整 (Resize)")
    skip_rows = st.sidebar.number_input("跳过前N行", min_value=0, value=0)
    has_header_in_skipped = st.sidebar.checkbox("跳过的行包含列名", value=False,
                                               help="如果选中，表示跳过的行中包含列名，跳过后的第一行将作为列名")
    take_rows = st.sidebar.number_input("取前N行 (0表示全部)", min_value=0, value=0)

    # Get columns from first file for selection
    first_file = uploaded_files[0]
    first_file.seek(0)

    # Determine header for sample reading
    sample_read_kwargs = {'encoding': encoding, 'nrows': 5}
    if skip_rows > 0 and has_header_in_skipped:
        sample_read_kwargs['skiprows'] = skip_rows
        sample_read_kwargs['header'] = 0
    else:
        # When not skipping header rows, always use first row as header
        sample_read_kwargs['header'] = 0
        if skip_rows > 0:
            # Read more rows to account for rows to be dropped
            sample_read_kwargs['nrows'] = 5 + skip_rows

    sample_df = pd.read_csv(first_file, **sample_read_kwargs)

    # If not skipping header rows but skip_rows > 0, drop the skipped rows
    if skip_rows > 0 and not has_header_in_skipped:
        sample_df = sample_df.drop(index=range(2, min(skip_rows + 2, len(sample_df))))

    available_columns = sample_df.columns.tolist()

    selected_columns = st.sidebar.multiselect("选择列 (留空选择全部)", available_columns, default=available_columns)

    st.markdown("---")
    st.subheader("筛选条件 (Filters)")

    # Dynamic filter addition
    if 'filters' not in st.session_state:
        st.session_state.filters = []

    # 条件之间的逻辑关系
    if st.session_state.filters:
        filter_logic = st.sidebar.radio(
            "条件之间的逻辑关系",
            ["AND (所有条件都必须满足)", "OR (至少满足一个条件)"],
            index=0,
            help="选择多个筛选条件之间的逻辑关系"
        )
    else:
        filter_logic = "AND"

    col_add, col_clear = st.columns([1,1])
    with col_add:
        if st.button("➕ 添加筛选条件"):
            st.session_state.filters.append({'column': available_columns[0] if available_columns else '', 'operator': 'equals', 'value': ''})

    with col_clear:
        if st.button("🗑️ 清空所有条件"):
            st.session_state.filters = []

    # Display and edit filters
    operators = ['equals', 'not equal', 'contains', 'not contain', 'start with', 'end with',
                'less than', 'greater than', 'less or equal', 'greater or equal', 'is null', 'is not null']

    filters_to_remove = []
    for i, f in enumerate(st.session_state.filters):
        st.markdown(f"**条件 {i+1}**")
        col1, col2, col3, col4 = st.columns([2,2,2,1])
        with col1:
            f['column'] = st.selectbox(f"列 {i+1}", available_columns,
                                     index=available_columns.index(f['column']) if f['column'] in available_columns else 0,
                                     key=f"col_{i}")
        with col2:
            f['operator'] = st.selectbox(f"操作 {i+1}", operators,
                                        index=operators.index(f['operator']),
                                        key=f"op_{i}")
        with col3:
            f['value'] = st.text_input(f"值 {i+1}", value=f['value'], key=f"val_{i}")
        with col4:
            if st.button("删除", key=f"del_{i}"):
                filters_to_remove.append(i)

    # Remove filters
    for i in reversed(filters_to_remove):
        st.session_state.filters.pop(i)

    st.markdown("---")
    st.subheader("处理结果")

    cleaned_files = {}

    for f in uploaded_files:
        st.markdown(f"**处理文件: {f.name}**")
        try:
            f.seek(0)

            # Read with resize options
            read_kwargs = {
                'encoding': encoding,
                'nrows': take_rows if take_rows > 0 else None,
                'usecols': selected_columns if selected_columns else None
            }

            if skip_rows > 0 and has_header_in_skipped:
                read_kwargs['skiprows'] = skip_rows
                read_kwargs['header'] = 0
            else:
                # When not skipping header rows, use first row as header
                read_kwargs['header'] = 0

            df = pd.read_csv(f, **read_kwargs)

            # If not skipping header rows but skip_rows > 0, drop the skipped rows from second row onwards
            if skip_rows > 0 and not has_header_in_skipped:
                df = df.drop(index=range(0, min(skip_rows, len(df))))
            if take_rows > 0 and 'nrows' not in read_kwargs:
                df = df.head(take_rows)

            # Apply filters
            if st.session_state.filters:
                # 确定逻辑关系
                logic = "AND" if filter_logic.startswith("AND") else "OR"
                df = apply_filters(df, st.session_state.filters, logic=logic)

            st.write(f"处理后行数: {len(df)}")
            st.dataframe(df.head())

            # Convert to CSV
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()

            cleaned_filename = f.name.replace('.csv', '_cleaned.csv')
            cleaned_files[cleaned_filename] = csv_data

            st.download_button(
                label=f"下载 {cleaned_filename}",
                data=csv_data,
                file_name=cleaned_filename,
                mime='text/csv'
            )

        except Exception as e:
            st.error(f"处理文件 {f.name} 时出错: {e}")

    # Download all files as ZIP
    if cleaned_files:
        st.markdown("---")
        st.subheader("批量下载")

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename, content in cleaned_files.items():
                zipf.writestr(filename, content)

        zip_buffer.seek(0)
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"cleaned_all_{now}.zip"

        st.download_button(
            label="📦 下载所有文件 (ZIP)",
            data=zip_buffer,
            file_name=zip_filename,
            mime="application/zip"
        )
