# 漏洞概述
2021年7月9日

漏洞存在于YAPI的mock脚本服务上，是由于mock脚本自定义服务未对JS脚本加以命令过滤，用户可以添加任何请求处理脚本，攻击者可利用该漏洞在受影响的服务器上执行任意javascript代码，最终导致接管并控制服务器。详见[YAPI开源接口管理平台远程代码执行零日漏洞预警](https://www.secrss.com/articles/32490)

# 参考链接

https://github.com/YMFE/yapi/issues/2233