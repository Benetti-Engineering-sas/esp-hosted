# The following lines of boilerplate have to be in your project's CMakeLists
# in this exact order for cmake to work correctly
cmake_minimum_required(VERSION 3.5)

file(READ "../../../common/include/esp_fw_version.h" HEADER_CONTENTS)
set(PROJECT_VERSION_REGEX "#define[ \t]+PROJECT_NAME[ \t]+\"([A-Z]+)\"[ \t\n]+#define[ \t]+PROJECT_VERSION_MAJOR_1[ \t]+([0-9]+)[ \t\n]+#define[ \t]+PROJECT_VERSION_MAJOR_2[ \t]+([0-9]+)[ \t\n]+#define[ \t]+PROJECT_VERSION_MINOR[ \t]+([0-9]+)[ \t\n]+#define[ \t]+PROJECT_REVISION_PATCH_1[ \t]+([0-9]+)[ \t\n]+#define[ \t]+PROJECT_REVISION_PATCH_2[ \t]+([0-9]+)")
string(REGEX MATCH "${PROJECT_VERSION_REGEX}" PROJECT_VERSION_MATCH "${HEADER_CONTENTS}")

if(PROJECT_VERSION_MATCH)
    set(PROJECT_NAME "${CMAKE_MATCH_1}")
    set(PROJECT_VERSION_MAJOR_1 "${CMAKE_MATCH_2}")
    set(PROJECT_VERSION_MAJOR_2 "${CMAKE_MATCH_3}")
    set(PROJECT_VERSION_MINOR "${CMAKE_MATCH_4}")
    set(PROJECT_REVISION_PATCH_1 "${CMAKE_MATCH_5}")
    set(PROJECT_REVISION_PATCH_2 "${CMAKE_MATCH_6}")

    # Construct project version
    set(PROJECT_VER "${PROJECT_NAME}-${PROJECT_VERSION_MAJOR_1}.${PROJECT_VERSION_MAJOR_2}.${PROJECT_VERSION_MINOR}.${PROJECT_REVISION_PATCH_1}.${PROJECT_REVISION_PATCH_2}")

    message(*************************************************************************************)
    message("                    Building ESP-Hosted Firmware version :: ${PROJECT_VER} ")
    message(*************************************************************************************)
endif()

set(PROJECT_VER "${PROJECT_VER}")
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(network_adapter)
idf_build_set_property(COMPILE_OPTIONS "-fdiagnostics-color=always" APPEND)


idf_component_get_property(lwip lwip COMPONENT_LIB)
target_compile_options(${lwip} PRIVATE "-I${PROJECT_DIR}/main")
target_compile_definitions(${lwip} PRIVATE "-DESP_IDF_LWIP_HOOK_FILENAME=\"esp_hosted_lwip_src_port_hook.h\"")
