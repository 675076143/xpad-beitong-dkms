# Maintainer: 675076143 <675076143@qq.com>
pkgname=xpad-beitong-dkms
pkgver=1.2
pkgrel=1
pkgdesc='Source-only Beitong xpad DKMS candidate for two reviewed CachyOS releases'
arch=('any')
url='https://github.com/675076143/xpad-beitong-dkms'
license=('GPL-2.0-or-later')
depends=('dkms')
makedepends=('patch')
optdepends=('clang: for Clang-built target kernels'
            'llvm: for Clang-built target kernels'
            'lld: for Clang-built target kernels')
# Exact official stable snapshots; byte-identical to matching CachyOS tags.
# See SOURCES.md. All inputs are local: no network in package or DKMS builds.
source=('xpad-linux-7.3.3.c'
        'xpad-linux-6.18.60.c'
        'beitong-linux-7.3.3.patch'
        'beitong-linux-6.18.60.patch'
        'Makefile'
        'Kbuild'
        'dkms.conf')
sha256sums=(
  'b47281151829fc382c4bcb5f466865f476a6f4ebfacd617ee49393f99c1e3950'
  'a82cdcd930f7e9528ca645d68ade181531d2ac4de1e3e8395e7935945a3bb92e'
  '985def323765e0839a64a3ac7251c2cc2362bee3566522fe57b5f3bd8ed4b260'
  '89066afcc16dfed2d03b9b9e36b449eeb72ec17c8abfe5d72f15b6f1440bb870'
  'dd2c3045f6716a51c188fe7f72c2c600dbf8a2f2638fbf083bfe1f7096240443'
  '03181e10ba96fe4da2946fde4f1246e0fe8b24caa7e4955a18a7b230cb6ab720'
  'a1d56e24d827b3b4ee4ee9f355a56743718fb1c4b2c382978dbedc0f0fe22272'
)

prepare() {
  rm -rf -- "${srcdir}/module"
  mkdir -p -- "${srcdir}/module/sources"
  local version
  for version in 7.3.3 6.18.60; do
    mkdir -- "${srcdir}/module/work-${version}"
    cp -- "${srcdir}/xpad-linux-${version}.c" "${srcdir}/module/work-${version}/xpad.c"
    (
      cd "${srcdir}/module/work-${version}"
      patch --batch --fuzz=0 -Np0 -i "${srcdir}/beitong-linux-${version}.patch"
    )
    mv -- "${srcdir}/module/work-${version}/xpad.c" "${srcdir}/module/sources/xpad-linux-${version}.c"
    rmdir -- "${srcdir}/module/work-${version}"
  done
}

# DKMS selects the matching local source and compiler for each allowed target.
package() {
  local dst="${pkgdir}/usr/src/xpad-beitong-${pkgver}"
  install -Dm644 "${srcdir}/module/sources/xpad-linux-7.3.3.c" "${dst}/sources/xpad-linux-7.3.3.c"
  install -m644 "${srcdir}/module/sources/xpad-linux-6.18.60.c" "${dst}/sources/"
  install -m644 "${srcdir}/Makefile" "${srcdir}/Kbuild" "${dst}/"
  sed "s/@PKGVER@/${pkgver}/g" "${srcdir}/dkms.conf" > "${dst}/dkms.conf"
  chmod 644 "${dst}/dkms.conf"
}
