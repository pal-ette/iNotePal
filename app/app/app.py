"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

import os
import jdk

jdk_dir = f"{os.getcwd()}/.cache/jdk"
if os.path.isdir(jdk_dir):
    [first_version] = os.listdir(jdk_dir)
    jdk_dir = f"{jdk_dir}/{first_version}"
    print(f"JAVA LOADED: {jdk_dir}")
else:
    jdk_dir = jdk.install("22", path=f"{os.getcwd()}/.cache/jdk")
    print(f"JAVA INSTALLED: {jdk_dir}")
os.environ["JAVA_HOME"] = jdk_dir
os.environ["PATH"] = f"{os.environ.get('PATH')}:{jdk_dir}/bin"

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="tomato",
    )
)
