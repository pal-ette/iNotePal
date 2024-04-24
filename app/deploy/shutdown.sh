#!/bin/sh

ps -ef | grep $(pwd)/.venv/bin/ | grep reflex | grep -v grep | awk '{print $2}' | xargs kill
