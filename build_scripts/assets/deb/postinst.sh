#!/usr/bin/env bash
# Post install script for the UI .deb to place symlinks in places to allow the CLI to work similarly in both versions

set -e

ln -s /opt/flax/resources/app.asar.unpacked/daemon/flax /usr/bin/flax || true
ln -s /opt/flax/flax-blockchain /usr/bin/flax-blockchain || true
