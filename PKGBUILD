# Maintainer: 675076143 <675076143@qq.com>
pkgname=xpad-beitong-dkms
pkgver=1.1
pkgrel=1
pkgdesc='Source-only DKMS xpad module with Beitong KP-series GIP initialization'
arch=('any')
url='https://github.com/675076143/xpad-beitong-dkms'
license=('GPL-2.0-or-later')
depends=('dkms')
makedepends=('patch')
optdepends=('clang: for Clang-built target kernels'
            'llvm: for Clang-built target kernels'
            'lld: for Clang-built target kernels')
# Vendored byte-for-byte from torvalds/linux v6.18 at this immutable commit:
# 7d0a66e4bb9081d75c82ec4957c50034cb0ea449
source=('xpad-linux-6.18.c'
        'beitong-gip-init.patch'
        'Makefile'
        'Kbuild'
        'dkms.conf')
sha256sums=(
  '6f37e6da9c5925b43447ae1a8bc34b7e159cbd8f0411467929ce124b17ca6311'
  'c5e503c3c55341673a33e964585e41b9edd3669e40cc64057915fe7d52968042'
  '0801cbf8aff8bdc299e48d3508af7d28398385b44e930b77d83265ba7e08c09b'
  '03181e10ba96fe4da2946fde4f1246e0fe8b24caa7e4955a18a7b230cb6ab720'
  '0065699eb197974743ac678f81dbccf505792c3f3c070acb8a28ab2e3e6c78a9'
)

prepare() {
  # Recreate our working directory whenever prepare() runs again.
  rm -rf -- "${srcdir}/module"
  mkdir -- "${srcdir}/module"
  cp -- "${srcdir}/xpad-linux-6.18.c" "${srcdir}/module/xpad.c"
  cp -- "${srcdir}/Makefile" "${srcdir}/Kbuild" "${srcdir}/module/"
  cd "${srcdir}/module"
  patch --batch --fuzz=0 -Np0 -i "${srcdir}/beitong-gip-init.patch"
}

# No build(): the package contains no host-kernel .ko. DKMS builds for targets.
package() {
  local dst="${pkgdir}/usr/src/xpad-beitong-${pkgver}"
  install -Dm644 "${srcdir}/module/xpad.c" "${dst}/xpad.c"
  install -m644 "${srcdir}/module/Makefile" "${srcdir}/module/Kbuild" "${dst}/"
  sed "s/@PKGVER@/${pkgver}/g" "${srcdir}/dkms.conf" > "${dst}/dkms.conf"
  chmod 644 "${dst}/dkms.conf"
}
