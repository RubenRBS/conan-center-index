from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import get, copy
import os

required_conan_version = ">=1.52.0"


class ArteryFontFormatConan(ConanFile):
    name = "artery-font-format"
    description = "Artery Atlas Font format library"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/Chlumsky/artery-font-format"
    topics = ("artery", "font", "atlas", "header-only")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    @property
    def _min_cppstd(self):
        return 11

    def package_id(self):
        self.info.clear()

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def package(self):
        copy(self, pattern="LICENSE.txt", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        copy(
            self,
            pattern="*.h",
            dst=os.path.join(self.package_folder, "include"),
            src=self.source_folder,
        )
        copy(
            self,
            pattern="*.hpp",
            dst=os.path.join(self.package_folder, "include"),
            src=self.source_folder,
        )

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
