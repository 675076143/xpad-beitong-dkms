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
source=(
  'beitong-gip-init.patch'
  'Makefile'
  'dkms.conf'
  'xpad.c::https://raw.githubusercontent.com/torvalds/linux/refs/tags/v7.3/drivers/input/joystick/xpad.c'
)
sha256sums=('324f341da568c69a2e8e85d9cce787c8f88c71b7b83da82e83113bb0205cb3dd'
            '14997cba13de06821537a419ca185a7e424495f420cc91b701e4562e6e5adad8'
            '36a339eccc17148a1c878fed96daec7e121ccbb9b819408e5cfb0bc45858d809'
            'b47281151829fc382c4bcb5f466865f476a6f4ebfacd617ee49393f99c1e3950')


prepare() {
  msg2 "Using downloaded xpad.c, corresponding kernal version is v7.3"
}

package() {
  cd "${srcdir}"
  local dkms_dst="${pkgdir}/usr/src/xpad-beitong-${pkgver}"

  install -Dm644 xpad.c               "${dkms_dst}/xpad.c"
  install -Dm644 beitong-gip-init.patch "${dkms_dst}/patches/beitong-gip-init.patch"
  install -Dm644 Makefile             "${dkms_dst}/Makefile"

  sed "s/@PKGVER@/${pkgver}/g" "${srcdir}/dkms.conf" > "${dkms_dst}/dkms.conf"
  chmod 644 "${dkms_dst}/dkms.conf"
}
