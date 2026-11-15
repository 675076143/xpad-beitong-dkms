#!/usr/bin/env python3
"""Offline checks; temporary files only, no package/module installation."""
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {'7.3.3-1-cachyos': ('7.3.3', 'CLANG', '1'),
           '7.3.4-1-cachyos': ('7.3.4', 'CLANG', '1'),
           '6.18.60-2-cachyos-lts': ('6.18.60', 'GCC', '')}
INPUTS = ('PKGBUILD', 'xpad-linux-7.3.3.c', 'xpad-linux-6.18.60.c',
          'beitong-linux-7.3.3.patch', 'beitong-linux-6.18.60.patch',
          'xpad-linux-7.3.4.c', 'beitong-linux-7.3.4.patch',
          'Makefile', 'Kbuild', 'dkms.conf', 'SOURCES.md')


def run(args, cwd):
    env = os.environ.copy()
    for key in ('LLVM', 'XPAD_LLVM', 'CC', 'LD', 'MAKEFLAGS', 'MFLAGS', 'MAKELEVEL'):
        env.pop(key, None)
    return subprocess.run(args, cwd=cwd, env=env, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='xpad-check-')
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)

    def test_exact_target_source_compiler_and_overrides(self):
        module = self.work / 'module'
        headers = self.work / 'headers'
        (module / 'sources').mkdir(parents=True)
        (headers / 'include/config').mkdir(parents=True)
        shutil.copy2(ROOT / 'Makefile', module)
        (headers / 'Makefile').write_text(
            '.PHONY: modules clean\nmodules clean:\n'
            '\t@echo "selected LLVM=$(LLVM) CC=$(CC) release=$(KERNELRELEASE)"\n')
        for target, (version, compiler, llvm) in TARGETS.items():
            (headers / 'include/config/kernel.release').write_text(target+'\n')
            (headers / '.config').write_text(f'CONFIG_CC_IS_{compiler}=y\n')
            (module / f'sources/xpad-linux-{version}.c').write_text(version+'\n')
            p = run(['make', f'KDIR={headers}', f'KVER={target}', f'KERNELRELEASE={target}'], module)
            self.assertEqual(p.returncode, 0, p.stdout)
            self.assertIn(f'selected LLVM={llvm} CC=', p.stdout)
            self.assertEqual((module / 'xpad.c').read_text(), version+'\n')
        target = '6.18.60-2-cachyos-lts'
        for args, expected in [(['LLVM=1', 'CC=custom-clang'], 'LLVM=1 CC=custom-clang'),
                               (['LLVM=1', 'XPAD_LLVM='], 'LLVM= CC=')]:
            p = run(['make', f'KDIR={headers}', f'KVER={target}', *args], module)
            self.assertEqual(p.returncode, 0, p.stdout)
            self.assertIn('selected '+expected, p.stdout)
        (headers / '.config').unlink()
        p = run(['make', f'KDIR={headers}', f'KVER={target}'], module)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('Cannot identify target compiler', p.stdout)
        p = run(['make', f'KDIR={headers}', f'KVER={target}', 'LLVM=-23', 'clean'], module)
        self.assertEqual(p.returncode, 0, p.stdout)
        p = run(['make', f'KDIR={headers}', 'KVER=7.3.5-1-cachyos', 'LLVM=1'], module)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('Unsupported target', p.stdout)
        (headers / 'include/config/kernel.release').write_text('different-headers\n')
        p = run(['make', f'KDIR={headers}', f'KVER={target}', 'LLVM=1'], module)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('Target headers do not match', p.stdout)

    def test_checksums_repeat_prepare_and_stock_fixes(self):
        for name in INPUTS:
            shutil.copy2(ROOT / name, self.work)
        digests = []
        for _ in range(2):
            p = run(['makepkg', '--nobuild', '--nodeps'], self.work)
            self.assertEqual(p.returncode, 0, p.stdout)
            current = []
            for version, _, _ in TARGETS.values():
                src = self.work / f'src/module/sources/xpad-linux-{version}.c'
                current.append(hashlib.sha256(src.read_bytes()).hexdigest())
                text = src.read_text()
                self.assertIn('if (len >= offset)', text)
                self.assertNotIn('0x518b', text)
                def ids(s):
                    return set(re.findall(r'\{ (0x[0-9a-f]+), (0x[0-9a-f]+),', s))
                self.assertTrue(ids((ROOT / f'xpad-linux-{version}.c').read_text()) <= ids(text))
            digests.append(current)
        self.assertEqual(digests[0], digests[1])
        with (self.work / 'xpad-linux-7.3.3.c').open('a') as f:
            f.write('\n/* deliberate checksum test */\n')
        p = run(['makepkg', '--verifysource', '--nodeps'], self.work)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('FAILED', p.stdout)

    def test_srcinfo_and_dkms_allowlist(self):
        p = run(['makepkg', '--printsrcinfo'], ROOT)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertEqual(p.stdout, (ROOT / '.SRCINFO').read_text())
        config = (ROOT / 'dkms.conf').read_text()
        pattern = re.search(r'BUILD_EXCLUSIVE_KERNEL="([^"]+)"', config).group(1)
        for target in TARGETS:
            self.assertIsNotNone(re.fullmatch(pattern, target))
        for target in ('7.3.5-1-cachyos', '6.18.61-2-cachyos-lts', '7.3.3-custom'):
            self.assertIsNone(re.fullmatch(pattern, target))


if __name__ == '__main__':
    unittest.main(verbosity=2)
