%{?!ros_distro:%global ros_distro rolling}
%global pkg_name adaptive_component
%global normalized_pkg_name %{lua:return (string.gsub(rpm.expand('%{pkg_name}'), '_', '-'))}

Name:           ros-rolling-adaptive-component
Version:        0.2.1
Release:        4%{?dist}
Summary:        ROS %{pkg_name} package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  bloom-rpm-macros
BuildRequires:  cmake

%{?bloom_package}

%description
A composable container for Adaptive ROS 2 Node computations. Allows building
Nodes that can select between FPGA, CPU or GPU, at run-time. Stateless by
default, can be made stateful to meet use-case specific needs. Refer to examples
in README. Technically, provides A ROS 2 Node subclass programmed as a
&quot;Component&quot; and including its own single threaded executor to build
adaptive computations. Adaptive ROS 2 Nodes are able to perform computations in
the CPU, the FPGA or the GPU, adaptively. Adaptive behavior is controlled
through the &quot;adaptive&quot; ROS 2 parameter.


%package devel
Release:        %{release}%{?release_suffix}
Summary:        %{summary}
Provides:       %{name} = %{version}-%{release}
Provides:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-runtime%{?_isa} = %{version}-%{release}

%description devel
A composable container for Adaptive ROS 2 Node computations. Allows building
Nodes that can select between FPGA, CPU or GPU, at run-time. Stateless by
default, can be made stateful to meet use-case specific needs. Refer to examples
in README. Technically, provides A ROS 2 Node subclass programmed as a
&quot;Component&quot; and including its own single threaded executor to build
adaptive computations. Adaptive ROS 2 Nodes are able to perform computations in
the CPU, the FPGA or the GPU, adaptively. Adaptive behavior is controlled
through the &quot;adaptive&quot; ROS 2 parameter.


%package runtime
Release:        %{release}
Summary:        %{summary}

%description runtime
A composable container for Adaptive ROS 2 Node computations. Allows building
Nodes that can select between FPGA, CPU or GPU, at run-time. Stateless by
default, can be made stateful to meet use-case specific needs. Refer to examples
in README. Technically, provides A ROS 2 Node subclass programmed as a
&quot;Component&quot; and including its own single threaded executor to build
adaptive computations. Adaptive ROS 2 Nodes are able to perform computations in
the CPU, the FPGA or the GPU, adaptively. Adaptive behavior is controlled
through the &quot;adaptive&quot; ROS 2 parameter.


%prep
%autosetup -p1


%generate_buildrequires
%bloom_buildrequires


%build
%cmake \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="%{bloom_prefix}" \
    -DAMENT_PREFIX_PATH="%{bloom_prefix}" \
    -DCMAKE_PREFIX_PATH="%{bloom_prefix}" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif

%cmake3_build


%install
%cmake_install


%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C %{__cmake_builddir} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
CTEST_OUTPUT_ON_FAILURE=1 \
    %cmake_build $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif


%files devel
%dir %{bloom_prefix}
%ghost %{bloom_prefix}/share/%{pkg_name}/package.xml


%files runtime
%{bloom_prefix}


%changelog
* Thu Mar 21 2024 Víctor Mayoral Vilches <victor@accelerationrobotics.com> - 0.2.1-4
- Autogenerated by Bloom
