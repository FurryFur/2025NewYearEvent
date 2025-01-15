import pandas as pd
import requests
import streamlit as st

if "debonce" not in st.session_state:
    st.session_state.debonce = 0

if "db" not in st.session_state:
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi

    try:
        uri = st.secrets["DB_STR"]
    except Exception:
        import os

        from dotenv import load_dotenv

        load_dotenv()
        uri = os.getenv("DB_STR")

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi("1"))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        database = client["nianshou"]
        collection = database["2025"]
        st.session_state.data = collection
        st.success("数据库成功，持久化功能已启用。")

    except Exception as e:
        # show warn message
        st.warning("数据库失败，转入临时模式，刷新页面会丢失数据。")
        print(e)

# retrive year1, year2, count from db
if "year1" not in st.session_state:
    st.session_state.year1 = [0]
    st.session_state.year2 = [0]
    st.session_state.count = 0
    if "data" in st.session_state:
        collection = st.session_state.data
        if data := collection.find_one():
            st.session_state.year1 = data["year1"]
            st.session_state.year2 = data["year2"]
            st.session_state.count = data["count"]


def get_external_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    if response.status_code != 200:
        return "Unknown"
    data = response.json()
    return data.get("ip")


if "external_ip" not in st.session_state:
    st.session_state.external_ip = get_external_ip()


def add_one_year_1():
    st.session_state.debonce += 1
    st.session_state.year1.append(st.session_state.year1[-1] + 1)
    st.session_state.year2.append(st.session_state.year2[-1])
    st.session_state.count += 1


def add_two_year_1():
    st.session_state.debonce += 1
    st.session_state.year1.append(st.session_state.year1[-1] + 2)
    st.session_state.year2.append(st.session_state.year2[-1])
    st.session_state.count += 1


def add_one_year_2():
    st.session_state.debonce += 1
    st.session_state.year1.append(st.session_state.year1[-1])
    st.session_state.year2.append(st.session_state.year2[-1] + 1)
    st.session_state.count += 1


def add_two_year_2():
    st.session_state.debonce += 1
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
    st.session_state.debonce = 0


if "validated" not in st.session_state:
    psw = st.text_input("请输入更新密码", type="password")
    if psw == "chiyuanshixiaozhu":
        st.session_state.validated = True
    else:
        st.error("密码验证失败，您仅能查看数据")

if "validated" in st.session_state and st.session_state.validated:
    st.success("密码验证成功，启动数据更新功能")

# markdown
st.markdown(f"FurryFurCon 2025 Guangdong @ {st.session_state.external_ip}")

# 设置网页标题
st.header("特雷亚大陆的故事 新春特辑 2025")
st.title("一起喂年兽 @ 冒险者公会 (A2)")

st.line_chart(get_year_log(), color=["#4fa28f", "#c74635"])

if "validated" in st.session_state and st.session_state.validated:
    year1btn, year1img, year2btn, year2img = st.columns(4)

    with year1btn:
        st.button(
            "给乙木·凶兽投喂高级食材 x1",
            on_click=add_two_year_1,
            type="primary",
        )
        st.button("给乙木·凶兽投喂普通食材 x1", on_click=add_one_year_1)

    with year1img:
        st.image("./year1.png", width=400)

    with year2btn:
        st.button(
            "给乙木·灵兽投喂高级食材 x1",
            on_click=add_two_year_2,
            type="primary",
        )
        st.button("给乙木·灵兽投喂普通食材卡 x1", on_click=add_one_year_2)

    with year2img:
        st.image("./year2.png", width=400)
else:
    year1, year2 = st.columns(2)
    with year1:
        st.button("拍一下乙木·凶兽")
        st.image("./year1.png", width=400)

    with year2:
        st.button("摸一把乙木·灵兽")
        st.image("./year2.png", width=400)


res, status = st.columns(2)

with res:
    st.button("重置", on_click=reset)
with status:
    if "validated" in st.session_state and st.session_state.validated:
        # sync data to db
        if "data" in st.session_state and st.session_state.debonce % 5 == 0:
            with st.status("正在保存数据到数据库..."):
                collection = st.session_state.data

                update_operation = {
                    "$set": {
                        "year1": st.session_state.year1,
                        "year2": st.session_state.year2,
                        "count": st.session_state.count,
                    }
                }
                collection.update_one({}, update_operation, upsert=True)

                # pop up message
                st.write("数据已经保存到数据库。")
                status.update(label="数据同步完成!", state="complete", expanded=False)
        else:
            with st.status(
                f"目前数据未同步，{5 - st.session_state.debonce % 5} 次更新后自动保存数据"
            ):
                pass
    else:
        with st.status("目前数据未同步，请输入正确的密码"):
            pass
