# Cathodic Protection Control Loop MVP — 7 Day Plan

## Objective

在 3～7 天内完成一个可测试、可解释、可复现的最小闭环系统，用于判断工业恒电位控制方向的适配度，并形成可用于岗位沟通的真实项目证据。

MVP 范围仅包括 STM32F103、ADC、UART、PWM、PWM + RC 模拟量、简单 RC Dummy Load、P/PI 控制、串口数据上传，以及 PC/Python 实时显示。所有结果在完成真实测试前均为 `Not Tested`；未知参数均为 `TBD`。

## Day 1 — UART and ADC

- 跑通 STM32 UART。
- 完成 ADC 基础采样。
- 串口输出 `ADC_RAW`、`VDDA` 和 `VIN`。
- 执行 TEST-001；保存固件 commit、接线、仪器及原始记录。

## Day 2 — PWM

- 输出 PWM。
- 验证频率和 Duty 可调。
- 执行 TEST-004；TEST-005 作为 Duty 细化验证。

## Day 3 — PWM to Analog

- 搭建 PWM + RC 滤波。
- 获得可调模拟电压。
- 执行 TEST-006，记录纹波、建立时间和线性表现。

## Day 4 — Dummy Load and Control

- 搭建简单 RC Dummy Load。
- 表征被控对象基本响应。
- 依次实现并验证 P 控制、PI 控制。
- 执行 TEST-007、TEST-008、TEST-009；未经前序测试不得启用闭环。

## Day 5 — Telemetry and Python Plot

- 定义简洁、可解析的串口数据协议。
- PC/Python 实时显示 `Setpoint`、`Measured`、`Control Output`。
- 保存协议版本、脚本版本和示例原始数据；数据必须来自真实运行。

## Day 6 — Step Response

- 执行设定值序列：`0.8 V → 1.2 V → 1.8 V`。
- 记录稳态误差、超调和响应时间。
- 同时保存原始串口数据、曲线、测试条件、硬件版本和固件 commit。
- 在测试前，安全范围和各项合格阈值为 `TBD`。

## Day 7 — Evidence Package

- 整理系统框图。
- 整理测试数据和波形。
- 更新 Debug Log 和 Issue Log。
- 更新项目介绍和面试材料。
- 只陈述有测试记录支持的结果，其他内容保持 `TBD` 或 `Not Tested`。

## MVP Scope Boundary

以下模块保留原工业完整版规划，但统一延后为 **Post-MVP / Future Work**：RS485、Modbus、Current Sense、Voltage Sense、Reference AFE、PCB、Protection、MOSFET 大功率级、真实工业参比电极及工业高压功率级。

## Immediate Task

唯一第一任务：**TEST-001 ADC Basic Acquisition**。
