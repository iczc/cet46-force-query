# cet46-force-query 

四六级成绩暴力查询。

## Requirements

* Python3

* Packages: [requests](http://www.python-requests.org/)

使用以下命令安装Packages:

```bash
$ pip install -r requirements.txt
```

## Usage

1.修改配置文件`config.ini`

| parameter    | explanation  | 
| :----------- | :----------- | 
| user_name    | 考生姓名      | 
| prefix       | 准考证号前十位 | 
| room_lower   | 起始搜索考场号 | 
| room_upper   | 结束搜索考场号 | 
| seat_lower   | 起始搜索座位号 | 
| seat_upper   | 结束搜索座位号 | 
| api_username | 打码平台用户名 | 
| api_password | 打码平台密码   | 


Tips  
* 打码平台 [注册地址](http://www.ruokuai.com/home/register)，注册充值后将用户名密码填入配置文件。
* 四六级准考证号一共由15位组成，前6位为学校（校区）代码，第7-8位为考试年份，如18即2018年，第9位是指该年中的第几次测试，上半年为1，下半年为2，第10位是四六级类别，四级为1，六级为2；第11-13位是考场号，第14-15位是座位号。


![四六级准考证号说明](https://s1.ax1x.com/2018/10/24/isagcq.png)



2.运行`search.py`开始暴力搜索成绩
```bash
$ python search.py
```
## TODO
异常处理  
使用`SVM`或`CNN`识别查询验证码。