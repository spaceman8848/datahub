import streamlit as st
import pandas as pd
import io
import zipfile
from collections import defaultdict

# /d:/Yuxi/dataHub/pages/004_CSV_Data_Cleaning.py

def apply_filters(df, filters):
    """应用筛选条件"""
    for f in filters:
        col = f['column']
        op = f['operator']
        val = f['value']
        
        if col not in df.columns:
            st.warning(f"列 '{col}' 不存在于数据中，跳过此筛选条件")
            continue
        
        if op == 'equals':
            df = df[df[col] == val]
        elif op == 'not equal':
            df = df[df[col] != val]
        elif op == 'contains':
            df = df[df[col].astype(str).str.contains(str(val), na=False)]
        elif op == 'not contain':
            df = df[~df[col].astype(str).str.contains(str(val), na=False)]
        elif op == 'start with':
            df = df[df[col].astype(str).str.startswith(str(val), na=False)]
        elif op == 'end with':
            df = df[df[col].astype(str).str.endswith(str(val), na=False)]
        elif op == 'less than':
            try:
                df = df[pd.to_numeric(df[col], errors='coerce') < float(val)]
            except:
                st.warning(f"列 {col} 无法转换为数字进行比较")
        elif op == 'greater than':
            try:
                df = df[pd.to_numeric(df[col], errors='coerce') > float(val)]
            except:
                st.warning(f"列 {col} 无法转换为数字进行比较")
        elif op == 'less or equal':
            try:
                df = df[pd.to_numeric(df[col], errors='coerce') <= float(val)]
            except:
                st.warning(f"列 {col} 无法转换为数字进行比较")
        elif op == 'greater or equal':
            try:
                df = df[pd.to_numeric(df[col], errors='coerce') >= float(val)]
            except:
                st.warning(f"列 {col} 无法转换为数字进行比较")
        elif op == 'is null':
            df = df[df[col].isnull()]
        elif op == 'is not null':
            df = df[df[col].notnull()]
    return df

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
                df = apply_filters(df, st.session_state.filters)
            
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
    
    # Batch download
    if cleaned_files:
        st.markdown("---")
        st.subheader("批量下载清洗结果")
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename, data in cleaned_files.items():
                zip_file.writestr(filename, data)
        
        zip_data = zip_buffer.getvalue()
        
        st.download_button(
            label="下载所有清洗CSV文件 (ZIP)",
            data=zip_data,
            file_name="cleaned_csv_files.zip",
            mime="application/zip"
        )
else:
    st.info("请上传CSV文件以开始数据清洗。")