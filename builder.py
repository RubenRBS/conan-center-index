import json
import os
import subprocess

import yaml

profiles = [
    "linux-gcc11-shared", "macos-appleclang13-static",
    "linux-gcc11-static", "windows-msvc-192-shared",
    "macos-appleclang13-m1-shared", "windows-msvc-192-static",
    "macos-appleclang13-m1-static", "windows-msvc-193-shared",
    "macos-appleclang13-shared", "windows-msvc-193-static"
]

results = []
to_build = []

recipes_path = "/Users/ruben/coding/conan-center-index/recipes"

try:
    for recipe in os.listdir(recipes_path):
        with open(os.path.join(recipes_path, recipe, "config.yml"), "r") as f:
            config = yaml.safe_load(f)
        for version in config["versions"].keys():
            for profile in profiles:
                try:
                    output = subprocess.check_output(
                        ["conan", "graph", "build-order", f"--requires={recipe}/{version}", "-r=conancenter", f"-pr=/Users/ruben/Downloads/epoch-surgery/profiles/{profile}", "-f=json"])
                    order = json.loads(output)
                    for ref in order:
                        for dependency in ref:
                            for package in dependency["packages"]:
                                for pref in package:
                                    if pref["binary"] == "Missing":
                                        to_build.append(dependency["ref"])
                except subprocess.CalledProcessError as e:
                    print(e.output)
finally:
    names = set([m.split("/")[0] for m in to_build])
    print(names)
