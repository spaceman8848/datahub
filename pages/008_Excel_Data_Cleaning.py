
import streamlit as st
import pandas as pd
import io
from datetime import datetime

# /d:/Yuxi/dataHub/pages/008_Excel_Data_Cleaning.py

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

st.set_page_config(page_title="Excel数据清洗", layout="wide")
st.title("Excel 数据清洗与筛选")

st.sidebar.header("上传文件")
uploaded_file = st.file_uploader("选择 Excel 文件", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # 数据预览
        st.write("原始数据预览")
        st.dataframe(df.head(200))
        st.write(f"总行数: {len(df)}, 总列数: {len(df.columns)}")

        # 缺失值分析
        st.subheader("缺失值分析")
        missing_stats = pd.DataFrame({
            '列名': df.columns,
            '缺失值数量': df.isnull().sum().values,
            '缺失值比例(%)': (df.isnull().sum() / len(df) * 100).values
        })
        st.dataframe(missing_stats)

        # 数据类型信息
        st.subheader("数据类型信息")
        dtypes_df = pd.DataFrame({
            '列名': df.columns,
            '数据类型': df.dtypes.values,
            '唯一值数量': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(dtypes_df)

        # 清洗选项
        st.sidebar.header("清洗选项")
        missing_handling = st.sidebar.selectbox(
            "缺失值处理",
            ["保留", "删除含缺失值的行", "填充缺失值"],
            help="选择如何处理数据中的缺失值"
        )

        df_cleaned = df.copy()

        if missing_handling == "删除含缺失值的行":
            df_cleaned = df.dropna()
            st.write(f"删除含缺失值的行后: {len(df_cleaned)} 行 (原 {len(df)} 行)")
        elif missing_handling == "填充缺失值":
            fill_value = st.sidebar.text_input("填充值", "0", help="用于填充缺失值的默认值")
            try:
                # 尝试将填充值转换为数字
                try:
                    fill_value = float(fill_value)
                except ValueError:
                    pass  # 保持为字符串

                df_cleaned = df.fillna(fill_value)
                st.write(f"已用 '{fill_value}' 填充缺失值")
            except Exception as e:
                st.error(f"填充缺失值失败: {e}")

        # 数据筛选 - 参照004脚本
        st.sidebar.header("数据筛选")

        # 动态添加筛选条件
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
                available_columns = df_cleaned.columns.tolist()
                st.session_state.filters.append({'column': available_columns[0] if available_columns else '', 'operator': 'equals', 'value': ''})

        with col_clear:
            if st.button("🗑️ 清空所有条件"):
                st.session_state.filters = []

        # 显示和编辑筛选条件
        operators = ['equals', 'not equal', 'contains', 'not contain', 'start with', 'end with',
                    'less than', 'greater than', 'less or equal', 'greater or equal', 'is null', 'is not null']

        filters_to_remove = []
        for i, f in enumerate(st.session_state.filters):
            st.markdown(f"**条件 {i+1}**")
            col1, col2, col3, col4 = st.columns([2,2,2,1])
            with col1:
                available_columns = df_cleaned.columns.tolist()
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

        # 移除筛选条件
        for i in reversed(filters_to_remove):
            st.session_state.filters.pop(i)

        # 应用筛选条件
        if st.session_state.filters:
            # 确定逻辑关系
            logic = "AND" if filter_logic.startswith("AND") else "OR"
            df_cleaned = apply_filters(df_cleaned, st.session_state.filters, logic=logic)
            st.write(f"应用筛选条件后 ({filter_logic}): {len(df_cleaned)} 行")

        # 数据类型转换
        st.sidebar.header("数据类型转换")
        convert_col = st.sidebar.selectbox("选择要转换的列", options=df_cleaned.columns)

        if convert_col:
            convert_to = st.sidebar.selectbox(
                "转换类型",
                ["不转换", "数值型", "字符串", "日期时间"],
                help="选择目标数据类型"
            )

            if convert_to != "不转换":
                try:
                    if convert_to == "数值型":
                        df_cleaned[convert_col] = pd.to_numeric(df_cleaned[convert_col], errors='coerce')
                        st.write(f"已将列 '{convert_col}' 转换为数值型")
                    elif convert_to == "字符串":
                        df_cleaned[convert_col] = df_cleaned[convert_col].astype(str)
                        st.write(f"已将列 '{convert_col}' 转换为字符串")
                    elif convert_to == "日期时间":
                        df_cleaned[convert_col] = pd.to_datetime(df_cleaned[convert_col], errors='coerce')
                        st.write(f"已将列 '{convert_col}' 转换为日期时间")
                except Exception as e:
                    st.error(f"数据类型转换失败: {e}")

        # 显示清洗后数据
        st.subheader("清洗后数据预览")
        st.dataframe(df_cleaned.head(200))
        st.write(f"最终行数: {len(df_cleaned)}, 列数: {len(df_cleaned.columns)}")

        # 下载功能
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as writer:
            df_cleaned.to_excel(writer, index=False)
        buf.seek(0)
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cleaned_{now}.xlsx"
        st.download_button(
            "下载清洗后的 Excel",
            data=buf,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"读取文件失败: {e}")
else:
    st.info("请上传一个 Excel 文件")
