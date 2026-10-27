"""Host contracts for the opt-in diagnostic path; no device/FPS claims."""
import os
import pathlib
import re
import shutil
import subprocess
import tempfile
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'validation/fixtures'
BRIDGE = ROOT / 'ios/openmw_ios_renderer_diagnostics.mm'
OSG_PATCH = ROOT / 'ios/patches/osg-route-gl-entry-points-through-gl4es.patch'


def run(command, **kwargs):
    return subprocess.run(command, check=True, capture_output=True, text=True, **kwargs)


def materialize_gl4es(destination):
    with zipfile.ZipFile(FIXTURES / 'gl4es-c9895df-wo33-patch-inputs.zip') as archive:
        archive.extractall(destination)
    for file in destination.rglob('*'):
        if file.is_file():
            file.write_bytes(file.read_bytes().replace(b'\r\n', b'\n'))
    for patch in sorted((ROOT / 'patches/gl4es').glob('*.patch')):
        run(['git', 'apply', str(patch)], cwd=destination)


class RendererConfigurationTests(unittest.TestCase):
    def test_actual_configuration_function_exact_value_and_process_lifetime(self):
        compiler = shutil.which('c++')
        if not compiler:
            self.skipTest('C++ compiler unavailable')
        source = BRIDGE.read_text()
        # Compile the actual portable function from the Objective-C++ bridge.
        function = re.search(r'extern "C" int openmw_ios_renderer_diag_enabled\(void\)\n\{.*?\n\}',
                             source, re.S).group()
        with tempfile.TemporaryDirectory() as directory:
            temp = pathlib.Path(directory)
            cpp = temp / 'configuration.cpp'
            cpp.write_text('#include <cstdlib>\n#include <cstdio>\n' + function + '''
int main() {
    int first = openmw_ios_renderer_diag_enabled();
    setenv("OPENMW_IOS_RENDERER_DIAGNOSTICS", first ? "0" : "1", 1);
    std::printf("%d %d\\n", first, openmw_ios_renderer_diag_enabled());
}
''')
            binary = temp / 'configuration'
            run([compiler, '-std=c++17', str(cpp), '-o', str(binary)])
            for value in (None, '', '0', '1', 'true', '01', '10', '1 ', ' 1'):
                with self.subTest(value=value):
                    env = os.environ.copy()
                    env.pop('OPENMW_IOS_RENDERER_DIAGNOSTICS', None)
                    if value is not None:
                        env['OPENMW_IOS_RENDERER_DIAGNOSTICS'] = value
                    expected = int(value == '1')
                    self.assertEqual(f'{expected} {expected}', run([str(binary)], env=env).stdout.strip())

    def test_every_public_bridge_entry_guards_before_work(self):
        functions = re.findall(r'extern "C" [\w ]+ (openmw_ios_renderer_diag_\w+)\([^{}]*?\)\n\{(.*?)\n\}',
                               BRIDGE.read_text(), re.S)
        self.assertGreater(len(functions), 10)
        for name, body in functions:
            if name.endswith('_enabled'):
                continue
            with self.subTest(function=name):
                self.assertTrue(body.lstrip().startswith('if (!openmw_ios_renderer_diag_enabled())'))

    def test_materialized_gl4es_enabled_and_disabled_bridge(self):
        compiler = shutil.which('cc')
        if not compiler:
            self.skipTest('C compiler unavailable')
        with tempfile.TemporaryDirectory() as directory:
            temp = pathlib.Path(directory)
            materialize_gl4es(temp)
            # Exercise the existing representative draw/upload/fog workload, using the
            # complete current production translation unit (including WO33 and this patch).
            fixture = (FIXTURES / 'wo32_gl4es_target_fixture.c').read_text()
            fixture = fixture.replace('#include <math.h>', '#include <math.h>\n#include <stdlib.h>')
            fixture = fixture.replace('int openmw_ios_renderer_diag_enabled(void)\n{\n    return 1;\n}',
                                      'int openmw_ios_renderer_diag_enabled(void)\n{\n    return getenv("TEST_ENABLED") != NULL;\n}')
            # Abort on any disabled bridge work, even if it would not emit output.
            fixture = re.sub(r'((?:unsigned int|int|uint64_t) openmw_ios_renderer_diag_(?!enabled)\w+\([^{}]*?\)\n\{)',
                             r'\1\n    if (!openmw_ios_renderer_diag_enabled()) abort();', fixture, flags=re.S)
            fixture += '''
void openmw_ios_renderer_diag_blend_event(const char* source, const char* site, const char* detail) {
    if (!openmw_ios_renderer_diag_enabled()) abort();
}
'''
            fixture = fixture.replace('int main(void)\n{', '''int main(void)
{
    if (wo31_diag_enabled() != (getenv("TEST_ENABLED") != NULL)) abort();
    wo31_diag_handshake("configuration-test");
    wo33_diag_blend_event("configuration-test", "test");
    wo32_diag_texture_target_for_name(42);
    const unsigned char pixels[] = {0, 64, 128, 255};
    wo31_diag_texture_upload(41, pixels, sizeof(pixels), 0x1908, 1, 1, 1, 0, 1);''')
            path = temp / 'fixture.c'
            path.write_text(fixture)
            binary = temp / 'fixture'
            run([compiler, '-std=c11', '-DWO31_DIAGNOSTIC_TEST_BRIDGE=1', '-I'+str(temp/'src/gl'),
                 str(temp/'src/gl/ios_renderer_diag.c'), str(path), '-o', str(binary)])
            env = os.environ.copy()
            env.pop('TEST_ENABLED', None)
            self.assertEqual('', run([str(binary)], env=env).stdout)
            env['TEST_ENABLED'] = '1'
            enabled = run([str(binary)], env=env).stdout
            for family in ('handshake', 'r1.upload', 'r1.draw.targeted', 'r2.received', 'r2.applied.targeted'):
                self.assertIn('"family":"'+family+'"', enabled)

    def test_callers_guard_expensive_work(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = pathlib.Path(directory)
            materialize_gl4es(temp)
            for file in ('drawing.c', 'listdraw.c'):
                source = (temp/'src/gl'/file).read_text()
                self.assertRegex(source, r'wo33_smoke_target_bound\(void\)\s*\{\s*if \(!wo31_diag_enabled\(\)\) return 0;')
            drawing = (temp/'src/gl/drawing.c').read_text()
            self.assertIn('if (wo31_diag_enabled()) {\n            program_t* wo31_program', drawing)
            shader = (temp/'src/gl/shader.c').read_text()
            self.assertIn('if(wo31_diag_enabled() && !*wo17_logged', shader)
        osg = OSG_PATCH.read_text()
        self.assertIn('!openmw_ios_renderer_diag_enabled()', osg)
        patch = (ROOT/'patches/openmw/0016-ios-opt-in-renderer-probes.patch').read_text()
        self.assertIn('if (!openmw_ios_renderer_diag_enabled()) return;', patch)
        self.assertIn('if (openmw_ios_renderer_diag_enabled() && wo23ProgramCount < 8', patch)

    def test_osg_patch_driver_accepts_current_and_rejects_stale_tree_without_writing(self):
        if not shutil.which('cmake') or not pathlib.Path('/usr/bin/patch').exists():
            self.skipTest('CMake and production /usr/bin/patch required')
        with tempfile.TemporaryDirectory() as directory:
            temp = pathlib.Path(directory)
            with zipfile.ZipFile(FIXTURES/'osg-01cc2b5-wo33-patch-inputs.zip') as archive:
                archive.extractall(temp)
            command = ['cmake', '-DOSG_SOURCE_DIR='+str(temp), '-DOSG_PATCH_FILE='+str(OSG_PATCH),
                       '-P', str(ROOT/'ios/cmake/apply-osg-patch.cmake')]
            run(command)
            self.assertIn('already applied', run(command).stdout)
            # Simulate an old patch: routing is present, but one diagnostic gate is absent.
            source = temp/'src/osg/Texture2D.cpp'
            old = source.read_text()
            stale = old.replace('!openmw_ios_renderer_diag_enabled()', 'false')
            self.assertNotEqual(old, stale)
            source.write_text(stale)
            before = {p.relative_to(temp): p.read_bytes() for p in temp.rglob('*') if p.is_file()}
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            self.assertIn('older or locally modified', result.stderr)
            self.assertEqual(before, {p.relative_to(temp): p.read_bytes() for p in temp.rglob('*') if p.is_file()})


if __name__ == '__main__':
    unittest.main()
