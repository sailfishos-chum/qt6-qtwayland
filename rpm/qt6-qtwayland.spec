%global  qt_version 6.7.2

Summary: Qt6 - Wayland platform support and QtCompositor module
Name:    qt6-qtwayland
Version: 6.8.3
Release: 0%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io

Source0: %{name}-%{version}.tar.bz2

# filter qml provides
%global __provides_exclude_from ^%{_qt6_archdatadir}/qml/.*\\.so$

BuildRequires: clang
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: qt6-qtbase-devel >= %{qt_version}
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
BuildRequires: pkgconfig(libudev)

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
Requires: qt6-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

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
%{_qt6_archdatadir}/sbom/%{qt_module}-%{qt_version}.spdx
%{_qt6_libdir}/libQt6WaylandCompositor.so.6*
%{_qt6_libdir}/libQt6WaylandCompositor.so.6*
%{_qt6_libdir}/libQt6WaylandCompositorIviapplication.so.6*
%{_qt6_libdir}/libQt6WaylandCompositorPresentationTime.so.6*
%{_qt6_libdir}/libQt6WaylandCompositorWLShell.so.6*
%{_qt6_libdir}/libQt6WaylandCompositorXdgShell.so.6*
%{_qt6_libdir}/libQt6WaylandEglCompositorHwIntegration.so.6*
%{_qt6_plugindir}/wayland-graphics-integration-server
%{_qt6_plugindir}/wayland-shell-integration
%{_qt6_qmldir}/QtWayland/

%files devel
%{_qt6_headerdir}/QtWaylandCompositor/
%{_qt6_headerdir}/QtWaylandCompositorIviapplication/
%{_qt6_headerdir}/QtWaylandCompositorPresentationTime/
%{_qt6_headerdir}/QtWaylandCompositorWLShell/
%{_qt6_headerdir}/QtWaylandCompositorXdgShell/
%{_qt6_headerdir}/QtWaylandEglCompositorHwIntegration/
%{_qt6_libdir}/libQt6WaylandCompositor.so
%{_qt6_libdir}/libQt6WaylandCompositorIviapplication.prl
%{_qt6_libdir}/libQt6WaylandCompositorIviapplication.so
%{_qt6_libdir}/libQt6WaylandCompositorPresentationTime.prl
%{_qt6_libdir}/libQt6WaylandCompositorPresentationTime.so
%{_qt6_libdir}/libQt6WaylandCompositorWLShell.prl
%{_qt6_libdir}/libQt6WaylandCompositorWLShell.so
%{_qt6_libdir}/libQt6WaylandCompositorXdgShell.prl
%{_qt6_libdir}/libQt6WaylandCompositorXdgShell.so
%{_qt6_libdir}/libQt6WaylandEglCompositorHwIntegration.so
%{_qt6_libdir}/libQt6WaylandCompositor.prl
%{_qt6_libdir}/libQt6WaylandEglCompositorHwIntegration.prl
%{_qt6_libdir}/cmake/Qt6WaylandCompositor/Qt6WaylandCompositorConfig*.cmake
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%dir %{_qt6_libdir}/cmake/Qt6WaylandClient/
%dir %{_qt6_libdir}/cmake/Qt6WaylandClientFeaturesPrivate/
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositor/
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorIviapplication/
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorIviapplicationPrivate
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorPresentationTime/
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorPresentationTimePrivate
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorPrivate
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorWLShell/
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorWLShellPrivate
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorXdgShell/
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorXdgShellPrivate
%dir %{_qt6_libdir}/cmake/Qt6WaylandEglCompositorHwIntegrationPrivate/
%{_qt6_libdir}/cmake/Qt6/*.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtWaylandTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandClient/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandClientFeaturesPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandCompositor/
%{_qt6_libdir}/cmake/Qt6WaylandCompositorIviapplication/
%{_qt6_libdir}/cmake/Qt6WaylandCompositorIviapplicationPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandCompositorPresentationTime/
%{_qt6_libdir}/cmake/Qt6WaylandCompositorPresentationTimePrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandCompositorPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandCompositorWLShell/
%{_qt6_libdir}/cmake/Qt6WaylandCompositorWLShellPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandCompositorXdgShell/
%{_qt6_libdir}/cmake/Qt6WaylandCompositorXdgShellPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandEglCompositorHwIntegrationPrivate/
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc
