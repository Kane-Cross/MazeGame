#pragma once

#include "../external/glad/include/glad/glad.h"
#include <GLFW/glfw3.h>

#include "../Renderer/Renderer.hpp"

namespace XPE{
    class Window{
        GLFWwindow* window = nullptr;
        Renderer* bound_renderer;
        bool error = false;
        static void WindowResizeCallback(GLFWwindow* window, int width, int height);
    public:
        Window();
        Window(const char* title, int width, int height);
        bool CreateWindow(const char* title, int width, int height);
        void Show();
        void Hide();
        void Resize(int width, int height);
        void SetCurrent();
        void GetSize(int* x, int* y);
        void SwapBuffers();
        void PollEvents();
        bool WindowShouldClose();
        bool IsValid();

        void BindRenderer(Renderer* renderer);
        Renderer* GetRenderer();
        GLFWwindow* GetWindow();

        void Destroy();
    };

    inline Window CreateWindow(const char* title, int width, int height){
        return Window(title, width, height);
    }
}