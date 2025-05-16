import json
import os
import streamlit as st

def load_config(config_path="config.json"):
    if not os.path.exists(config_path):
        st.error("无配置文件")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError:
        st.error(f"配置文件格式错误")
        return None
    except Exception as e:
        st.exception(e)
        return None
