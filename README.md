# A-Pixiv-Crawler
Just a practice of two rookies

## 配置需求
- Python v3+ 解释器
- 一些科学上网方法
- urllib3==1.25.
  11(其它版本可能没法科学上网)
- beautifulsoup4

## 主要功能
基于作者或关键词批量爬取pixiv图片

## 使用
调节参数配置如下：
```angular2html
tag = 0             # 0表示基于关键词，1表示基于作者
author_name = ""    # 作者id
key_tag = ""        # 关键词标签    
end_num =           # 要获取的作品数量
file_path = ""      # 储存图片的路径
```
由于p站新增了reCAPTCHA人机验证

目前的方法是手动输入cookies来绕过登录

自动模拟登录的方法还在尝试中
