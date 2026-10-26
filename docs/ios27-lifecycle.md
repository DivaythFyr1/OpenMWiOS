# iOS 27 scene lifecycle migration

Status: implementation candidate; physical-device acceptance is outstanding.
Base: merged WO33 consolidation `31db729` (main at implementation start).
The reported startup exception has not been captured. Legacy lifecycle versus
SDK 27 is a strong compatibility hypothesis, not a verified diagnosis of that crash.

## Architecture and decision

SDL2 2.32.10 calls UIApplicationMain with SDLUIKitDelegate. Previously its
application:didFinishLaunchingWithOptions: scheduled postFinishLaunch, which
calls the forwarded SDL_main while SDL pumps the UIKit run loop. SDL creates
an SDL_uikitwindow using initWithFrame and retains it through SDL_WindowData;
its view controller owns the SDL view. UIKit_GL_CreateContext attaches the
existing SDLEAGLContext/view to that same window. OpenMW's SDL_main entry logs
sdl_application_entry and performs the existing platform bootstrap.

SDL's lifecycle observer formerly listened to four UIApplication notifications.
Its handlers send SDL app events and window focus/minimize/restore events.
OpenMW ignores the app background messages themselves, but consumes the window
events for focus and window visibility. The touch overlay attaches to the
key window's root view (with a connected-scenes fallback); it sends existing
SDL input events. The maintained ios/Info.plist.in feeds the app bundle through
CMake's MACOSX_BUNDLE_INFO_PLIST setting.

An app-only scene delegate would still leave SDL constructing an unassociated
window, scheduling main too early, and using application lifecycle notifications.
The targeted SDL2 patch keeps ownership and event translation together. No SDL3
migration or dependency version change is required.

## Implementation

- `ios/Info.plist.in`: one application UIWindowScene configuration, delegate
  OpenMWSDLSceneDelegate, multiple scenes disabled, no scene storyboard.
- `ports/sdl2/ios-scene-lifecycle.patch`: changes four SDL UIKit files. The
  existing app delegate retains the connected scene under SDL's ARC build.
  SDL_WindowData remains the owner of the gameplay window; the scene delegate
  does not create a second window or view controller.
- Scene connection records the scene. Activation schedules SDL startup on the
  next run-loop turn, after UIKit's callback returns. postFinishLaunch requires
  an active connected scene and sets a once-per-process guard before SDL_main.
  Deactivation cancels a pending start; later activation retries it.
- SDL's window uses initWithWindowScene and scene coordinate-space bounds.
  Missing/mismatched scene creation fails explicitly. The legacy temporary
  launch window is skipped for scene apps; the OS launch screen remains. There
  may be a blank interval during synchronous engine loading; no new loading UI
  is introduced.
- Scene activation/deactivation/background/foreground call the existing
  SDL_OnApplication handlers. The four application notification subscriptions
  are disabled for scene apps to avoid duplicate delivery. Process termination
  and memory-warning observation remain intact. No GLES context, framebuffer,
  shader, fog, or view-distance code changes.
- Disconnect hides/detaches the existing window and clears the scene reference.
  Reconnection reattaches it and activation restores visibility without running
  SDL_main again. Single scene only; secondary scenes/external displays are not
  supported. Reconnect, input cancellation and drawable restoration require
  device testing. Existing URL-to-SDL-drop routing is forwarded from scene APIs.
- `scripts/build-ios.sh` selects `ports/` with --overlay-ports. The SDL overlay
  copies the port from pinned vcpkg `cd61e1e26a038e82d6550a3ebbe0fbbfe7da78e3`,
  preserving version 2.32.10#1, archive SHA-512, features and existing patches.
  The added patch changes the port ABI/cache key; verify the build actually
  rebuilds SDL rather than using an independently installed legacy archive.
- `ports/icu/` retains pinned ICU 78.3#1 and its upstream patches/checksum. The
  iOS-only port option passes `cross_compiling=yes` to Autoconf. On the reported
  Apple Silicon/Xcode 27.1 run, ICU linked an iPhoneOS `conftest` but attempted
  to execute it on macOS because both `--build` and `--host` were
  `aarch64-apple-darwin`. `config.log` records `Killed: 9` and
  `cannot run C compiled programs` (configure exit 77). The existing host-tool
  build remains selected with `--with-cross-build`. The new option avoids that
  invalid execution attempt; successful ICU configuration/build still needs a
  fresh Mac retry. No ICU version or global triplet setting changes.

No generated project is edited. OpenMW gameplay, GL4ES, touch controls, dependency
versions, and the iOS 16.3 deployment minimum are unchanged. This is a local
adaptation, not a claim that upstream SDL provides this implementation.

## Cloud validation

154 host tests pass (148 inherited plus six focused lifecycle/build tests), Python 3.12.14,
GCC and CMake 4.3.4. New tests replay the patch, generate/parse the plist with
CMake, check single active-scene startup, SDL window ownership, notification
routing and overlay/version wiring. They are source contracts, not an Objective-C
UIKit compilation or device event-loop simulation.

All four overlay patches apply in port order to pristine SDL release-2.32.10,
commit `5d249570393f7a37e037abf22cd6012a4cc56a71`. The four pristine UIKit files
are retained in validation/fixtures/sdl2-2.32.10-uikit.zip with upstream license
headers and SHA-256 `f471b131a7a2b07ec86696fcc81172a7490c1bc94bd07ba783fbd13653b44b17`.

The existing validate-source.sh wrapper was run: regression tests, Bash/Python
syntax, CMake pin, JSON, all 15 OpenMW/nine GL4ES patches and all five dependency
revision checks passed. Its overall exit status is 1 because ShellCheck, plutil
and Ruby are unavailable here; ShellCheck and the wrapper's plist/YAML checks
are not passed checks. The new plist-generation test passes independently.
No Xcode generation, Objective-C compilation, app linking, launch or visual
qualification can be claimed from this Linux host.

## Required Xcode 27 / physical iPhone procedure

1. Use a fresh checkout of this PR, preserving existing local builds and edits.
   Select Xcode 27 with xcode-select; record `xcodebuild -version` and
   `xcrun --sdk iphoneos --show-sdk-version`. Use CMake 4.3.4, Python 3.10+,
   Ninja and the build prerequisites from integration-plan.md. Resolve the
   pinned ShellCheck host-architecture requirement before source validation.
2. Run `./scripts/bootstrap.sh`, `./scripts/validate-source.sh`, and
   `CONFIGURATION=Debug ./scripts/build-ios.sh`. Confirm vcpkg selects the local
   SDL port and builds its patched UIKit sources. This generates the project;
   it is not the final app compile. Preserve full configure/build logs. A cold
   OSG failure remains a separate build prerequisite; do not silently
   incorporate an unqualified workaround.
   On the reported Apple Silicon machine, confirm the ICU configure command
   contains `cross_compiling=yes` and completes before continuing. If it still
   fails, retain ICU's `config.log` and the configure out/err logs; do not
   advance dependency pins to work around an unidentified failure.
3. Open build/ios/OpenMW.xcodeproj. Select openmw, Debug and the physical iPhone.
   Select a local Personal Team and unique bundle identifier (free signing is
   sufficient). Keep these choices local and do not commit generated projects.
   Provide legally owned Morrowind files using the documented Documents layout.
4. Add an All Objective-C Exceptions breakpoint and symbolic breakpoints:
   `-[OpenMWSDLSceneDelegate scene:willConnectToSession:options:]`,
   `-[OpenMWSDLSceneDelegate sceneDidBecomeActive:]`,
   `-[SDLUIKitDelegate postFinishLaunch]`, `SDL_main`, `UIKit_CreateWindow`,
   and `UIKit_GL_CreateContext`. Run from Xcode. Verify connection then activation
   then a single SDL_main entry, with a scene-bound window before GLES creation.
5. If startup throws, capture the exception reason, `thread backtrace all`,
   `image list -o -f`, console log and built Info.plist. Use LLDB
   `po [[UIApplication sharedApplication] connectedScenes]` and
   `po [[[UIApplication sharedApplication] delegate] window]` to inspect ownership;
   inspect that window's windowScene, rootViewController and key-window state.
   Run `plutil -p build/ios/Debug/openmw.app/Info.plist` and
   `dwarfdump --uuid build/ios/Debug/openmw.app/openmw`; retain SDK, source SHA,
   app/dSYM UUID and exact signing/build configuration with the report.
6. Reach main menu and enter the world. Verify landscape in both directions,
   drawable dimensions, HUD, touch sticks/buttons, short/long presses and touch
   cancellation. Compare the same scene/settings with WO33; make no new claim
   about pre-existing foliage/fog defects. Check GL4ES still owns presentation.
7. Background during menu/gameplay, lock/unlock, interrupt with Control Center,
   and resume repeatedly. Verify focus/minimize/restore event delivery, no stuck
   touches, no duplicate SDL_main, no GLES background crash or black framebuffer,
   and working audio/input after resume. Exercise scene disconnect/reconnect if
   reproducible; distinguish it from process termination followed by cold launch.
8. Repeat cold launches and an optimized build. Record pass/fail for each item
   and attach logs/exception evidence. Keep the PR Draft until a clean Xcode 27
   build and physical-iPhone launch/resume validation succeed.

Remaining risks: unconfirmed original root cause; UIKit API/ARC compilation not
exercised here; SDL's existing status-bar/orientation APIs remain legacy; timing
of suspension, scene reconnect, GLES drawable restoration and held-touch
cancellation need device evidence. No paid Apple Developer membership is required.
