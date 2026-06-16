import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
import time

# ========== 配置区 ==========
VJUDGE_USERNAME = "liulixian"
DATA_FILE = "static/data/vjudge-record.json"
BASE_URL = f"https://vjudge.net/user/{VJUDGE_USERNAME}"

def get_today_solve():
    # 自动创建data目录
    data_dir = os.path.dirname(DATA_FILE)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"已自动创建目录: {data_dir}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }
    print(f"正在访问Vjudge主页: {BASE_URL}")
    resp = requests.get(BASE_URL, headers=headers, timeout=10)
    resp.raise_for_status() # 捕获404/500网络错误
    soup = BeautifulSoup(resp.text, "html.parser")

    # 匹配总解题数，增强容错
    total_solved = 0
    all_text = soup.get_text()
    for seg in all_text.split():
        if seg.isdigit() and "Solved" in all_text:
            total_solved = int(seg)
            break
    if total_solved == 0:
        raise Exception("未能抓取到总做题数，请检查用户名是否正确")
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    print(f"抓取成功，累计总题量：{total_solved}，今日日期：{today_str}")

    # 读取历史数据
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"dateList": [], "countList": [], "records": []}

    # 判断今日记录
    exist_today = any(r["date"] == today_str for r in data["records"])
    if exist_today:
        # 找到昨天总量
        last_total = 0
        for rec in reversed(data["records"]):
            if rec["date"] != today_str:
                last_total = rec["total"]
                break
        daily_add = total_solved - last_total
        # 更新今日行
        for idx, rec in enumerate(data["records"]):
            if rec["date"] == today_str:
                data["records"][idx]["daily"] = daily_add
                data["records"][idx]["total"] = total_solved
                data["countList"][idx] = daily_add
                break
        print(f"更新今日记录，当日新增：{daily_add}")
    else:
        # 新增今日记录
        if len(data["records"]) == 0:
            daily_add = total_solved
        else:
            daily_add = total_solved - data["records"][-1]["total"]
        data["dateList"].append(today_str)
        data["countList"].append(daily_add)
        data["records"].append({"date": today_str, "daily": daily_add, "total": total_solved})
        print(f"新增今日记录，当日新增：{daily_add}")
    
    # 写入json
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存至 {DATA_FILE}")

def run_task():
    try:
        get_today_solve()
        # Git提交推送
        print("开始提交代码到Gitee...")
        os.system("git add .")
        commit_msg = f'auto update vjudge record {datetime.now().strftime("%Y-%m-%d")}'
        os.system(f'git commit -m "{commit_msg}"')
        os.system("git push origin main")
        print("✅ 全部任务执行完成！")
    except Exception as e:
        print(f"❌ 执行失败：{str(e)}")

if __name__ == "__main__":
    print("===== Vjudge刷题统计脚本启动 =====")
    # 先手动执行一次测试
    run_task()
    # 注释下面两行，先测试，不需要自动定时常驻
    # schedule.every().day.at("01:00").do(run_task)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)