Name: aurora
Version: 0.7.0
Release: 1%{?dist}
Summary: Mesos framework for long-running services and cron jobs
Group: Applications/System
License: Apache-2.0
URL: http://aurora.incubator.apache.org
Source0: https://dist.apache.org/repos/dist/release/incubator/aurora/%{version}/apache-aurora-%{version}-incubating.tar.gz
Source1: https://svn.apache.org/repos/asf/incubator/aurora/3rdparty/centos/7/python/mesos.native-0.20.1-py2.7-linux-x86_64.egg
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: python-devel
BuildRequires: java-1.7.0-openjdk-devel

%define installdir /opt/aurora

%description
Aurora runs applications and services across a shared pool of machines, and is
responsible for keeping them running, forever. When machines experience
failure, Aurora intelligently reschedules those jobs onto healthy machines.

%package scheduler
Summary: Master schedule for Aurora
Requires: mesos

%description scheduler
Provides the master scheduler for Aurora.

%package client
Summary: Client for scheduling services on Aurora

%description client
Provides tools for interacting with the Aurora scheduler.

%package thermos
Summary: A simple Pythonic process management framework for Mesos chroots
Requires: mesos

%description thermos
Provides the Thermos process management framework.

%prep
%setup -q -n apache-aurora-%{version}-incubating

mkdir -p third_party
cp -p %SOURCE1 third_party/

%build
gradle wrapper
./gradlew distTar

./pants binary src/main/python/apache/aurora/admin:aurora_admin
./pants binary src/main/python/apache/aurora/client/cli:aurora
./pants binary src/main/python/apache/aurora/executor/bin:gc_executor
./pants binary src/main/python/apache/aurora/executor/bin:thermos_executor
./pants binary src/main/python/apache/thermos/bin:thermos_runner
./pants binary src/main/python/apache/thermos/observer/bin:thermos_observer

python <<EOF
import contextlib
import zipfile
with contextlib.closing(zipfile.ZipFile('dist/thermos_executor.pex', 'a')) as zf:
  zf.writestr('apache/aurora/executor/resources/__init__.py', '')
  zf.write('dist/thermos_runner.pex', 'apache/aurora/executor/resources/thermos_runner.pex')
EOF

%install
install -d -m 755 %{buildroot}%{installdir}

tar -xvf dist/distributions/aurora-scheduler-%{version}-INCUBATING.tar
mv aurora-scheduler-%{version}-INCUBATING/bin %{buildroot}%{installdir}
mv aurora-scheduler-%{version}-INCUBATING/lib %{buildroot}%{installdir}

install -m 755 dist/aurora_admin.pex %{buildroot}%{installdir}/bin/aurora_admin
install -m 755 dist/aurora.pex %{buildroot}%{installdir}/bin/aurora
install -m 755 dist/gc_executor.pex %{buildroot}%{installdir}/bin/gc_executor
install -m 755 dist/thermos_executor.pex %{buildroot}%{installdir}/bin/thermos_executor
install -m 755 dist/thermos_runner.pex %{buildroot}%{installdir}/bin/thermos_runner
install -m 755 dist/thermos_observer.pex %{buildroot}%{installdir}/bin/thermos_observer

%files scheduler
%{installdir}/bin/aurora-scheduler
%{installdir}/bin/aurora-scheduler.bat
%{installdir}/lib/*

%files client
%defattr(-,root,root,-)
%{installdir}/bin/aurora_admin
%{installdir}/bin/aurora

%files thermos
%defattr(-,root,root,-)
%{installdir}/bin/gc_executor
%{installdir}/bin/thermos_executor
%{installdir}/bin/thermos_runner
%{installdir}/bin/thermos_observer
