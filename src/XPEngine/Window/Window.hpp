#pragma once

#include "../external/glad/include/glad/glad.h"
#include <GLFW/glfw3.h>

namespace XPE{
    class Window{
        GLFWwindow* window = nullptr;
    public:
        Window();
        Window(const char* title, int width, int height);
        bool CreateWindow(const char* title, int width, int height);
        bool IsValid();
        ~Window();
    };

    inline Window CreateWindow(const char* title, int width, int height){
        return Window(title, width, height);
    }
}