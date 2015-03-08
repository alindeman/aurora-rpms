#!/bin/bash
set -e

dir="$1"
if [ -z "$dir" ]; then
  dir="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"
fi
cd $dir

GRADLE_VERSION=2.2
if [ ! -s $dir/gradle-${GRADLE_VERSION}.zip ]; then
  wget -qcL -O $dir/gradle-${GRADLE_VERSION}.zip \
    https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip
fi

mkdir -p $dir/gradle
unzip -oq -d $dir/gradle $dir/gradle-${GRADLE_VERSION}.zip
export GRADLE_HOME=$dir/gradle/gradle-${GRADLE_VERSION}
export PATH=$PATH:$dir/gradle/gradle-${GRADLE_VERSION}/bin

rpmdev-setuptree
trap rpmdev-wipetree EXIT

rpmlint aurora.spec || exit 1
spectool -g -R aurora.spec
rpmbuild -ba aurora.spec

for ddir in RPMS SRPMS; do
  rm -rf $ddir
  cp -Rpv ~/rpmbuild/$ddir .
done
