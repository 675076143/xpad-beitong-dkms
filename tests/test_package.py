#!/usr/bin/env python3
"""Offline checks; writes only temporary files, never installs a package/module."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def run(args, cwd, **kwargs):
    env = os.environ.copy()
    for key in ('LLVM', 'XPAD_LLVM', 'CC', 'LD', 'MAKEFLAGS', 'MFLAGS', 'MAKELEVEL'):
        env.pop(key, None)
    return subprocess.run(args, cwd=cwd, env=env, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='xpad-check-')
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)

    def test_target_selection_overrides_and_dkms_kernelrelease(self):
        module = self.work / 'module'
        headers = self.work / 'headers'
        module.mkdir()
        headers.mkdir()
        shutil.copy2(ROOT / 'Makefile', module)
        (headers / 'Makefile').write_text(
            '.PHONY: modules clean\nmodules clean:\n'
            '\t@echo "selected LLVM=$(LLVM) CC=$(CC) release=$(KERNELRELEASE)"\n')
        for compiler, expected in [('CLANG', '1'), ('GCC', '')]:
            (headers / '.config').write_text(f'CONFIG_CC_IS_{compiler}=y\n')
            p = run(['make', f'KDIR={headers}', 'KERNELRELEASE=test-target'], module)
            self.assertEqual(p.returncode, 0, p.stdout)
            self.assertIn(f'selected LLVM={expected} CC=', p.stdout)
            self.assertIn('release=test-target', p.stdout)
        (headers / '.config').write_text('CONFIG_CC_IS_CLANG=y\n')
        p = run(['make', f'KDIR={headers}', 'LLVM=', 'CC=custom-gcc'], module)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn('selected LLVM= CC=custom-gcc', p.stdout)
        p = run(['make', f'KDIR={headers}', 'LLVM=1', 'XPAD_LLVM='], module)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn('selected LLVM= CC=', p.stdout)
        (headers / '.config').unlink()
        p = run(['make', f'KDIR={headers}'], module)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('Cannot identify target compiler', p.stdout)
        p = run(['make', f'KDIR={headers}', 'LLVM=-23', 'clean'], module)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn('selected LLVM=-23', p.stdout)

    def test_makepkg_checksums_and_repeat_prepare(self):
        for name in ('PKGBUILD', 'xpad-linux-6.18.c', 'beitong-gip-init.patch',
                     'Makefile', 'Kbuild', 'dkms.conf'):
            shutil.copy2(ROOT / name, self.work)
        digests = []
        for _ in range(2):
            p = run(['makepkg', '--nobuild', '--nodeps'], self.work)
            self.assertEqual(p.returncode, 0, p.stdout)
            digests.append(hashlib.sha256((self.work / 'src/module/xpad.c').read_bytes()).hexdigest())
        self.assertEqual(digests[0], digests[1])
        with (self.work / 'xpad-linux-6.18.c').open('a') as f:
            f.write('\n/* deliberate checksum test */\n')
        p = run(['makepkg', '--verifysource', '--nodeps'], self.work)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('FAILED', p.stdout)

    def test_srcinfo_matches(self):
        p = run(['makepkg', '--printsrcinfo'], ROOT)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertEqual(p.stdout, (ROOT / '.SRCINFO').read_text())


if __name__ == '__main__':
    unittest.main(verbosity=2)
