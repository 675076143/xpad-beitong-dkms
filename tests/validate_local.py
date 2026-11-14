#!/usr/bin/env python3
"""Build local source package and actual driver with DKMS in NEW isolated trees.

Never installs the package/module, runs depmod, or loads/unloads a module.
Usage: python tests/validate_local.py /absolute/new/evidence-directory
Requires locally installed makepkg, fakeroot, DKMS and both documented headers.
"""
from pathlib import Path
import hashlib
import os
import subprocess
import sys

repo = Path(__file__).resolve().parents[1]
out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=False)
env = os.environ.copy()
for key in ('LLVM', 'XPAD_LLVM', 'CC', 'LD', 'MAKEFLAGS', 'MFLAGS', 'KBUILD_OUTPUT', 'KBUILD_EXTMOD'):
    env.pop(key, None)
# Only the isolated, never-installed test outputs are unsigned. No config edited.
env['try_sign_modules'] = 'false'
(out / 'tmp').mkdir()
env['TMPDIR'] = str(out / 'tmp')


def run(name, args, cwd=repo, expected=0):
    p = subprocess.run(args, cwd=cwd, env=env, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out / (name + '.log')).write_text('$ ' + ' '.join(args) + '\n' + p.stdout + f'\nexit={p.returncode}\n')
    if p.returncode != expected:
        raise RuntimeError(f'{name} exit={p.returncode}; see {out}')
    print(f'{name}: exit={p.returncode} (expected {expected})', flush=True)
    return p.stdout


run('unit', [sys.executable, 'tests/test_package.py'])
run('package', ['makepkg', '--force'])
archive = repo / 'xpad-beitong-dkms-1.2-1-any.pkg.tar.zst'
listing = run('archive-list', ['bsdtar', '-tf', str(archive)])
allowed = {'.BUILDINFO', '.MTREE', '.PKGINFO', 'usr/', 'usr/src/',
           'usr/src/xpad-beitong-1.2/', 'usr/src/xpad-beitong-1.2/sources/'} | {
               'usr/src/xpad-beitong-1.2/' + n for n in ('sources/xpad-linux-7.3.3.c', 'sources/xpad-linux-6.18.60.c', 'Makefile', 'Kbuild', 'dkms.conf')}
assert set(listing.splitlines()) == allowed, listing
stage = out / 'stage'
stage.mkdir()
run('archive-extract', ['bsdtar', '-xf', str(archive), '-C', str(stage)])
source = stage / 'usr/src'
state = out / 'state'
install = out / 'install'
state.mkdir()
install.mkdir()
common = ['-m', 'xpad-beitong', '-v', '1.2', '--dkmstree', str(state),
          '--sourcetree', str(source), '--installtree', str(install)]
run('dkms-add', ['dkms', 'add', *common])
rows = []
for kernel in ('7.3.3-1-cachyos', '6.18.60-2-cachyos-lts'):
    run('dkms-' + kernel, ['dkms', 'build', *common, '-k', kernel,
                          '--kernelsourcedir', f'/usr/lib/modules/{kernel}/build', '-j', '2'])
    module = state / 'xpad-beitong/1.2' / kernel / 'x86_64/module/xpad.ko'
    assert module.is_file()
    vermagic = run('vermagic-' + kernel, ['modinfo', '-F', 'vermagic', str(module)]).strip()
    assert vermagic.split()[0] == kernel, vermagic
    rows.append(f'{kernel}: built, vermagic={vermagic}, sha256={hashlib.sha256(module.read_bytes()).hexdigest()}')
run('dkms-status', ['dkms', 'status', *common])
run('unsupported', ['dkms', 'build', *common, '-k', '7.3.4-1-cachyos',
                    '--kernelsourcedir', '/usr/lib/modules/7.3.3-1-cachyos/build'], expected=77)
assert not list(install.iterdir()), 'isolation install tree must stay empty'
(out / 'summary.txt').write_text('\n'.join(rows) + '\nNo package/module installation or live-driver changes.\n')
print('\n'.join(rows))
