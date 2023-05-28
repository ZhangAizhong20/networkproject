import re
import ipaddress
import requests

import streamlit as st
import pandas as pd 
import plotly.graph_objects as go
import numpy as np

key = 'C1124EC93984B81A7614D75B3FF2C3C4'

import ipaddress


def is_reserved_ip(ip_address):
    
    ip = ipaddress.ip_address(ip_address)
    return ip.is_private


def get_geodata(ip_address):
    payload = {'key':key, 'ip': ip_address, 'format': 'json'}
    api_result = requests.get('https://api.ip2location.io/', params=payload)
    return api_result.json()

def extract_ip_addresses(trace_text):
    ip_addresses = []
    lines = trace_text.split('\n')
    for line in lines:
        match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
        if match:
            ip_addresses.append(match.group())
    return ip_addresses

def get_geolist(trace_text):
    ip_list = extract_ip_addresses(trace_text)
    geo_data = []
    re_ip = []
    try:
        for ip in ip_list:
            if is_reserved_ip(ip):
                re_ip.append(ip)
            else:
                geo_data.append(get_geodata(ip))
                
        return pd.DataFrame(geo_data),re_ip
    except:return False


def draw_map(locations:pd.DataFrame):
    locations.dropna(subset=['latitude','longitude'],inplace=True)
# 创建地图图表对象
    fig = go.Figure()

    # 添加地图轮廓图层
    fig.add_trace(go.Choroplethmapbox(
        geojson='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json',
        locations=[],
        z=[],
        colorscale='Blues',
        zmin=0,
        zmax=1,
        marker_opacity=0.5,
        marker_line_width=0
    ))

    # 设置地图布局参数
    fig.update_layout(
        mapbox=dict(
            style='carto-positron',
            zoom=1.5,
            center=dict(lat=0, lon=0),
            layers=[]
        ),
        margin=dict(r=0, l=0, t=0, b=0),
        height=600
    )




    l = 0.5  # the arrow length
    widh =0.035 #2*widh is the width of the arrow base as triangle
    frames = []
    frame_data = []
    fig.add_trace(go.Scattermapbox(
            lat=[locations['latitude'][0]],  # 点的纬度
            lon=[locations['longitude'][0]],  # 点的经度
            mode='markers',  # 模式设置为 markers
            marker=dict(
                size=20,  # 点的大小
                color='red'  # 点的颜色
            ),
            # text=['Point 1', 'Point 2', 'Point 3'],  # 点旁边的文字
            # hoverinfo='text'  # 设置悬停时显示的信息为文字
        ))
    for i in range(len(locations)-1):
        try:
            fig.add_trace(go.Scattermapbox(
                lat=[locations['latitude'][i+1]],  # 点的纬度
                lon=[locations['longitude'][i+1]],  # 点的经度
                mode='markers',  # 模式设置为 markers
                marker=dict(
                    size=15,  # 点的大小
                    color='green'  # 点的颜色
                ),
                # text=['Point 1', 'Point 2', 'Point 3'],  # 点旁边的文字
                # hoverinfo='text'  # 设置悬停时显示的信息为文字
            ))
            fig.add_trace(go.Scattermapbox(
            lat = [locations['latitude'][i], locations['latitude'][i+1]], 
            lon = [locations['longitude'][i], locations['longitude'][i+1]],
            mode = 'lines',
            line = dict(width = 1.5, color = 'blue'),
            ))
            A = np.array([locations['longitude'][i], locations['latitude'][i]])
            B = np.array([locations['longitude'][i+1], locations['latitude'][i+1]])
            v = B-A
            w = v/np.linalg.norm(v)     
            u  =np.array([-v[1], v[0]])  #u orthogonal on  w
                    
            P = B-l*w
            S = P - widh*u
            T = P + widh*u
            fig.add_trace(go.Scattermapbox(lon = [S[0], T[0], B[0], S[0]], 
                                        lat =[S[1], T[1], B[1], S[1]], 
                                        mode='lines', 
                                        fill='toself', 
                                        fillcolor='yellow', 
                                        line_color='yellow'))
        except:pass
    # fig.show()
    return fig
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

    