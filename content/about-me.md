---
title: "关于我"
date: 2026-06-16
draft: false
layout: single
type: page
---
{{< raw >}}
<style>
.about-wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}
.about-header {
  display: flex;
  gap: 32px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
  padding: 40px 20px;
  background: linear-gradient(145deg, #1c2028, #12151b);
  border-radius: 20px;
  margin-bottom: 40px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
.avatar-box {
  position: relative;
  width: 160px;
  height: 160px;
}
.avatar-glow {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #36bffd44;
  animation: rotateGlow 8s linear infinite;
}
.avatar-glow img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
@keyframes rotateGlow {
  0% { box-shadow: 0 0 15px #36bffd77; }
  50% { box-shadow: 0 0 30px #2fd09088; }
  100% { box-shadow: 0 0 15px #36bffd77; }
}
.info-text {
  flex: 1;
  min-width: 300px;
}
.info-text h1 {
  font-size: 36px;
  margin: 0;
  background: linear-gradient(90deg, #36bffd, #2fd090);
  -webkit-background-clip: text;
  color: transparent;
}
.info-sub {
  color: #aaa;
  font-size: 16px;
  margin: 8px 0 16px;
}
.info-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 16px 0;
}
.tag {
  padding: 6px 14px;
  background: #252b36;
  border-radius: 99px;
  font-size: 14px;
  color: #99d8f7;
  border: 1px solid #36bffd33;
}
.desc-box {
  line-height: 1.8;
  color: #ccc;
  font-size: 16px;
}
.split-line {
  height: 2px;
  background: linear-gradient(90deg, transparent, #36bffd44, transparent);
  margin: 45px 0;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}
.func-card {
  background: linear-gradient(145deg, #1e232c, #171a20);
  padding: 28px;
  border-radius: 16px;
  border: 1px solid #36bffd22;
  transition: all 0.3s ease;
  cursor: pointer;
}
.func-card:hover {
  transform: translateY(-8px);
  border-color: #36bffd77;
  box-shadow: 0 12px 40px rgba(54, 191, 253, 0.15);
}
.func-card h3 {
  font-size: 22px;
  margin: 0 0 10px;
  color: #eee;
}
.func-card p {
  color: #aaa;
  margin:0;
  line-height:1.7;
}
</style>

<div class="about-wrap">
  <div class="about-header">
    <div class="avatar-box">
      <div class="avatar-glow">
        <!-- 修正图片路径 static/images/avatar.png -->
        <img src="/hugo-blog/images/avatar.png" alt="个人头像">
      </div>
    </div>
    <div class="info-text">
      <h1>liulixian</h1>
      <div class="info-sub">xbmu | 19 years old</div>
      <div class="info-tags">
        <span class="tag">C/C++</span>
        <span class="tag">算法竞赛</span>
        <span class="tag">Hugo博客</span>
        <span class="tag">Web前端</span>
        <span class="tag">Linux</span>
      </div>
      <div class="desc-box">
        热爱算法与程序设计，常年泡OJ刷题，专注ICPC/蓝桥杯竞赛；
        喜欢折腾博客、服务器、前端美化。平时记录刷题笔记、竞赛总结与学习心得。
        持续刷题提升代码能力，不断沉淀技术与竞赛荣誉。
      </div>
    </div>
  </div>
  <div class="split-line"></div>
  <h2 style="text-align:center;font-size:28px;color:#ddd;margin-bottom:30px;">个人栏目导航</h2>
  <div class="card-grid">
    <a href="/hugo-blog/about/honor/" class="func-card" style="text-decoration:none;">
      <h3>🏆 荣誉墙</h3>
      <p>竞赛获奖、省赛金奖、各类证书汇总，记录所有竞赛成果</p>
    </a>
    <a href="#" class="func-card" style="text-decoration:none;">
      <h3>💻 技能栈</h3>
      <p>编程语言、工具、框架、竞赛训练方向完整清单</p>
    </a>
    <a href="https://vjudge.net/user/liulixian" target="_blank" class="func-card" style="text-decoration:none;">
      <h3>📚 Vjudge刷题主页</h3>
      <p>跳转Vjudge个人主页，查看实时做题数据与热力日历</p>
    </a>
    <a href="/hugo-blog/posts/" class="func-card" style="text-decoration:none;">
      <h3>📝 全部学习笔记</h3>
      <p>C++算法、编程题解、课堂学习记录与心得总结</p>
    </a>
  </div>
</div>
{{< /raw >}}