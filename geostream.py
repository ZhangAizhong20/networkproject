import re
import streamlit as st
import requests
import geofun as gf
import plotly
key = 'C1124EC93984B81A7614D75B3FF2C3C4'

format = """\n
                        1    41 ms     4 ms     2 ms  10.XXX.XXX.XX\n
                        2     *        *        *     请求超时。\n
                        3     *        *        3 ms  XX.X.5.XX\n
                        4     6 ms     4 ms    19 ms  XX.XX.XX.XX\n
                        5     *        *        *     请求超时。\n
                        6     *        *        *     请求超时。\n
                        7     *        *        *     请求超时。\n
                        8     *        *        *     请求超时。\n
                        9    55 ms    41 ms    40 ms  XX.xx.XX.XX\n
                        10     *       45 ms     *     XX.XX.XX.XX\n
                        11    42 ms    44 ms    46 ms  XX.XX.XX.XXX\n
                        12     *        *        *     请求超时。\n
                        13     *        *        *     请求超时。\n
                        14     *        *        *     请求超时。\n
                        15     *        *        *     请求超时。\n
                        16    40 ms    40 ms    40 ms  XX.XX.XX.XX"
        """


def get_geodata(ip_address):
    payload = {'key':key, 'ip': ip_address, 'format': 'json'}
    api_result = requests.get('https://api.ip2location.io/', params=payload)
    return api_result.json()

def main():
    st.title("IP traceroute")
    st.markdown('input demo (or just ip (with\\n))'+format)
    # 创建一个文本框供用户输入
    text_input = st.text_area("INPUT The result", height=200)

    # 点击按钮后触发的事件
    try:
        if st.button("Handle THE RESULT"):
            # 获取用户输入的文本
            processed_text = process_text(text_input)
            # 显示处理后的文本
            st.markdown("valid IP")
            ip_data,private_ip = gf.get_geolist(text_input)
            st.text(ip_data[['ip','region_name','city_name','time_zone','latitude','longitude']])
            st.write(gf.draw_map(ip_data))
            st.markdown("Private IP")
            st.text(private_ip)
            st.markdown('[Learn More about Private IP](https://blog.csdn.net/linuxjackaroo/article/details/2180793)')

            # if len(ip_list)==0:
            #     print('error')
            # print(ip_list)
            # print(processed_text)
            st.text(processed_text)
    except:st.markdown("Error Happen,please enter the right format or just IP address:"+"\n"+format)
                       
    
    with st.container():
        st.markdown('---')

        st.caption(
            'This is a project for Network communication(RUSH)'
        )
        st.caption('Made by AizhongZhang')
        st.caption('E-mail of author zhangaizhong20@163.com')
        st.caption(
            'IP data source:'
            + '<a href="https://www.ip2location.com/">https://www.ip2location.com/</a>'
            , unsafe_allow_html=True
        )
        st.caption('Copyright © 2023')
def process_text(text):
    # 在这里进行你的文本处理操作
    # 这里只是一个示例，将文本转换为大写
    processed_text = text.upper()
    return processed_text


if __name__ == "__main__":
    main()


# {'ip': '223.120.10.86',
#  'country_code': 'HK',
#  'country_name': 'Hong Kong',
#  'region_name': 'Hong Kong',
#  'city_name': 'Hong Kong',
#  'latitude': 22.28552,
#  'longitude': 114.15769,
#  'zip_code': '-',
#  'time_zone': '+08:00',
#  'asn': '58453',
#  'as': 'Level 30 Tower 1',
#  'is_proxy': False}
# def draw_map(geo_data):