# xpad-beitong-dkms

为北通 KP 系列 2.4G 手柄修复断连问题的 DKMS 内核模块。

## 问题

北通 KP 系列手柄（KP20A、KP40A、KP50B 等）在 Linux 上使用 2.4G 无线接收器时，每 ~1 秒断连一次。固件会检测主机操作系统类型，如果在初始化阶段未收到 Xbox One GIP（Game Input Protocol）协议包，则主动断开 USB 重连。

**症状：** USB 设备 `20bc:5127` 持续断连重连；蓝牙和 USB 有线模式正常工作。

## 修复

应用 [Zixing Liu 的补丁](https://lore.kernel.org/linux-input/20260102030154.197749-2-liushuyu@aosc.io) 到 `xpad.c`，添加 `FLAG_FORCE_INIT` 标志，在手柄探测阶段发送 GIP 确认和声明包。固件收到这些包后确认主机为 Windows/Xbox 驱动，从而稳定工作在 XINPUT 模式。

## 安装

### 从 AUR

```bash
yay -S xpad-beitong-dkms
# 或
paru -S xpad-beitong-dkms
```

### 从源码

```bash
git clone https://github.com/675076143/xpad-beitong-dkms.git
cd xpad-beitong-dkms
makepkg -si
```

安装完成后，重启或执行：

```bash
sudo modprobe -r xpad && sudo modprobe xpad
```

## 依赖

- `dkms` 包
- 当前内核对应的 headers 包（如 `linux-headers`、`linux-zen-headers`、`linux-cachyos-rc-headers` 等）

## 工作原理

1. 从当前内核 headers 复制 `xpad.c`
2. 应用 GIP 初始化补丁
3. 注册 DKMS，内核更新后自动重编
4. 添加 modprobe 黑名单屏蔽内核自带的 `xpad` 模块

## 兼容设备

以下 VID:PID 组合受支持：

| VID | PID | 设备 |
|-----|-----|------|
| 20bc | 5125-5128 | KP20A/KP40A |
| 20bc | 512f-5130 | KP70A |
| 20bc | 5133-5134 | KP50B |
| 20bc | 5145-5146 | KP40A/KP40B |
| 20bc | 5149-514a | KP50C |
| 20bc | 5150-5151 | KP50D |
| 20bc | 5152-5153 | KP50E |
| 20bc | 5154-5155 | KP40D |
| 20bc | 5158-5159 | KP20D |
| 20bc | 515b-515c | KP40D（白色） |
| 20bc | 515d-515e | KP40F（白色） |
| 20bc | 515f-5160 | KP70A |
| 20bc | 5169-516a | KP40F（黑色） |

**临时性** DKMS 包，补丁合入主线后弃用（预计 Linux 7.3+）。

## 上游状态

| 项目 | 状态 |
|------|------|
| 补丁作者 | Zixing Liu |
| 已提交 | v3，2026-07-17 |
| 目标 | Linux 主线（预计 7.3 或后续） |
| 本包 | 合入后弃用 |

## 链接

- [完整排查记录（Wiki）](https://github.com/675076143/notes/wiki/beitong-btp-kp40a-linux-usb-disconnect)
- [上游补丁讨论 (linux-input)](https://lore.kernel.org/linux-input/20260102030154.197749-2-liushuyu@aosc.io/)
- [Arch Wiki - Gamepad（ShanWan 章节）](https://wiki.archlinux.org/title/Gamepad)
