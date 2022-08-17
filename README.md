# A-Pixiv-Crawler
Just a practice of two rookies

## 配置需求
- Python v3+ 解释器
- 一些科学上网方法
- 以及写在requirements.txt中的package需求

## 主要功能

- 基于不同模式获取pixiv资源
  - 作者
  - 关键词
  - 排行榜
- 可分辨并获取的不同类型资源
  - jpg, png等格式的图片
  - gif动图

## 使用
调节参数配置如下：
```angular2html
mode = 0            # 爬取模式
author_name = ""    # 作者id
key_tag = ''        # 关键词标签
end_num =           # 要获取的作品数量
file_path = ""      # 图片存放地址
sleep_time = 2      # 爬虫休眠间隔
```
由于p站新增了reCAPTCHA人机验证，
目前的方法是输入cookies来绕过登录

请在**catch_pixiv文件夹下新建cookie.txt**

并复制您访问的pixiv的cookie

***

首次输入后将记录cookie，直到cookie失效后会提醒重新输入

自动模拟登录的方法还在尝试中
