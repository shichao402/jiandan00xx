@echo off 
setlocal EnableDelayedExpansion
cd %~dp0

if "%1" == "h" goto begin 

mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit 

:begin 

scrapy crawl ooxx

python make_wallpaper.py
