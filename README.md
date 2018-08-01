运行方式，先用requirements.txt 安装需要的库后，直接运行run.py
移植的前端模板为 http://ace.jeka.by/search.html
由于移植得到的前端页面太多，我把我们的放到/template/used目录下，template/used目录下的每个html只需要
填充page_content，一般套路是在page_content定义一个id，然后通过ajax动态生成。
HuobiService.py HuohbiUtil.py这两个是用于火币调用api
