import streamlit as st
import pandas as pd

# 1. Loading the dataset
df = pd.read_excel("data/table.xlsx")

# 2. Preprocessing the dataset
df["Bionic prototype"] = df["Bionic prototype"].str.strip()
df["Materials"] = df["Materials"].str.split(";").apply(lambda x: [material.strip() for material in x])
df["Method"] = df["Method"].str.split(";").apply(lambda x: [method.strip() for method in x])
df["Multifunction"] = df["Multifunction"].str.split(";").apply(lambda x: [multifunction.strip() for multifunction in x])

# 3. Saving the processed dataset
# df.to_excel("data/filtered_table.xlsx", index=False)

# 4. Extracting a unique list for each column
bionic_prototype_list = df["Bionic prototype"].unique()
method_list = df["Method"].explode().unique()
multifunction_list = df["Multifunction"].explode().unique()
bionic_prototype_list.sort()
method_list.sort()
multifunction_list.sort()

with st.sidebar:
    st.slider(
        label="Search results limit",
        min_value=1,
        max_value=50,
        value=20,
        step=1,
        key="limit",
        help="Limit the number of search results",
    )

    st.multiselect(
        label="Display columns",
        options=["Bionic prototype", "Multifunction", "Method", "Materials", "Res"],
        default=["Bionic prototype", "Multifunction", "Method", "Materials", "Res"],
        help="Select columns to display in the search results",
        key="display_columns",
    )

st.title("Bionic Path Selection")

st.multiselect(
    label="Multifunction",
    options=multifunction_list,
    default=[],
    help="Select the multifunction to display in the search results",
    placeholder="Select the multifunction to display in the search results",
    key="multifunction_option"
)

st.session_state.disabled = False if len(st.session_state.multifunction_option) > 0 else True

left_col, right_col = st.columns(2)
with left_col:
    st.selectbox(
        label="Bionic prototype",
        options=bionic_prototype_list,
        help="Select the bionic prototype to display in the search results",
        placeholder="Select the bionic prototype to display in the search results",
        index=None,
        key="bionic_prototype_option",
        disabled=st.session_state.disabled
    )
with right_col:
    st.multiselect(
        label="Method",
        options=method_list,
        default=[],
        help="Select the method to display in the search results",
        placeholder="Select the method to display in the search results",
        key="method_option",
        disabled=st.session_state.disabled
    )

search = st.button("Search")
if search:
    multifunction_option = st.session_state.multifunction_option
    bionic_prototype_option = st.session_state.bionic_prototype_option
    method_option = st.session_state.method_option

    # Filter the multifunction column
    filtered_df = df[
        df["Multifunction"].apply(lambda x: all(multifunction in x for multifunction in multifunction_option))]
    # Filter the bionic prototype column
    filtered_df = filtered_df[filtered_df["Bionic prototype"] == bionic_prototype_option] \
        if (bionic_prototype_option is not None and not st.session_state.disabled and not filtered_df.empty) \
        else filtered_df
    # Filter the method column
    filtered_df = filtered_df[filtered_df["Method"].apply(lambda x: any(method in x for method in method_option))] \
        if (len(method_option) > 0 and not st.session_state.disabled and not filtered_df.empty) \
        else filtered_df

    st.dataframe(filtered_df[st.session_state.display_columns].head(st.session_state.limit))
