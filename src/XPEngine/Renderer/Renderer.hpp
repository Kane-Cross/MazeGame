#pragma once

#include "../external/glad/include/glad/glad.h"
#include <GLFW/glfw3.h>
#include <vector>

namespace XPE{
    class Window;

    class Renderer{
        Window* parent_window;
        std::vector<float> vertices;
        unsigned int VAO;
        std::vector<int> indices;
        unsigned int EBO;
        std::vector<unsigned int> shaders;
    public:
        Renderer();
        Renderer(Window* window);
        bool CreateRenderer(Window* window);
        void SetViewport(int x, int y, int width, int height);
        void DrawRectangle();
        bool IsValid();
        void Destroy();
    };

    inline Renderer CreateRenderer(Window* window){
        return Renderer(window);
    }
}