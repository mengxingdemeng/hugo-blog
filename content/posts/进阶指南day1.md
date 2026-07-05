---
title: 进阶指南day1
subtitle:
date: 2026-07-05T11:48:13+08:00
slug: db0cd0f
draft: false
author:
  name:
  link:
  email:
  avatar:
description:
keywords:
comment: false
weight: 0
tags:
  - draft
categories:
  - draft
hiddenFromHomePage: false
hiddenFromSearch: false
hiddenFromRelated: false
hiddenFromFeed: false
summary:
featuredImagePreview:
featuredImage:
password:
message:
repost:
  enable: false
  url:

# See details front matter: https://fixit.lruihao.cn/documentation/content-management/introduction/#front-matter
---

<!--more-->

这个夏天，让我开始研习李煜东大神的算法竞赛进阶指南
[![pm0bCwV.png](https://s41.ax1x.com/2026/07/05/pm0bCwV.png)](https://imgchr.com/i/pm0bCwV)

### [洛谷](https://www.luogu.com.cn/training/400)和[vjudge](https://vjudge.net/article/3573)以及[AC Wing](https://www.acwing.com/problem/search/1/?csrfmiddlewaretoken=MKUiDRtg5tVmqfHubk65Mz95UnNlnAyHFAupGr1wFiRjjVATcV4SJMiCGDQlYdZw&show_algorithm_tags=0&search_content=%E7%AE%97%E6%B3%95%E7%AB%9E%E8%B5%9B%E8%BF%9B%E9%98%B6%E6%8C%87%E5%8D%97)都有题单哦

---

$2026.7.5$
# 0x00 基本算法
## memset 函数

### 1. 头文件与原型
```c
#include <string.h>
void *memset(void *ptr, int value, size_t num);
```
#### 参数说明：

1. `ptr`：要填充的内存起始地址（任意类型指针，void* 兼容 char/int/ 结构体 / 数组）
2. `value`：填充的字节值，**仅低 8 位有效**（0~255），int 只是参数类型，实际按 unsigned char 写入内存
3. `num`：填充**字节个数**，不是元素个数！核心易错点
    
    返回值：传入的 ptr 指针本身
### 2. 底层原理
memset 直接操作**原始内存字节**，逐一字节赋值，不区分变量类型、不识别数组元素，只看字节长度。
### 3.标准示例
#### 示例 1：字符数组清零 / 填充字符

```c
char buf[100];
// 全部置 '\0'（清零）
memset(buf, 0, sizeof(buf));
// 全部填充 '#'
memset(buf, '#', sizeof(buf));
```
#### 示例 2：int 数组清零（唯一安全的多类型填充）
```c
int arr[10];
memset(arr, 0, sizeof(arr));
```
内存中每个字节写 0，4 字节 int 整体就是 `0x00000000`，数值为 0。
#### 示例 3：结构体清零（常用初始化）

```c
struct Student {
    char name[20];
    int age;
    float score;
} stu;
// 结构体整块内存清零
memset(&stu, 0, sizeof(stu));
```

#### 示例 4：动态分配内存初始化
```c
int *p = malloc(10 * sizeof(int));
if(p != NULL) {
    memset(p, 0, 10 * sizeof(int));
}
```

## 快速幂



