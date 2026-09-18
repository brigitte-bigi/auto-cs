#!/bin/bash

# ---------------------------------------------------------------------------
# File: make_release.bash
# Author: Brigitte Bigi
# Date: September, 18th, 2026
# Brief: Auto-CS packaging script.
# ---------------------------------------------------------------------------

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROGRAM_NAME="autocs"
PROGRAM_VERSION=$(grep -e '__version__ =' $HERE/autocs/__init__.py | awk -F'=' '{print $2}' | cut -f2 -d'"')
PACKAGE_NAME=`pwd`/dist/${PROGRAM_NAME}-${PROGRAM_VERSION}.zip

echo "Create release for Auto-CS-"$PROGRAM_VERSION

echo "Create documentation"
python makedoc.py
if [ "$?" != 0 ]; then
    echo -e "${RED}No documentation created!${NC}"
    exit 1
fi

echo "Delete any __pycache__ folder"
  for pycache in `find . -name "__pycache__"`;
  do
    rm -rf $pycache;
  done

echo "Create 'zip' archive" $PACKAGE_NAME
  pushd $HERE/autocs
  zip -q -r $PACKAGE_NAME resources sppas
  if [ "$?" != 0 ]; then
      echo -e "${RED}No package created!${NC}"
      popd
      return 1
  else
      popd
      echo "  The file" $PACKAGE_NAME "has been created."
  fi
