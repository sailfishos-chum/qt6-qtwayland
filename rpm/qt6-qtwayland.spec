Summary: Qt6 - Wayland platform support and QtCompositor module
Name:    qt6-qtwayland
Version: 6.7.2
Release: 0%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

Source0: %{name}-%{version}.tar.bz2

# filter qml provides
%global __provides_exclude_from ^%{_qt6_archdatadir}/qml/.*\\.so$

BuildRequires: clang
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: qt6-qtbase-devel >= %{version}
BuildRequires: qt6-qtbase-static
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel

BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(wayland-scanner)
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-cursor)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libinput)

BuildRequires:  libXext-devel

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
Requires: qt6-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# BuildRequires: qt6-qtwayland-devel >= %{version}
%description examples
%{summary}.
%endif

%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=OFF \
  -DQT_INSTALL_EXAMPLES_SOURCES=OFF

%cmake_build


%install
%cmake_install

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%license LICENSES/*
%{_qt6_libdir}/libQt6WaylandCompositor.so.6*
%{_qt6_libdir}/libQt6WaylandClient.so.6*
%{_qt6_libdir}/libQt6WaylandCompositor.so.6*
%{_qt6_libdir}/libQt6WaylandClient.so.6*
%{_qt6_libdir}/libQt6WaylandEglClientHwIntegration.so.6*
%{_qt6_libdir}/libQt6WaylandEglCompositorHwIntegration.so.6*
%{_qt6_libdir}/libQt6WlShellIntegration.so.6*
%{_qt6_plugindir}/wayland-decoration-client/
%{_qt6_plugindir}/wayland-graphics-integration-server
%{_qt6_plugindir}/wayland-graphics-integration-client
%{_qt6_plugindir}/wayland-shell-integration
%{_qt6_plugindir}/platforms/libqwayland-egl.so
%{_qt6_plugindir}/platforms/libqwayland-generic.so
#{_qt6_plugindir}/platforms/libqwayland-xcomposite-egl.so
#{_qt6_plugindir}/platforms/libqwayland-xcomposite-glx.so
%{_qt6_qmldir}/QtWayland/

%files devel
%{_qt6_libexecdir}/qtwaylandscanner
%{_qt6_headerdir}/QtWaylandCompositor/
%{_qt6_headerdir}/QtWaylandClient/
%{_qt6_headerdir}/QtWaylandEglClientHwIntegration/
%{_qt6_headerdir}/QtWaylandEglCompositorHwIntegration/
%{_qt6_headerdir}/QtWlShellIntegration/
%{_qt6_headerdir}/QtWaylandGlobal/
%{_qt6_libdir}/libQt6WaylandCompositor.so
%{_qt6_libdir}/libQt6WaylandClient.so
%{_qt6_libdir}/libQt6WaylandEglClientHwIntegration.so
%{_qt6_libdir}/libQt6WaylandEglCompositorHwIntegration.so
%{_qt6_libdir}/libQt6WlShellIntegration.so
%{_qt6_libdir}/libQt6WaylandCompositor.prl
%{_qt6_libdir}/libQt6WaylandClient.prl
%{_qt6_libdir}/libQt6WaylandEglClientHwIntegration.prl
%{_qt6_libdir}/libQt6WaylandEglCompositorHwIntegration.prl
%{_qt6_libdir}/libQt6WlShellIntegration.prl
%{_qt6_libdir}/cmake/Qt6WaylandCompositor/Qt6WaylandCompositorConfig*.cmake
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%{_qt6_libdir}/cmake/Qt6/*.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtWaylandTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Gui/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositor/
%{_qt6_libdir}/cmake/Qt6WaylandCompositor/
%dir %{_qt6_libdir}/cmake/Qt6WaylandClient/
%{_qt6_libdir}/cmake/Qt6WaylandClient/
%dir %{_qt6_libdir}/cmake/Qt6WaylandScannerTools/
%{_qt6_libdir}/cmake/Qt6WaylandScannerTools/
%dir %{_qt6_libdir}/cmake/Qt6WaylandEglClientHwIntegrationPrivate/
%{_qt6_libdir}/cmake/Qt6WaylandEglClientHwIntegrationPrivate/
%dir %{_qt6_libdir}/cmake/Qt6WaylandEglCompositorHwIntegrationPrivate/
%{_qt6_libdir}/cmake/Qt6WaylandEglCompositorHwIntegrationPrivate/
%dir %{_qt6_libdir}/cmake/Qt6WlShellIntegrationPrivate/
%{_qt6_libdir}/cmake/Qt6WlShellIntegrationPrivate/
%dir  %{_qt6_libdir}/cmake/Qt6WaylandGlobalPrivate/
%{_qt6_libdir}/cmake/Qt6WaylandGlobalPrivate/
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc
