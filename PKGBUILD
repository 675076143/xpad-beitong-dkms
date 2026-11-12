# Maintainer: 675076143 <675076143@qq.com>
#
# Patch by Zixing Liu that adds FLAG_FORCE_INIT to xpad.c, sending GIP
# (Game Input Protocol) initialization packets (ACK + ANNOUNCE) to Beitong
# KP-series 2.4G gamepads during probing, fixing the firmware's
# OS-detection-based disconnect loop.

pkgname=xpad-beitong-dkms
pkgver=1.0
pkgrel=1
pkgdesc='DKMS module for patched xpad with Beitong KP-series 2.4G gamepad fix'
arch=('any')
url='https://github.com/675076143/xpad-beitong-dkms'
license=('GPL2')
depends=('dkms')
install="${pkgname}.install"
makedepends=('curl')
source=(
  'beitong-gip-init.patch'
  'Makefile'
  'dkms.conf'
)
sha256sums=('SKIP' 'SKIP' 'SKIP')

prepare() {
  cd "${srcdir}"

  # 提取当前运行内核的主版本号（如 6.8 或 7.2）
  # uname -r 输出类似 7.2.11-zen1-1-zen，cut 提取出 7.2.11
  local kernel_ver=$(uname -r | cut -d- -f1)
  
  if [[ ! -f xpad.c ]]; then
    msg2 "Downloading xpad.c for kernel ${kernel_ver}..."
    
    # 从 kernel.org 稳定版分支下载对应版本的源码
    curl -sL -o xpad.c "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/drivers/input/joystick/xpad.c?h=v${kernel_ver}"
    
    # 如果下载失败（比如没有该小版本号的 tag），回退到主版本号（如 v6.8）
    if [[ ! -s xpad.c ]] || grep -q "<html" xpad.c; then
      local major_ver=$(echo "$kernel_ver" | cut -d. -f1,2)
      msg2 "Exact version not found, trying major version v${major_ver}..."
      curl -sL -o xpad.c "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/drivers/input/joystick/xpad.c?h=v${major_ver}"
    fi
  fi

  # 兜底逻辑：如果网络下载全失败，按原作者的逻辑在系统头文件目录找找看
  if [[ ! -s xpad.c ]] || grep -q "<html" xpad.c; then
    msg2 "Download failed, falling back to searching kernel headers..."
    local src
    for d in /usr/lib/modules/*/build/drivers/input/joystick; do
      if [[ -f "${d}/xpad.c" ]]; then
        src="${d}/xpad.c"
        break
      elif [[ -f "${d}/xpad.c.zst" ]]; then
        src="${d}/xpad.c.zst"
        break
      fi
    done

    if [[ -n "${src}" ]]; then
      if [[ "${src}" == *.zst ]]; then
        zstd -d -f "${src}" -o "${srcdir}/xpad.c"
      else
        cp "${src}" "${srcdir}/xpad.c"
      fi
    fi
  fi

  # 如果最终还是没拿到文件，干净地报错退出
  if [[ ! -s xpad.c ]] || grep -q "<html" xpad.c; then
    error "Failed to obtain xpad.c. Network issue or unsupported kernel version."
    exit 1
  fi

  msg2 "Successfully obtained xpad.c ($(wc -l < xpad.c) lines)"
  
  # 应用补丁
  msg2 "Applying patch..."
  patch -Np0 -i beitong-gip-init.patch
}

build() {
  cd "${srcdir}"

  local running_kernel="$(uname -r)"
  local kdir="/usr/lib/modules/${running_kernel}/build"

  if [[ ! -d "${kdir}" ]]; then
    warning "Kernel build dir not found for ${running_kernel}. DKMS will build at install time."
    return 0
  fi

  msg2 "Building for kernel ${running_kernel}..."
  make -C "${kdir}" M="${srcdir}" LLVM=1 modules
}

package() {
  cd "${srcdir}"
  local dkms_dst="${pkgdir}/usr/src/xpad-beitong-${pkgver}"

  install -Dm644 xpad.c               "${dkms_dst}/xpad.c"
  install -Dm644 beitong-gip-init.patch "${dkms_dst}/beitong-gip-init.patch"
  install -Dm644 Makefile             "${dkms_dst}/Makefile"

  sed "s/@PKGVER@/${pkgver}/g" "${srcdir}/dkms.conf" > "${dkms_dst}/dkms.conf"
  chmod 644 "${dkms_dst}/dkms.conf"

  local running_kernel="$(uname -r)"
  if [[ -f xpad.ko ]]; then
    install -Dm644 xpad.ko "${pkgdir}/usr/lib/modules/${running_kernel}/updates/dkms/xpad.ko"
  fi
}
