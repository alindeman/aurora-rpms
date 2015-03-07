#!/bin/bash
set -e

sudo yum install -y rpmdevtools rpmlint yum-utils

# install gradle
GRADLE_VERSION=2.2
if [ ! -s /tmp/gradle-${GRADLE_VERSION}.zip ]; then
  wget -qcL -O /tmp/gradle-${GRADLE_VERSION}.zip \
    https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip
fi

sudo mkdir -p /opt/gradle
sudo unzip -oq -d /opt/gradle /tmp/gradle-${GRADLE_VERSION}.zip
sudo ln -sfn /opt/gradle/gradle-${GRADLE_VERSION} /opt/gradle/latest
export GRADLE_HOME=/opt/gradle/latest
export PATH=$PATH:/opt/gradle/latest/bin

cd /vagrant
rpmdev-setuptree

rpmlint aurora.spec || exit 1
sudo yum-builddep -y aurora.spec
spectool -g -R aurora.spec
rpmbuild -ba aurora.spec

for dir in RPMS SRPMS; do
  rm -rf $dir
  cp -Rpv ~/rpmbuild/$dir .
done
