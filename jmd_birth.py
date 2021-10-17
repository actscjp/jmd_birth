import pandas as pd
import altair as alt
import streamlit as st
from urllib.parse import urljoin


@st.cache
def get_data():
    base_url = 'http://www.ipss.go.jp/p-toukei/JMD/'
    url_list = []
    birth_list = []
    name_list = []
    for i in range(47):
        if i < 9:
            url_list.append(urljoin(base_url, str(
                0) + str(i+1) + '/STATS/Births.txt'))
        else:
            url_list.append(urljoin(base_url, str(i+1) + '/STATS/Births.txt'))
    for url in url_list:
        birth_list.append(pd.read_csv(url, sep='\s+', skiprows=1))
        name_list.append(pd.read_csv(url, nrows=1).columns[0].split('.')[1])
    for i in range(47):
        birth_list[i]['Pref'] = name_list[i]
    df = pd.concat(birth_list)
    return df, name_list


try:
    st.title('都道府県別出生数の可視化アプリ')

    st.sidebar.write("""
    # 都道府県別出生数
    以下のオプションを指定できます。
    """)
    st.sidebar.write("""
    ## 表示年数選択
    """)
    year = st.sidebar.slider('年数', 1975, 2019, 1975)

    st.sidebar.write("""
    ## 出生数の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください',
        0.0, 200000.0, (0.0, 200000.0)
    )

    st.sidebar.write("""
    ## 性別
    """)
    gender = st.sidebar.selectbox('性別を選択してください',
                                  ('Total', 'Male', 'Female'))

    st.write(f"""
    ### **{year}年**以降の都道府県別の出生数
    """)

    df = get_data()[0]
    name_list = get_data()[1]
    max_year = df['Year'].max()

    prefectures = st.multiselect(
        '都道府県を選択してください',
        name_list,
        ['Tokyo', 'Osaka']
    )

    if not prefectures:
        st.error('少なくとも一つの都道府県を選んでください')
    else:
        data = df[df['Pref'].isin(prefectures) & df['Year'].isin(
            list(range(year, max_year + 1, 1)))]
        st.write("### 出生数（人）", data)

    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x="Year:N",
            y=alt.Y(gender, stack=None, scale=alt.Scale(domain=[ymin, ymax])),
            color='Pref'
        )
    )
    st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        'おっと！なにかエラーが起きているようです。'
    )
