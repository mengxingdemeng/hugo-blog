---
title: "Vjudge 刷题记录"
date: 2026-06-16
draft: false
layout: single
---
<span style="font-size: 30px; color: #00ccff;
            text-shadow: 0 0 5px #00ccff, 0 0 10px #66ffff;">
  Vjudge刷题统计看板
</span>

<div id="vjudge-chart" style="width:100%;height:450px;margin:2rem 0;border:1px solid #555;border-radius:6px;"></div>

<h2>每日刷题明细</h2>
<div class="table-responsive mt-3">
  <table class="table table-dark table-striped">
    <thead>
      <tr>
        <th>日期</th>
        <th>当日做题数</th>
        <th>累计总题数</th>
      </tr>
    </thead>
    <tbody id="record-table"></tbody>
  </table>
</div>

<script src="https://cdn.bootcdn.net/ajax/libs/echarts/5.4.3/echarts.min.js"></script>
<script>
// 修正1: 正确的数据路径 - JSON文件需要放在 static/data/ 目录下
const dataUrl = {{ "/data/vjudge-record.json" | relURL | jsonify }};

document.addEventListener('DOMContentLoaded', function() {
  // 修正2: 使用更可靠的容器选择器
  const wrap = document.querySelector(".main-content") || document.querySelector("article") || document.body;
  
  // 显示加载提示
  const loadingDiv = document.createElement('div');
  loadingDiv.id = 'loading-msg';
  loadingDiv.className = 'alert alert-info mt-3';
  loadingDiv.textContent = '正在读取刷题数据...';
  wrap.insertBefore(loadingDiv, wrap.firstChild);

  fetch(dataUrl)
  .then(function(res) {
    if (!res.ok) {
      throw new Error("无法加载数据文件，请确保 static/data/vjudge-record.json 存在");
    }
    return res.json();
  })
  .then(function(data) {
    // 移除加载提示
    const loadingMsg = document.getElementById('loading-msg');
    if (loadingMsg) loadingMsg.remove();

    // 验证数据完整性
    if (!data.dateList || !data.countList || !data.records) {
      throw new Error("数据格式不正确，缺少必要字段: dateList, countList, records");
    }

    if (data.dateList.length === 0) {
      throw new Error("数据为空，请先运行Python脚本抓取刷题数据");
    }

    // 初始化图表
    const chartDom = document.getElementById('vjudge-chart');
    if (!chartDom) {
      throw new Error("找不到图表容器 #vjudge-chart");
    }

    const chartIns = echarts.init(chartDom, 'dark');
    
    // 图表配置
    const chartOpt = {
      title: { 
        text: 'Vjudge 每日刷题趋势', 
        textStyle: { color: '#ccc' } 
      },
      tooltip: { 
        trigger: 'axis',
        formatter: function(params) {
          const date = params[0].name;
          const count = params[0].value;
          // 在记录中查找对应的累计总数
          const record = data.records.find(r => r.date === date);
          const total = record ? record.total : '未知';
          return `${date}<br/>当日刷题: ${count} 题<br/>累计总数: ${total} 题`;
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: { 
        type: 'category', 
        data: data.dateList, 
        axisLine: { lineStyle: { color: '#666' } },
        axisLabel: { 
          color: '#aaa',
          rotate: data.dateList.length > 30 ? 45 : 0  // 日期过多时旋转显示
        }
      },
      yAxis: { 
        type: 'value', 
        name: '当日刷题数量', 
        axisLine: { lineStyle: { color: '#666' } },
        axisLabel: { color: '#aaa' },
        splitLine: { lineStyle: { color: '#333' } }
      },
      series: [{
        name: '当日刷题',
        type: 'line',
        smooth: true,
        data: data.countList,
        lineStyle: { 
          width: 3,
          color: '#42b983'
        },
        itemStyle: { 
          color: '#42b983' 
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(66, 185, 131, 0.3)' },
            { offset: 1, color: 'rgba(66, 185, 131, 0)' }
          ])
        },
        markLine: {
          data: [
            { 
              type: 'average', 
              name: '平均值',
              label: { 
                formatter: '平均: {c} 题',
                color: '#ffd700'
              }
            }
          ],
          lineStyle: { color: '#ffd700', type: 'dashed' }
        }
      }]
    };
    
    chartIns.setOption(chartOpt);
    
    // 窗口大小改变时自适应
    window.addEventListener('resize', function() { 
      chartIns.resize(); 
    });

    // 填充表格数据
    const tableBody = document.getElementById('record-table');
    if (tableBody) {
      // 清空表格（保留表头）
      tableBody.innerHTML = '';
      
      if (data.records.length === 0) {
        const tr = document.createElement('tr');
        tr.innerHTML = '<td colspan="3" style="text-align:center;">暂无数据</td>';
        tableBody.appendChild(tr);
      } else {
        data.records.forEach(function(item) {
          const tr = document.createElement('tr');
          tr.innerHTML = '<td>' + item.date + '</td><td>' + item.daily + '</td><td>' + item.total + '</td>';
          tableBody.appendChild(tr);
        });
      }
    }
  })
  .catch(function(err) {
    // 错误处理
    const loadingMsg = document.getElementById('loading-msg');
    if (loadingMsg) {
      loadingMsg.className = 'alert alert-danger mt-3';
      loadingMsg.textContent = '❌ 数据加载失败：' + err.message;
    } else {
      const errorDiv = document.createElement('div');
      errorDiv.className = 'alert alert-danger mt-3';
      errorDiv.innerHTML = '<strong>❌ 数据加载失败</strong><br/>' + err.message;
      wrap.insertBefore(errorDiv, wrap.firstChild);
    }
    console.error('详细错误信息:', err);
    
    // 在图表区域显示错误提示
    const chartDom = document.getElementById('vjudge-chart');
    if (chartDom) {
      chartDom.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#ff6b6b;font-size:18px;">⚠️ 图表数据加载失败，请检查控制台错误信息</div>';
    }
  });
});
</script>

<!-- 添加样式美化表格和错误提示 -->
<style>
#vjudge-chart {
  background: #1a1a1a;
  min-height: 450px;
}
.table-dark {
  background-color: #1a1a1a;
}
.table-dark th {
  border-bottom: 2px solid #42b983;
  color: #42b983;
}
.table-dark td {
  border-color: #333;
  color: #ddd;
}
.alert {
  padding: 15px 20px;
  border-radius: 6px;
  margin: 15px 0;
}
.alert-info {
  background-color: #1a3a4a;
  color: #7fc9ff;
  border: 1px solid #2a5a6a;
}
.alert-danger {
  background-color: #4a1a1a;
  color: #ff7f7f;
  border: 1px solid #6a2a2a;
}
</style>