[app]

# (str) Název vaší aplikace
title = Marble

# (str) Název balíčku
package.name = marbleapp

# (str) Doména balíčku (potřebná pro balení pro android/ios)
package.domain = com.porplycia

# (str) Zdrojový kód, kde se nachází main.py
source.dir = .

# (list) Zdrojové soubory, které se mají zahrnout (nechte prázdné, aby zahrnovaly všechny soubory)
#source.include_exts = py,png,kv,ttf,ini,wav

# (list) Seznam začleněných souborů pomocí porovnávání vzorů
source.include_patterns = sounds/*.wav,images/*.png

# (list) Zdrojové soubory k vyloučení (nechte prázdné, abyste nic nevylučovali)
#source.exclude_exts = spec

# (list) Seznam adresářů k vyloučení (nechat prázdný, aby se nic nevyloučilo)
#source.exclude_dirs = tests, bin, venv

# (list) Seznam vyloučení pomocí porovnávání vzorů
# Nepoužívejte předponu './'
#source.exclude_patterns = license,images/*/*.jpg

# (str) Verzování aplikace (metoda 1)
version = 0.1

# (str) Verzování aplikace (metoda 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Požadavky na aplikaci
# oddělené čárkou např. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) CVlastní zdrojové složky pro požadavky
# Nastaví vlastní zdrojový kód pro všechny požadavky s recepty
# requirements.source.kivy = ../../kivy

# (str) PPředvolba aplikace
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Ikona aplikace
icon.filename = %(source.dir)s/icon.png

# (list) Podporované orientace
# Platné možnosti jsou: landscape, portrait, portrait-reverse or landscape-reverse
orientation = portrait, landscape

# (list) Seznam služeb, které mají být deklarovány
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Jaroslav Porplycia

# měna hlavní verze pythonu používané aplikací
osx.python_version = 3.10.6

# Verze Kivy, která se má používat
osx.kivy_version = 2.1.0

#
# Android specific
#

# (bool) Určuje, zda má být aplikace celoobrazovková, nebo ne
fullscreen = 0

# (string) Barva pozadí Presplash (pro řetězec nástrojů android)
# Podporované formáty jsou: #RRGGBB #AARRGGBB nebo jeden z následujících názvů:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
android.presplash_color = blue

# (string) Animace Presplash s použitím formátu Lottie.
# Příklady viz https://lottiefiles.com/ a https://airbnb.design/lottie/
# pro obecnou dokumentaci.
# Soubory Lottie lze vytvářet pomocí různých nástrojů, například Adobe After Effect nebo Synfig.
#android.presplash_lottie = "path/to/lottie/file.json"

# (str) Adaptivní ikona aplikace (používá se, pokud je úroveň API Androidu 26+ za běhu)
#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
#icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

# (list) Oprávnění
# (Všechny podporované syntaxe a vlastnosti viz https://python-for-android.readthedocs.io/en/latest/buildoptions/#build-options-1)
#android.permissions = android.permission.RECORD_AUDIO

# (list) features (přidává do manifestu uses-feature -tags)
#android.features = android.hardware.usb.host

# (int) Cílové API Androidu, mělo by být co nejvyšší.
#android.api = 31

# (int) Minimální API, které bude váš APK / AAB podporovat.
#android.minapi = 21

# (int) Verze Android SDK, která se má použít.
#android.sdk = 20

# (str) Verze NDK pro Android, kterou chcete použít
#android.ndk = 23b

# (int) Android NDK API k použití. Jedná se o minimální API, které bude vaše aplikace podporovat, obvykle by mělo odpovídat android.minapi.
#android.ndk_api = 21

# (bool) Použití --private data storage (True) nebo --dir public storage (False).
android.private_storage = True

# (str) Adresář Android NDK (pokud je prázdný, bude stažen automaticky.)
#android.ndk_path =

# (str) Adresář Android SDK (pokud je prázdný, bude stažen automaticky.)
#android.sdk_path =

# (str) adresář ANT (pokud je prázdný, bude automaticky stažen.)
#android.ant_path =

# (bool) Pokud True, přeskočíte pokus o aktualizaci sdk Androidu.
# To může být užitečné, abyste se vyhnuli nadměrnému stahování z internetu nebo ušetřili čas
# když má dojít k aktualizaci a vy chcete pouze otestovat/vyrobit svůj balíček
android.skip_update = True

# (bool) Pokud True, pak automaticky akceptujte licenci SDK
# dohody. Toto je určeno pouze pro automatizaci. Pokud je nastaveno na False,
# výchozí nastavení, zobrazí se licence při prvním spuštění buildozeru.
# android.accept_sdk_license = False

# (str) Vstupní bod pro Android, výchozí hodnota je pro aplikace založené na Kivy-based app.
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Úplný název včetně cesty k balíčku třídy Java, která implementuje Android Activity
# použijte tento parametr spolu s android.entrypoint pro nastavení vlastní třídy Java místo PythonActivity
#android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra xml pro zápis přímo do elementu <manifest> souboru AndroidManifest.xml
# použijte tento parametr pro zadání názvu souboru, odkud se načte váš vlastní kód XML
#android.extra_manifest_xml = ./src/android/extra_manifest.xml

# (str) Extra xml pro zápis přímo uvnitř tagu <manifest><application> souboru AndroidManifest.xml
# použijte tento parametr pro zadání názvu souboru, odkud se načtou vaše vlastní argumenty XML:
#android.extra_manifest_application_arguments = ./src/android/extra_manifest_application_arguments.xml

# (str) Úplný název včetně cesty k balíčku třídy Java, která implementuje službu Python Service
# použijte tento parametr pro nastavení vlastní třídy Java, která rozšiřuje PythonService
#android.service_class_name = org.kivy.android.PythonService

# (str) téma aplikace pro Android, výchozí je pro aplikaci založenou na Kivy-based app
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Vzor pro whitelist pro celý projekt
#android.whitelist =

# (str) Cesta k vlastnímu souboru whitelistu
#android.whitelist_src =

# (str) Cesta k vlastnímu souboru blacklistu
#android.blacklist_src =

# (list) Seznam souborů Java .jar, které se přidají do knihoven, aby k nim mohl pyjnius přistupovat
# jejich třídám. Nepřidávejte jary, které nepotřebujete, protože další jary mohou zpomalit
# zpomalit proces sestavování. Umožňuje přiřazování zástupných znaků, např:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) Seznam souborů Java, které se mají přidat do projektu android (může to být java nebo a
# adresář obsahující soubory)
#android.add_src =

# (list) Archivy AAR pro Android, které se mají přidat
#android.add_aars =

# (list) Vložte tyto soubory nebo adresáře do adresáře apk assets.
# Lze použít obě formy a assets nemusí být v adresáři 'source.include_exts'.
# 1) android.add_assets = source_asset_relative_path
# 2) android.add_assets = source_asset_path:destination_asset_relative_path
#android.add_assets =

Vložte tyto soubory nebo adresáře do adresáře apk res.
# Volbu lze použít třemi způsoby, hodnota může obsahovat jeden nebo nula znaků ':'.
# Některé příklady:
# 1) Soubor, který se přidá do zdrojů, legální názvy zdrojů obsahují ['a-z','0-9','_'].
# android.add_resources = my_icons/all-inclusive.png:drawable/all_inclusive.png
# 2) Adresář, zde 'legal_icons', musí obsahovat zdroje jednoho druhu
# android.add_resources = legal_icons:drawable
# 3) Adresář, zde 'legal_resources' musí obsahovat jeden nebo více adresářů, 
# každý s jedním druhem zdroje: drawable, xml atd...
# android.add_resources = legal_resources
#android.add_resources =

# (list) Závislosti Gradle k přidání
#android.gradle_dependencies =

# (bool) Zapnout podporu AndroidX. Enable when 'android.gradle_dependencies'
# obsahuje balíček 'androidx' nebo jakýkoli balíček ze zdrojového kódu Kotlin.
# android.enable_androidx requires android.api >= 28
#android.enable_androidx = True

# (list) přidat možnosti kompilace java
# to může být nezbytné například při importu určitých knihoven java pomocí volby 'android.gradle_dependencies'.
# další informace naleznete na https://developer.android.com/studio/write/java8-support
# android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Repozitáře Gradle, které je třeba přidat {může být nutné pro některé android.gradle_dependencies}
# prosím uzavřete do dvojitých uvozovek 
# např. android.gradle_repositories = "maven { url 'https://kotlin.bintray.com/ktor' }"
#android.add_gradle_repositories =

# (list) možností balíčkování, které se mají přidat 
# viz https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# může být nutné řešit konflikty v gradle_dependencies
# prosím uzavřete do dvojitých uvozovek 
# např. android.add_packaging_options = "exclude 'META-INF/common.kotlin_module'", "exclude 'META-INF/*.kotlin_module'".
#android.add_packaging_options =

# (list) Třídy Java, které se přidají jako aktivity do manifestu.
#android.add_activities = com.example.ExampleActivity

# (str) Kategorie konzole OUYA. Měla by to být jedna z možností GAME nebo APP
# Pokud tuto položku necháte prázdnou, podpora OUYA nebude povolena.
#android.ouya.category = GAME

# (str) Název souboru ikony konzole OUYA. Musí to být obrázek png 732x412.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) Soubor XML, který se má zahrnout jako filtr záměru do značky <activity>.
#android.manifest.intent_filters =

# (list) Zkopírujte tyto soubory do src/main/res/xml/ (používá se například u intent-filters)
#android.res_xml = PATH_TO_FILE,

# (str) launchMode pro nastavení hlavní aktivity
#android.manifest.launch_mode = standard

# (str) screenOrientation pro nastavení hlavní aktivity.
# Platné hodnoty naleznete na adrese https://developer.android.com/guide/topics/manifest/activity-element.
#android.manifest.orientation = fullSensor

# (list) doplňkové knihovny Androidu, které se zkopírují do libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Určuje, zda má obrazovka zůstat zapnutá
# Nezapomeňte přidat oprávnění WAKE_LOCK, pokud nastavíte tuto hodnotu na True
#android.wakelock = False

# (list) Metadata aplikace Android, která se mají nastavit (formát klíč=hodnota)
#android.meta_data =

# (list) Projekt knihovny systému Android, který se má přidat (bude přidán do
# project.properties automaticky.)
#android.library_references =

# (list) sdílené knihovny Androidu, které budou přidány do souboru AndroidManifest.xml pomocí značky <uses-library>.
#android.uses_library =

# (str)  filtry Android logcat, které se mají použít
#android.logcat_filters = *:S python:D

# (bool) Android logcat zobrazí pouze log pro pid aktivity
#android.logcat_pid_only = False

# (str) Další argumenty adb pro Android
#android.adb_args = -H host.docker.internal

# (bool) Kopírování knihovny místo vytváření libpymodules.so
#android.copy_libs = 1

# (list) Architektura Androidu, pro kterou se má sestavovat, na výběr: armeabi-v7a, arm64-v8a, x86, x86_64
# V minulosti to bylo `android.arch`, protože jsme nepodporovali sestavení pro více archů najednou.
android.archs = arm64-v8a, armeabi-v7a

# (int) přepíše automatický výpočet versionCode (používá se v build.gradle)
# toto není totéž co verze aplikace a mělo by se upravovat pouze v případě, že víte, co děláte
# android.numeric_version = 1

# (bool) zapíná funkci automatického zálohování Androidu (Android API >=23)
android.allow_backup = True

# (str) soubor XML pro vlastní pravidla zálohování (viz oficiální dokumentace k automatickému zálohování)
# android.backup_rules =

# (str) Pokud potřebujete vložit proměnné do souboru AndroidManifest.xml,
# můžete tak učinit pomocí vlastnosti manifestPlaceholders.
# Tato vlastnost přebírá mapu dvojic klíč-hodnota. (prostřednictvím řetězce)
# Příklad použití : android.manifest_placeholders = [myCustomUrl:\"org.kivy.customurl\"]
# android.manifest_placeholders = [:]

# (bool) Přeskočit kompilaci bajtů pro soubory .py
# android.no-byte-compile-python = False

# (str) Formát použitý k zabalení aplikace pro režim vydání (aab nebo apk nebo aar).
# android.release_artifact = aab

# (str) Formát použitý k zabalení aplikace pro režim ladění (apk nebo aar).
# android.debug_artifact = apk

#
# Python for android (p4a) specifika
#

# (str) adresa URL python-for-android, která se má použít pro checkout
#p4a.url =

# (str) python-for-android fork, který se použije v případě, že není zadáno p4a.url, výchozí je upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android specifická revize, která se má použít, výchozí hodnota je HEAD, musí být uvnitř p4a.branch
#p4a.commit = HEAD

# (str) adresář git klonu python-for-android (pokud je prázdný, bude automaticky naklonován z githubu)
#p4a.source_dir =

# (str) Adresář, ve kterém má python-for-android hledat vaše vlastní sestavovací recepty (pokud existují)
#p4a.local_recipes =

# (str) Název souboru s háčkem pro p4a
#p4a.hook =

# (str) Bootstrap, který se má použít pro sestavení pro android
# p4a.bootstrap = sdl2

# (int) číslo portu pro zadání explicitního argumentu --port= p4a (např. pro bootstrap flask)
#p4a.port =

# Řízení předávání --use-setup-py vs --ignore-setup-py do p4a
# "v budoucnu" bude --use-setup-py výchozím chováním v p4a, nyní tomu tak není
# Nastavením této hodnoty na false projde --ignore-setup-py, true projde --use-setup-py
# POZNÁMKA: jedná se o obecnou integraci setuptools, stačí mít pyproject.toml, není třeba generovat
# setup.py, pokud používáte Poetry, ale musíte přidat "toml" do source.include_exts.
#p4a.setup_py = false

# (str) dodatečné argumenty příkazového řádku, které se předávají při volání pythonforandroid.toolchain
#p4a.extra_args =



#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency: ios-deploy
# Uncomment to use a custom checkout
#ios.ios_deploy_dir = ../ios_deploy
# Or specify URL and branch
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

# (bool) Whether or not to sign the code
ios.codesign.allowed = false

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) The development team to use for signing the debug version
#ios.codesign.development_team.debug = <hexstring>

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s

# (str) The development team to use for signing the release version
#ios.codesign.development_team.release = <hexstring>

# (str) URL pointing to .ipa file to be installed
# This option should be defined along with `display_image_url` and `full_size_image_url` options.
#ios.manifest.app_url =

# (str) URL pointing to an icon (57x57px) to be displayed during download
# This option should be defined along with `app_url` and `full_size_image_url` options.
#ios.manifest.display_image_url =

# (str) URL pointing to a large icon (512x512px) to be used by iTunes
# This option should be defined along with `app_url` and `display_image_url` options.
#ios.manifest.full_size_image_url =


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns.
#    Instead of doing:
#
#[app]
#source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    This can be translated into:
#
#[app:source.exclude_patterns]
#license
#data/audio/*.wav
#data/images/original/*
#


#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could first change the title to add "(demo)" in the name
#    and extend the excluded directories to remove the HD content.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
#    Then, invoke the command line with the "demo" profile:
#
#buildozer --profile demo android debug
