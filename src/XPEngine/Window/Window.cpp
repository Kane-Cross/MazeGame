#include "Window.hpp"

namespace XPE{
    Window::Window(){};

    Window::Window(const char* title, int width, int height){
        glfwWindowHint(GLFW_OPENGL_CORE_PROFILE, 4);
        glfwWindowHint(GLFW_OPENGL_API, 6);
    };

    bool Window::CreateWindow(const char* title, int width, int height){

    };

    bool Window::IsValid(){
        return window == nullptr;
    };

    Window::~Window(){
        glfwDestroyWindow(window);
    }
}