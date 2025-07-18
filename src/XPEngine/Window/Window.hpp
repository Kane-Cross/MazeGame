#pragma once

#include "../external/glad/include/glad/glad.h"
#include <GLFW/glfw3.h>

namespace XPE{
    class Window{
        GLFWwindow* window;
    public:
        Window();
        Window(const char* title, int width, int height);
        bool CreateWindow();
        bool IsValid();
        ~Window();
    };

    inline Window CreateWindow(){
        return Window();
    }
}