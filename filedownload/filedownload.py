import os
import requests
import pandas as pd
import logging
import urllib3
from urllib.parse import quote

# 配置日志记录器
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='download_log.log',  # 指定日志文件名称，可根据需要修改路径和文件名
                    filemode='w')  # 'w'表示每次运行覆盖原日志文件内容，若用'a'则为追加模式
logger = logging.getLogger(__name__)

# 读取CSV文件数据，这里假设已经能正确读取，编码等问题已解决
#data = pd.read_csv(r'C:\Users\77820\Desktop\filedownload.csv', encoding='utf-8')
data = pd.read_csv(r'/usr/python/filedownload/file_2020.csv', encoding='utf-8')
# 指定下载附件的保存目录的基础路径，可根据实际情况调整
#base_save_directory = r'C:\Users\77820\Desktop\downloaded_attachments'
base_save_directory = r'/usr/file'
if not os.path.exists(base_save_directory):
    os.makedirs(base_save_directory)
for index, row in data.iterrows():
    
    #url = 'https://kjj1.jiaxing.gov.cn/'+row['Url']
    url = 'https://10.254.115.81:8084/'+row['Url']
    try:
        # 解析URL获取路径部分，用于创建文件夹结构
        url_path = "/".join(url.split("/")[3:])  # 去掉协议和域名部分，获取后面的路径部分，可根据实际URL结构调整
        dir_path = os.path.dirname(row['Url'])
        save_path = base_save_directory + dir_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        print(save_path)
          # 获取附件的文件名，这里假设URL中最后一部分是文件名，可根据实际情况调整获取文件名的方式
        file_name = url.split('/')[-1]
        file_path = os.path.join(save_path, file_name)

        # 判断附件是否已经存在，如果存在则跳过当前附件的下载
        if os.path.exists(file_path):
            print(f"附件 {file_name} 已存在，跳过下载")
            continue
            
        s_utf8 = url.encode('utf-8').decode('utf-8')
         # 发送HTTP请求获取附件内容，配置证书验证并添加请求头
        response = requests.get(quote(s_utf8, safe=':/'), stream=True, verify=False)
        response.raise_for_status()  # 如果请求出现4xx、5xx等错误，抛出异常

        # 获取附件的文件名，这里假设URL中最后一部分是文件名，可根据实际情况调整获取文件名的方式
        file_name = url.split('/')[-1]
        file_path = os.path.join(save_path, file_name)

        # 以二进制写入模式打开文件，并将获取到的附件内容写入文件
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        #logger.info(f"附件 {file_name} 已成功下载到 {dir_path}")
    except requests.RequestException as e:
        logger.error(f"下载附件 {row['Url']} 时出现错误: {e}")