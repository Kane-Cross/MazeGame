#pragma once

#include "../external/glad/include/glad/glad.h"
#include <GLFW/glfw3.h>

#include "../Window/Window.hpp"

namespace XPE{
    class Renderer{
        Window* parent_window;
    public:
        Renderer();
        Renderer(Window* window);
        bool CreateRenderer(Window* window);
        void SetViewport(int x, int y, int width, int height);
        bool IsValid();
        void Destroy();
    };

    inline Renderer CreateRenderer(Window* window){
        return Renderer(window);
    }
}