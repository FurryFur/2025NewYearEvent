import pandas as pd
import requests
import streamlit as st

if "year1" not in st.session_state:
    st.session_state.year1 = [0]
    st.session_state.year2 = [0]
    st.session_state.count = 0


def get_external_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    if response.status_code != 200:
        return "Unknown"
    data = response.json()
    return data.get("ip")


if "external_ip" not in st.session_state:
    st.session_state.external_ip = get_external_ip()


def add_one_year_1():
    st.session_state.year1.append(st.session_state.year1[-1] + 1)
    st.session_state.year2.append(st.session_state.year2[-1])
    st.session_state.count += 1


def add_two_year_1():
    st.session_state.year1.append(st.session_state.year1[-1] + 2)
    st.session_state.year2.append(st.session_state.year2[-1])
    st.session_state.count += 1


def add_one_year_2():
    st.session_state.year1.append(st.session_state.year1[-1])
    st.session_state.year2.append(st.session_state.year2[-1] + 1)
    st.session_state.count += 1


def add_two_year_2():
    st.session_state.year1.append(st.session_state.year1[-1])
    st.session_state.year2.append(st.session_state.year2[-1] + 2)
    st.session_state.count += 1


def get_year_1():
    return st.session_state.year1[-1]


def get_year_2():
    return st.session_state.year2[-1]


def get_year_log():
    df = pd.DataFrame(
        {"年兽1": st.session_state.year1, "年兽2": st.session_state.year2},
        index=range(st.session_state.count + 1),
    )
    return df


def reset():
    st.session_state.year1 = [0]
    st.session_state.year2 = [0]
    st.session_state.count = 0


# markdown
st.markdown(f"FurryFurCon 2025 Guangdong @ {st.session_state.external_ip}")

# 设置网页标题
st.header("特雷亚大陆的故事 新春特辑2025")
st.title("一起喂年兽 @ 冒险者公会 (A2)")

st.line_chart(get_year_log())

col1, col2 = st.columns(2)

with col1:
    st.button(
        "年兽1投喂高级食材卡",
        on_click=add_two_year_1,
        type="primary",
    )
    st.button("年兽1投喂普通食材卡", on_click=add_one_year_1)
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with col2:
    st.button(
        "年兽2投喂高级食材卡",
        on_click=add_two_year_2,
        type="primary",
    )
    st.button("年兽2投喂普通食材卡", on_click=add_one_year_2)
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

st.button("重置", on_click=reset)
