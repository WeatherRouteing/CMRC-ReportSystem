import os


def read_estimate_report(ship_name,line_num):
    test_report = "\\\\10.28.16.194\\micapsdata\\航线评估报\\" + ship_name + '\\'+ str(line_num) +'\\'  # 目录地址
    try:
        lists = os.listdir(test_report)
    except:
        file_path_doc = 'None'
        file_name = 'None'
    else:
        file_lists = []
        for list in lists:
            if '~$' not in list:
                if '.doc' in list:
                    file_lists.append(list)
        file_lists.sort(key=lambda fn:os.path.getmtime(test_report + "\\" + fn)) #按时间排序
        file_name = file_lists[-1]
    return file_name