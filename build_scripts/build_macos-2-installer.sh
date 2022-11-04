#!/bin/bash

set -o errexit -o nounset

git status
git submodule

# If the env variable NOTARIZE and the username and password variables are
# set, this will attempt to Notarize the signed DMG.

if [ ! "$FLAX_INSTALLER_VERSION" ]; then
	echo "WARNING: No environment variable FLAX_INSTALLER_VERSION set. Using 0.0.0."
	FLAX_INSTALLER_VERSION="0.0.0"
fi
echo "Flax Installer Version is: $FLAX_INSTALLER_VERSION"

echo "Installing npm utilities"
cd npm_macos || exit 1
npm install
PATH=$(npm bin):$PATH
cd .. || exit 1

echo "Create dist/"
sudo rm -rf dist
mkdir dist

echo "Create executables with pyinstaller"
SPEC_FILE=$(python -c 'import flax; print(flax.PYINSTALLER_SPEC_PATH)')
pyinstaller --log-level=INFO "$SPEC_FILE"
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "pyinstaller failed!"
	exit $LAST_EXIT_CODE
fi
cp -r dist/daemon ../flax-blockchain-gui/packages/gui

# Change to the gui package
cd ../flax-blockchain-gui/packages/gui || exit 1

# sets the version for flax-blockchain in package.json
brew install jq
cp package.json package.json.orig
jq --arg VER "$FLAX_INSTALLER_VERSION" '.version=$VER' package.json > temp.json && mv temp.json package.json

echo "Building macOS Electron app"
OPT_ARCH="--x64"
if [ "$(arch)" = "arm64" ]; then
  OPT_ARCH="--arm64"
fi
PRODUCT_NAME="Flax"
if [ "$NOTARIZE" == true ]; then
	echo "Setting credentials for signing"
	export CSC_LINK=$APPLE_DEV_ID_APP
	export CSC_KEY_PASSWORD=$APPLE_DEV_ID_APP_PASS
else
	echo "Not on ci or no secrets so not signing"
	export CSC_IDENTITY_AUTO_DISCOVERY=false
fi
echo electron-builder build --mac "${OPT_ARCH}" --config.productName="$PRODUCT_NAME"
electron-builder build --mac "${OPT_ARCH}" --config.productName="$PRODUCT_NAME"
LAST_EXIT_CODE=$?
ls -l dist/mac*/flax.app/Contents/Resources/app.asar

# reset the package.json to the original
mv package.json.orig package.json

if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-builder failed!"
	exit $LAST_EXIT_CODE
fi

mv dist/* ../../../build_scripts/dist/
cd ../../../build_scripts || exit 1

mkdir final_installer
DMG_NAME="flax-${FLAX_INSTALLER_VERSION}.dmg"
if [ "$(arch)" = "arm64" ]; then
  mv dist/${DMG_NAME} dist/flax-${FLAX_INSTALLER_VERSION}-arm64.dmg
  DMG_NAME=flax-${FLAX_INSTALLER_VERSION}-arm64.dmg
fi
mv dist/$DMG_NAME final_installer/

ls -lh final_installer

if [ "$NOTARIZE" == true ]; then
	echo "Notarize $DMG_NAME on ci"
	cd final_installer || exit 1
  notarize-cli --file="$DMG_NAME" --bundle-id net.flax.blockchain \
	--username "$APPLE_NOTARIZE_USERNAME" --password "$APPLE_NOTARIZE_PASSWORD"
  echo "Notarization step complete"
else
	echo "Not on ci or no secrets so skipping Notarize"
fi

# Notes on how to manually notarize
#
# Ask for username and password. password should be an app specific password.
# Generate app specific password https://support.apple.com/en-us/HT204397
# xcrun altool --notarize-app -f Flax-0.1.X.dmg --primary-bundle-id net.flax.blockchain -u username -p password
# xcrun altool --notarize-app; -should return REQUEST-ID, use it in next command
#
# Wait until following command return a success message".
# watch -n 20 'xcrun altool --notarization-info  {REQUEST-ID} -u username -p password'.
# It can take a while, run it every few minutes.
#
# Once that is successful, execute the following command":
# xcrun stapler staple Flax-0.1.X.dmg
#
# Validate DMG:
# xcrun stapler validate Flax-0.1.X.dmg
