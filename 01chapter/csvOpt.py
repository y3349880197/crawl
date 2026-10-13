# with open("csv_data/01.csv", "w", encoding="utf-8") as f:
#     f.write("姓名,年龄,性别,爱好\n")
#     f.write("小王,18,男,football\n")
#     f.write("小李,18,男,python\n")
#     f.write("小张,18,男,basketball\n")
#     f.write("小丽,18,女,books\n")

import csv

with open("csv_data/02.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["姓名","年龄","性别","爱好"])
    writer.writeheader()
    writer.writerow({"姓名":"小王", "年龄":18, "性别":"男", "爱好":"football"})
    writer.writerow({"姓名": "小李", "年龄": 18, "性别": "男", "爱好": "python"})
    writer.writerows([{"姓名": "小雨", "年龄": 21, "性别": "女", "爱好": "books"},
                     {"姓名": "小丽", "年龄": 17, "性别": "女", "爱好": "study"}])


with open("csv_data/02.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)