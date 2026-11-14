# xpad-beitong-dkms

为现有北通 KP 系列 GIP 初始化补丁提供可复现的纯源码 DKMS 打包。补丁源自 Zixing Liu；本次修复不代表新增硬件支持已经验证。

源码固定为官方 Linux v6.18 的 `xpad.c`（commit `7d0a66e4bb9081d75c82ec4957c50034cb0ea449`），以原样副本随仓库保存。PKGBUILD 的每项输入均有 SHA-256 校验。每次 `prepare()` 从干净副本应用本仓库补丁，不下载、不从本机 headers 搜索源码。详见 [SOURCES.md](SOURCES.md)。

使用 `makepkg` 构建包。需要 DKMS，以及每个目标内核匹配的 headers 和编译器；Clang 内核另需 LLVM、LLD。归档仅含 `/usr/src/xpad-beitong-1.1/` 下的 `xpad.c`、`Makefile`、`Kbuild`、`dkms.conf`，不含预编译 `.ko`、自定义安装脚本或 modprobe 配置。Arch 的 DKMS pacman hooks 负责安装事务中的登记、编译、安装、移除；本包不主动装载、卸载或重载当前驱动，错误不会被脚本隐藏。确认 DKMS 输出后，在适当时机重启以启用已安装的模块。

Makefile 按目标 `KDIR/.config` 选择工具链：Clang 配置使用 `LLVM=1`，GCC 配置使用 GCC，配置无法识别则明确失败。独立 `Kbuild` 避免 DKMS 的 `KERNELRELEASE` 参数绕过包装逻辑。手动构建可指定 `KDIR` 或 `KVER`；DKMS 传入自己的目标路径与版本。显式 `LLVM=...`、命令行 `CC=...` 会保留；`XPAD_LLVM=...` 可覆盖部分 DKMS 自动追加的 LLVM 参数，空值表示 GCC。覆盖参数不保证与目标内核兼容。

本次实际驱动分别在 `7.3.3-1-cachyos`（Clang 23.1.4、ThinLTO）和 `6.18.60-2-cachyos-lts`（GCC 16.2.1）的 x86_64 headers 上编译。固定源码不保证兼容任意内核、配置或架构，也可能缺少新版本内核驱动中的修复和设备；扩展支持前需审阅并重测。离线检查：`python tests/test_package.py`。完整结果见 [VALIDATION.md](VALIDATION.md)。

保留原补丁的设备 ID 与 GIP 行为。本次未连接或操作手柄，也未安装/装载模块。原项目曾报告 KP40A 可用；不能据此宣称所有列出的设备均验证过。

[Issue #2](https://github.com/675076143/xpad-beitong-dkms/issues/2) 的 KP70C1 Mint 报告显示空闲接收器为 `20dd:518b`、手柄连接后为 `20bc:518b`，且手动加 ID 后仍不可用。因此本次不新增未经验证的设备 quirk，不把空闲接收器当作 XInput。后续需要活动状态接口描述符、内核/驱动日志和经授权的硬件测试，以区分 GIP 初始化与 XUSB 描述符方案。

[Issue #1](https://github.com/675076143/xpad-beitong-dkms/issues/1) 的外部 fork 仅按文本审阅，未导入其新版 XUSB/HID 行为。PR #3/#4 仅作为问题报告，本次未执行其 recipe。没有修改原 AUR 工作树、已安装驱动或系统配置，没有发布。
