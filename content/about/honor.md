---
title: "荣誉墙"
date: 2026-06-16
draft: false
layout: single
parent: "关于我"
---
{{< raw >}}
<style>
.honor-wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}
.back-home-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #222833;
  border: 1px solid #36bffd30;
  border-radius: 10px;
  color: #99d8f7;
  text-decoration: none;
  transition: all 0.3s ease;
  margin-bottom: 40px;
}
.back-home-btn:hover {
  border-color: #36bffd80;
  background: #262d3a;
  transform: translateX(-4px);
  box-shadow: 0 0 12px #36bffd40;
}
.page-main-title {
  text-align: center;
  font-size: 40px;
  margin: 0 0 50px;
  background: linear-gradient(90deg, #ffd700, #ff7c28, #ffd700);
  background-size: 200% auto;
  -webkit-background-clip: text;
  color: transparent;
  animation: title-flow 4s linear infinite;
}
/* 标题流光动画 */
@keyframes title-flow {
  0% { background-position: 0% center; }
  100% { background-position: 200% center; }
}
/* 证书画廊网格 */
.cert-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 28px;
}
/* 证书卡片容器 */
.cert-item {
  background: linear-gradient(145deg, #1e242d, #161a20);
  border: 1px solid #ffd70025;
  border-radius: 18px;
  padding: 18px;
  transition: all 0.4s cubic-bezier(0.2, 0, 0.2, 1);
  overflow: hidden;
}
.cert-item:hover {
  transform: translateY(-12px) scale(1.02);
  border-color: #ffd70090;
  box-shadow: 0 18px 60px rgba(255, 215, 0, 0.22);
}
/* 图片容器：自适应不裁切，完整展示证书 */
.cert-img-box {
  width: 100%;
  max-height: 220px;
  border-radius: 12px;
  overflow: hidden;
  cursor: zoom-in;
}
.cert-img {
  width: 100%;
  height: auto;
  display: block;
  transition: all 0.5s ease;
  background: #2a323f;
  font-size: 0;
}
/* 图片加载失败占位文字 */
.cert-img::after {
  content: "证书图片待上传";
  width: 100%;
  min-height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #88ccf8;
}
.cert-item:hover .cert-img {
  transform: scale(1.06);
  filter: brightness(1.08);
}
/* 文字区域间距优化 */
.cert-name {
  margin: 14px 0 6px;
  font-size: 17px;
  color: #f0f0f0;
  text-align: center;
  line-height: 1.4;
}
.cert-time {
  font-size: 14px;
  color: #ffd700;
  text-align: center;
  letter-spacing: 1px;
}
.split-line {
  height: 2px;
  background: linear-gradient(90deg, transparent, #ffd70035, transparent);
  margin: 60px 0;
}
.footer-tip {
  text-align:center;
  color:#888;
  font-size:15px;
}
/* 图片放大灯箱弹窗样式 */
.lightbox-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.92);
  z-index: 9999;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 40px;
  box-sizing: border-box;
  opacity: 0;
  transition: opacity 0.35s ease;
}
.lightbox-mask.show {
  display: flex;
  opacity: 1;
}
.lightbox-img {
  max-width: 92%;
  max-height: 92vh;
  border-radius: 8px;
  transform: scale(0.9);
  transition: transform 0.35s ease;
}
.lightbox-mask.show .lightbox-img {
  transform: scale(1);
}
.lightbox-close {
  position: absolute;
  top: 24px;
  right: 32px;
  color: #fff;
  font-size: 42px;
  cursor: pointer;
  user-select: none;
  transition: color 0.2s;
}
.lightbox-close:hover {
  color: #ffd700;
}
</style>

<div class="honor-wrap">
<a href="/hugo-blog/about-me" class="back-home-btn">
  ← 返回关于我
</a>

<h1 class="page-main-title">🏆 竞赛荣誉 & 获奖证书</h1>

<!-- 证书画廊外层容器（你原代码缺失，已补上） -->
<div class="cert-gallery">
  <!-- 示例证书 -->
  <div class="cert-item">
    <div class="cert-img-box">
      <img src="/hugo-blog/images/cert/2026年码蹄杯省赛学生证书.jpg" alt="码蹄杯省级金奖证书" class="cert-img">
    </div>
    <h4 class="cert-name">码蹄杯程序设计大赛 省级金奖</h4>
    <div class="cert-time">2026 · 05</div>
  </div>

  <!-- 新增证书模板，直接复制整块使用
  <div class="cert-item">
    <div class="cert-img-box">
      <img src="/hugo-blog/images/cert/图片文件名.jpg" alt="证书描述" class="cert-img">
    </div>
    <h4 class="cert-name">证书名称</h4>
    <div class="cert-time">获奖时间</div>
  </div>
  -->
</div>

<div class="split-line"></div>

<div class="footer-tip">
  持续备战 ICPC / 蓝桥杯国赛，长期坚持OJ刷题积累
</div>
</div>

<!-- 图片全屏放大弹窗 -->
<div class="lightbox-mask" id="lightbox">
  <span class="lightbox-close" id="closeBtn">×</span>
  <img class="lightbox-img" id="lightImg" src="" alt="证书高清大图">
</div>
<script>
// 获取所有元素
const imgList = document.querySelectorAll('.cert-img');
const lightbox = document.getElementById('lightbox');
const lightImg = document.getElementById('lightImg');
const closeBtn = document.getElementById('closeBtn');

// 点击图片打开弹窗
imgList.forEach(img => {
  img.addEventListener('click', () => {
    lightImg.src = img.src;
    lightbox.classList.add('show');
    document.body.style.overflow = 'hidden';
  })
})

// 关闭弹窗函数
function closeLightbox() {
  lightbox.classList.remove('show');
  document.body.style.overflow = '';
}
// 点击关闭按钮关闭
closeBtn.addEventListener('click', closeLightbox);
// 点击遮罩空白区域关闭
lightbox.addEventListener('click', (e) => {
  if(e.target === lightbox) closeLightbox();
})
// 键盘ESC一键关闭
document.addEventListener('keydown', (e) => {
  if(e.key === 'Escape') closeLightbox();
})
</script>
{{< /raw >}}