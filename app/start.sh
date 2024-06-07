#!/usr/bin/env bash
set -e

DEBUG=false
# Parse through arguments
while [[ $# -gt 0 ]]; do  # while there are still arguments

  # check next argument and process it accordingly
  # we use shift to pop the first argument from the argument list
  case "$1" in
    --debug)
      shift
      DEBUG=true
      ;;
    --help|*)
      echo ""
      echo "  --help    show this help message and exit "
      echo "  --debug   run http server in debug mode"
      echo ""
      exit 1
  esac
done

if [ "$DEBUG" = "true" ] ; then
    echo 'Debugging - ON'
    export DEBUG_SERVER_MODE="ON"
    uvicorn main:app --host 0.0.0.0 --port 8080 --log-level "debug" --reload
else
    echo 'Debugging - OFF'
    export DEBUG_SERVER_MODE="OFF"
    # TODO: lower logging level when production ready
    uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4 --log-level "debug"
fi
