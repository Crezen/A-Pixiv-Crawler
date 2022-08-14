# A-Pixiv-Crawler
Just a practice of two rookies

## 配置需求
- Python v3+ 解释器
- 一些科学上网方法
- urllib3==1.25.
  11(其它版本可能没法科学上网)
- beautifulsoup4
- lxml
- requests
- 及这些包的依赖项

之后将编写成requirements.txt

## 主要功能
基于作者或关键词批量爬取pixiv图片

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

*首次输入后将记录cookie，直到cookie失效后会提醒重新输入*
### 自动模拟登录的方法还在尝试中
