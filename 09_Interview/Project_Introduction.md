# Project Introduction

Do not claim measured performance until evidence exists.

## 30-Second Version

Template: problem context → safe low-voltage scope → personal responsibility → current verified stage (`project initialized; hardware Not Tested`) → next validation.

## 2-Minute Version

Template: application and safety boundary → V0/V1/V2 plan → sensing/control/communication architecture → engineering records and phase gates → verified results/TBD → next step.

## 5-Minute Technical Version

Template: signal chain → ADC error budget → PWM/filter and dummy-load characterization → staged P/PI approach → diagnostics/RS485 roadmap → test traceability → lessons supported by evidence.

## MVP版本项目描述

### 可编辑模板

我为了快速理解工业恒电位控制方向，使用 STM32F103 搭建了一个最小闭环控制系统，完成 ADC 采样、PWM 输出、PI 控制、串口通信和上位机实时曲线，用 RC 网络模拟被控对象，验证了设定值跟踪和扰动恢复。

### 当前证据约束

上述表述是 MVP 完成后的目标版本，当前不能直接作为已完成成果使用。按真实进度替换：

- ADC 采样：TBD / Not Tested
- PWM 输出：TBD / Not Tested
- PWM + RC 模拟量：TBD / Not Tested
- Dummy Load：TBD / Not Tested
- P 控制：TBD / Not Tested
- PI 控制：TBD / Not Tested
- 串口数据上传：TBD / Not Tested
- PC/Python 实时曲线：TBD / Not Tested
- 设定值跟踪：TBD after actual testing
- 扰动恢复：TBD after actual testing

只有测试记录、原始数据、波形、硬件版本和固件 commit 能共同支持时，才将对应 `TBD` 改为实际结果。
