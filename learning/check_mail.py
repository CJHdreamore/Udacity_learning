import time
import webbrowser
total_times = 3
check_time = 0
while(check_time < total_times):
    print("Let's check email from now on " + time.ctime())
    time.sleep(2*60*60)
    webbrowser.open("https://mail.cstnet.cn/coremail/XJS/index.jsp?sid=IAfSmghhwVertDojAghhQVCdcwUlPjOl",
                    'https://mail.qq.com/cgi-bin/frame_html?sid=3brys86-Y-dkSVwF&r=661654678d2e89cb75549cda6bd337a6')
    check_time = check_time + 1

