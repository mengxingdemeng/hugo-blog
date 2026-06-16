import requests
import json
import os
from datetime import datetime, timedelta
import time
import re

# ========== 配置区 ==========
VJUDGE_USERNAME = "liulixian"
DATA_FILE = "static/data/vjudge-record.json"
BASE_URL = f"https://vjudge.net/user/{VJUDGE_USERNAME}"

def get_vjudge_data():
    """抓取 Vjudge 用户数据"""
    # 自动创建data目录
    data_dir = os.path.dirname(DATA_FILE)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"已自动创建目录: {data_dir}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
    }
    
    print(f"正在访问 Vjudge: {BASE_URL}")
    
    try:
        resp = requests.get(BASE_URL, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求失败: {e}")
    
    # 使用正则提取总解题数
    # Vjudge 页面通常包含 "Solved: 数字" 或 "AC: 数字"
    text = resp.text
    
    # 多种匹配模式
    patterns = [
        r'Solved[:：]\s*(\d+)',
        r'AC[:：]\s*(\d+)',
        r'总通过[:：]\s*(\d+)',
        r'<span[^>]*>Solved<\/span>\s*<span[^>]*>(\d+)<\/span>',
        r'<span[^>]*>AC<\/span>\s*<span[^>]*>(\d+)<\/span>',
    ]
    
    total_solved = 0
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            total_solved = int(match.group(1))
            break
    
    # 如果正则匹配失败，尝试从文本中查找
    if total_solved == 0:
        # 寻找包含 "Solved" 或 "AC" 的数字
        lines = text.split('\n')
        for line in lines:
            if 'Solved' in line or 'AC' in line:
                numbers = re.findall(r'\d+', line)
                if numbers:
                    total_solved = int(numbers[0])
                    break
    
    if total_solved == 0:
        raise Exception("未能抓取到总做题数，请检查用户名是否正确或页面结构已变更")
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    print(f"✅ 抓取成功，累计总题量：{total_solved}，今日日期：{today_str}")
    
    return total_solved, today_str

def update_record(total_solved, today_str):
    """更新刷题记录"""
    # 读取历史数据
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"读取历史数据，共 {len(data.get('records', []))} 条记录")
    else:
        # 创建初始数据（向前推30天生成模拟数据）
        print("首次运行，生成初始数据...")
        data = generate_initial_data(total_solved, today_str)
    
    # 判断今日记录是否存在
    exist_today = any(r["date"] == today_str for r in data.get("records", []))
    
    if exist_today:
        # 找到昨天的总量
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
                if idx < len(data["countList"]):
                    data["countList"][idx] = daily_add
                break
        
        print(f"🔄 更新今日记录，当日新增：{daily_add}")
    else:
        # 新增今日记录
        if len(data.get("records", [])) == 0:
            daily_add = total_solved
        else:
            daily_add = total_solved - data["records"][-1]["total"]
        
        # 确保 daily_add 不为负数
        if daily_add < 0:
            daily_add = 0
        
        data.setdefault("dateList", []).append(today_str)
        data.setdefault("countList", []).append(daily_add)
        data.setdefault("records", []).append({
            "date": today_str, 
            "daily": daily_add, 
            "total": total_solved
        })
        
        print(f"➕ 新增今日记录，当日新增：{daily_add}")
    
    # 添加更新时间
    data["updateTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 写入JSON
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 数据已保存至 {DATA_FILE}")
    return data

def generate_initial_data(current_total, today_str):
    """生成初始模拟数据（用于首次运行）"""
    data = {
        "dateList": [],
        "countList": [],
        "records": [],
        "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 从30天前开始生成模拟数据
    start_date = datetime.now() - timedelta(days=30)
    total = current_total
    
    # 生成每天的数据（模拟每天做1-8题）
    current_date = start_date
    while current_date <= datetime.now():
        date_str = current_date.strftime("%Y-%m-%d")
        # 随机生成每天做题数（1-8题），使用hash保证一致性
        daily = (hash(date_str) % 8) + 1
        total += daily
        
        data["dateList"].append(date_str)
        data["countList"].append(daily)
        data["records"].append({
            "date": date_str,
            "daily": daily,
            "total": total
        })
        
        current_date += timedelta(days=1)
    
    print(f"📊 生成初始数据：{len(data['records'])} 条记录")
    return data

def run_task():
    """执行主任务"""
    print("\n" + "="*50)
    print(f"⏰ 开始执行任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    try:
        # 1. 抓取数据
        total_solved, today_str = get_vjudge_data()
        
        # 2. 更新记录
        data = update_record(total_solved, today_str)
        
        # 3. 显示统计信息
        print(f"\n📊 当前统计:")
        print(f"   - 总记录数: {len(data.get('records', []))}")
        print(f"   - 最后更新: {data.get('updateTime', '未知')}")
        
        # 4. Git提交推送（可选）
        try:
            print("\n🔄 开始提交代码到Git...")
            os.system("git add .")
            commit_msg = f'auto update vjudge record {datetime.now().strftime("%Y-%m-%d")}'
            os.system(f'git commit -m "{commit_msg}"')
            os.system("git push origin main")
            print("✅ Git提交完成！")
        except Exception as e:
            print(f"⚠️ Git提交失败（可忽略）: {e}")
        
        print("\n✅ 全部任务执行完成！")
        
    except Exception as e:
        print(f"\n❌ 执行失败：{str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("="*50)
    print("🚀 Vjudge刷题统计脚本 v2.0")
    print("="*50)
    print(f"👤 用户名: {VJUDGE_USERNAME}")
    print(f"📁 数据文件: {DATA_FILE}")
    print("="*50)
    
    # 先手动执行一次测试
    run_task()
    
    # 如果需要定时运行，取消注释下面的代码
    # import schedule
    # schedule.every().day.at("01:00").do(run_task)  # 每天凌晨1点执行
    # 
    # print("\n⏰ 已设置定时任务（每天01:00执行）")
    # print("按 Ctrl+C 停止程序\n")
    # 
    # try:
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(60)
    # except KeyboardInterrupt:
    #     print("\n程序已停止")

if __name__ == "__main__":
    main()