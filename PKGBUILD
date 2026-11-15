# Maintainer: 675076143 <675076143@qq.com>
pkgname=xpad-beitong-dkms
pkgver=1.3
pkgrel=1
pkgdesc='Source-only Beitong xpad DKMS candidate for three reviewed CachyOS releases'
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
        'xpad-linux-7.3.4.c'
        'xpad-linux-6.18.60.c'
        'beitong-linux-7.3.3.patch'
        'beitong-linux-7.3.4.patch'
        'beitong-linux-6.18.60.patch'
        'Makefile'
        'Kbuild'
        'dkms.conf')
sha256sums=(
  'b47281151829fc382c4bcb5f466865f476a6f4ebfacd617ee49393f99c1e3950'
  'd3d9500cac4a59aad0a6bfe1d064e5a4c16cfc18d928f4bf6f69f6fd51511176'
  'a82cdcd930f7e9528ca645d68ade181531d2ac4de1e3e8395e7935945a3bb92e'
  '985def323765e0839a64a3ac7251c2cc2362bee3566522fe57b5f3bd8ed4b260'
  '1e7db24552f5eeb6f3d0d09c65708726dca36e5032c9e30af94be8db0de274ce'
  '89066afcc16dfed2d03b9b9e36b449eeb72ec17c8abfe5d72f15b6f1440bb870'
  '7e2e2fa590a6df090c53e4eb3fbddcabef29f4aa188c1490c4a9215a69fe2a0a'
  '03181e10ba96fe4da2946fde4f1246e0fe8b24caa7e4955a18a7b230cb6ab720'
  'bd2a676bb60f06b8c1c991a644ce34a0d1f17e4430c44775bbedd791cdb6e92e'
)

prepare() {
  rm -rf -- "${srcdir}/module"
  mkdir -p -- "${srcdir}/module/sources"
  local version
  for version in 7.3.3 7.3.4 6.18.60; do
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
  install -m644 "${srcdir}/module/sources/xpad-linux-6.18.60.c" "${srcdir}/module/sources/xpad-linux-7.3.4.c" "${dst}/sources/"
  install -m644 "${srcdir}/Makefile" "${srcdir}/Kbuild" "${dst}/"
  sed "s/@PKGVER@/${pkgver}/g" "${srcdir}/dkms.conf" > "${dst}/dkms.conf"
  chmod 644 "${dst}/dkms.conf"
}
