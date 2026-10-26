"""Source contract tests; UIKit execution still requires a physical device."""
import hashlib
import pathlib
import plistlib
import subprocess
import tempfile
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


class SceneLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.directory.cleanup)
        cls.source = pathlib.Path(cls.directory.name)
        fixture = ROOT / 'validation/fixtures/sdl2-2.32.10-uikit.zip'
        assert hashlib.sha256(fixture.read_bytes()).hexdigest() == (
            'f471b131a7a2b07ec86696fcc81172a7490c1bc94bd07ba783fbd13653b44b17')
        with zipfile.ZipFile(fixture) as archive:
            archive.extractall(cls.source)
        patch = ROOT / 'ports/sdl2/ios-scene-lifecycle.patch'
        subprocess.run(['git', 'apply', '--check', str(patch)], cwd=cls.source, check=True)
        subprocess.run(['git', 'apply', str(patch)], cwd=cls.source, check=True)
        cls.app = (cls.source / 'src/video/uikit/SDL_uikitappdelegate.m').read_text()

    def test_generated_manifest(self):
        output = self.source / 'Info.plist'
        script = self.source / 'generate.cmake'
        script.write_text(f'configure_file("{ROOT}/ios/Info.plist.in" "{output}" @ONLY)\n')
        subprocess.run(['cmake', '-P', str(script)], check=True)
        info = plistlib.loads(output.read_bytes())
        manifest = info['UIApplicationSceneManifest']
        self.assertFalse(manifest['UIApplicationSupportsMultipleScenes'])
        config, = manifest['UISceneConfigurations']['UIWindowSceneSessionRoleApplication']
        self.assertEqual(config['UISceneDelegateClassName'], 'OpenMWSDLSceneDelegate')
        self.assertNotIn('UISceneStoryboardFile', config)
        self.assertEqual(info['UISupportedInterfaceOrientations'],
                         ['UIInterfaceOrientationLandscapeLeft', 'UIInterfaceOrientationLandscapeRight'])

    def test_main_waits_for_active_scene_and_runs_once(self):
        body = self.app.split('- (void)postFinishLaunch\n')[1].split('- (BOOL)application:')[0]
        self.assertIn('self.openmwMainStarted || !self.openmwWindowScene', body)
        self.assertIn('UISceneActivationStateForegroundActive', body)
        self.assertLess(body.index('self.openmwMainStarted = YES'), body.index('forward_main('))
        connect = self.app.split('- (void)scene:(UIScene *)scene willConnectToSession:')[1].split('- (void)sceneDidBecomeActive:')[0]
        self.assertNotIn('forward_main(', connect)
        self.assertNotIn('performSelector', connect)
        active = self.app.split('- (void)sceneDidBecomeActive:')[1].split('- (void)sceneWillResignActive:')[0]
        self.assertIn('performSelector:@selector(postFinishLaunch)', active)

    def test_window_belongs_to_scene_and_sdl(self):
        window = (self.source / 'src/video/uikit/SDL_uikitwindow.m').read_text()
        self.assertIn('initWithWindowScene:scene', window)
        self.assertIn('scene.coordinateSpace.bounds', window)
        self.assertIn('if (!scene || scene.screen != data.uiscreen)', window)
        self.assertIn('SetupWindowData(_this, window, uiwindow, SDL_TRUE)', window)
        self.assertIn('app.window.windowScene = app.openmwWindowScene', self.app)
        self.assertIn('app.window.windowScene = nil', self.app)
        self.assertNotIn('openmwMainStarted = NO', self.app)

    def test_scene_events_use_existing_sdl_handlers_without_duplicate_app_observers(self):
        events = (self.source / 'src/video/uikit/SDL_uikitevents.m').read_text()
        block = events.split('if (![NSBundle.mainBundle objectForInfoDictionaryKey:@"UIApplicationSceneManifest"]) {')[1].split('        }')[0]
        for event in ('DidBecomeActive', 'WillResignActive', 'DidEnterBackground', 'WillEnterForeground'):
            self.assertIn('SDL_OnApplication' + event + '();', self.app)
            self.assertIn('UIApplication' + event + 'Notification', block)
        self.assertIn('cancelPreviousPerformRequestsWithTarget:app', self.app)
        self.assertIn('UIApplicationWillTerminateNotification', events)
        self.assertIn('UIApplicationDidReceiveMemoryWarningNotification', events)

    def test_dependency_pin_and_build_wiring(self):
        import json
        manifest = json.loads((ROOT / 'ports/sdl2/vcpkg.json').read_text())
        self.assertEqual(manifest['version'], '2.32.10')
        self.assertEqual(manifest['port-version'], 1)
        port = (ROOT / 'ports/sdl2/portfile.cmake').read_text()
        self.assertIn('ios-scene-lifecycle.patch', port)
        self.assertIn('--overlay-ports="${ROOT_DIR}/ports"', (ROOT / 'scripts/build-ios.sh').read_text())

    def test_icu_cross_configure_is_scoped_to_ios(self):
        import json
        original = ROOT / 'deps/vcpkg-pinned/ports/icu'
        overlay = ROOT / 'ports/icu'
        self.assertEqual(json.loads((overlay / 'vcpkg.json').read_text()),
                         json.loads((original / 'vcpkg.json').read_text()))
        extra = (overlay / 'portfile.cmake').read_text().split(
            'if(VCPKG_TARGET_IS_IOS)\n'
            '    vcpkg_list(APPEND CONFIGURE_OPTIONS cross_compiling=yes)\n'
            'endif()\n')
        self.assertEqual(len(extra), 2)
        self.assertIn('vcpkg_list(SET CONFIGURE_OPTIONS)', extra[0])
        self.assertIn('--with-cross-build=', extra[1])
        for name in ('disable-static-prefix.patch', 'vcpkg-cross-data.patch',
                     'mh-darwin.patch'):
            self.assertEqual((overlay / name).read_bytes(), (original / name).read_bytes())
