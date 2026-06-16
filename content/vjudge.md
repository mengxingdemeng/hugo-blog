---
title: "Vjudge 刷题记录"
date: 2026-06-16
draft: false
layout: single
---
{{< raw >}}
<span style="font-size: 30px; color: #00ccff; text-shadow: 0 0 5px #00ccff, 0 0 10px #66ffff;">
  Vjudge刷题统计看板
</span>

<div id="vjudge-chart" style="width:100%;height:450px;margin:2rem 0;border:1px solid #555;border-radius:6px;background:#1a1a1a;display:flex;align-items:center;justify-content:center;color:#888;">
  <span>⏳ 加载数据中...</span>
</div>

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
    <tbody id="record-table">
      <tr><td colspan="3" style="text-align:center;color:#888;">加载中...</td></tr>
    </tbody>
  </table>
</div>

<script src="https://cdn.bootcdn.net/ajax/libs/echarts/5.4.3/echarts.min.js"></script>
<script>
(function() {
  'use strict';
  console.log('🚀 Vjudge 图表脚本加载');

  // 固定写死静态JSON地址，无任何Hugo模板插值，彻底规避语法报错
  const JSON_FILE_PATH = "/hugo-blog/data/vjudge-record.json";

  // 统一数据加载入口
  function loadData() {
    // 前置校验DOM容器存在
    const chartBox = document.getElementById("vjudge-chart");
    const tableBox = document.getElementById("record-table");
    if (!chartBox || !tableBox) {
      console.warn("页面DOM容器未加载完成，延迟重试");
      setTimeout(loadData, 300);
      return;
    }

    // 拉取静态JSON
    fetch(JSON_FILE_PATH)
      .then(res => {
        if (!res.ok) throw new Error("文件不存在：static/data/vjudge-record.json");
        return res.json();
      })
      .then(data => {
        renderAll(data);
      })
      .catch(err => {
        chartBox.innerHTML = `<div style="color:#ff6b6b;text-align:center;padding:20px;">
          <div style="font-size:32px;">⚠️</div>
          <div>数据加载失败</div>
          <div style="font-size:12px;color:#888;margin-top:10px;">${err.message}</div>
        </div>`;
        console.error("数据拉取异常：", err);
      });
  }

  // 一次性渲染图表+表格
  function renderAll(data) {
    const chartDom = document.getElementById("vjudge-chart");
    // 防止重复初始化图表
    if (window._chartRendered) return;

    // 等待ECharts加载完成
    if (typeof echarts === "undefined") {
      setTimeout(() => renderAll(data), 400);
      return;
    }

    // 渲染折线图
    chartDom.innerHTML = "";
    const chart = echarts.init(chartDom, "dark");
    const option = {
      title: { text: "Vjudge 每日刷题趋势", textStyle: { color: "#ccc" } },
      tooltip: {
        trigger: "axis",
        formatter: params => {
          const idx = params[0].dataIndex;
          const date = data.dateList[idx] || "未知";
          const dayCount = params[0].value || 0;
          const totalCount = data.records[idx]?.total || 0;
          return `<strong>${date}</strong><br/>当日：${dayCount} 题<br/>累计：${totalCount} 题`;
        }
      },
      grid: { left: "3%", right: "4%", bottom: "3%", containLabel: true },
      xAxis: {
        type: "category",
        data: data.dateList,
        axisLine: { lineStyle: { color: "#666" } },
        axisLabel: { color: "#aaa", rotate: data.dateList.length > 20 ? 45 : 0 }
      },
      yAxis: {
        type: "value",
        name: "当日刷题数量",
        axisLine: { lineStyle: { color: "#666" } },
        axisLabel: { color: "#aaa" },
        splitLine: { lineStyle: { color: "#333" } }
      },
      series: [{
        name: "当日刷题",
        type: "line",
        smooth: true,
        data: data.countList,
        lineStyle: { width: 3, color: "#42b983" },
        itemStyle: { color: "#42b983" },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "rgba(66, 185, 131, 0.3)" },
            { offset: 1, color: "rgba(66, 185, 131, 0)" }
          ])
        },
        markLine: {
          data: [{ type: "average", name: "平均值" }],
          lineStyle: { color: "#ffd700", type: "dashed" },
          label: { formatter: "平均: {c} 题", color: "#ffd700" }
        }
      }]
    };
    chart.setOption(option);
    window.addEventListener("resize", () => chart.resize());

    // 渲染表格（倒序，最新日期在前）
    const tableBody = document.getElementById("record-table");
    tableBody.innerHTML = "";
    const reverseData = [...data.records].reverse();
    reverseData.forEach(item => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${item.date}</td><td>${item.daily}</td><td>${item.total}</td>`;
      tableBody.appendChild(tr);
    });

    window._chartRendered = true;
    console.log("🎉 图表&表格渲染完成");
  }

  // 多时机触发加载，兼容PJAX/普通刷新
  function initTrigger() {
    setTimeout(loadData, 200);
  }
  document.addEventListener("DOMContentLoaded", initTrigger);
  document.addEventListener("pjax:complete", initTrigger);
  window.addEventListener("load", initTrigger);
  // 页面已加载完成直接执行
  if (document.readyState === "complete" || document.readyState === "interactive") {
    initTrigger();
  }
})();
</script>

<style>
#vjudge-chart {
  background: #1a1a1a;
  min-height: 450px;
  border-radius: 6px;
  transition: border-color 0.3s;
}
#vjudge-chart:hover {
  border-color: #42b983;
}
.table-dark {
  background-color: #1a1a1a;
  border-radius: 6px;
  overflow: hidden;
}
.table-dark th {
  border-bottom: 2px solid #42b983;
  color: #42b983;
  background-color: #0d0d0d;
}
.table-dark td {
  border-color: #333;
  color: #ddd;
}
.table-dark tr:hover td {
  background-color: #2a2a2a;
}
</style>
{{< /raw >}}